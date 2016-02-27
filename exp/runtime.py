import sys
import sys
import time
import json
import hmac
import base64
import hashlib
import requests
import threading
from . import network

import logging

from logging.handlers import RotatingFileHandler




class RuntimeException (Exception):
    pass

class Runtime (object):

  def __init__ (self):
    
    self.is_started = False
    self.auth = None
    self.event = threading.Event()
    self.exception = None

  def configure_logging (self, **kwargs):

   logger = logging.getLogger('exp')

   file_handler_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
   file_handler = RotatingFileHandler('debug.log', mode='a', maxBytes=5*1024*1024, backupCount=5, encoding=None, delay=0)
   file_handler.setFormatter(file_handler_formatter)
   file_handler.setLevel(logging.DEBUG)
   logger.addHandler(file_handler)

   stream_handler_formatter = logging.Formatter('EXP/%(levelname)-10s: %(message)s')
   stream_handler = logging.StreamHandler()
   stream_handler.setLevel(logging.INFO)
   stream_handler.setFormatter(stream_handler_formatter)
   logger.addHandler(stream_handler)

   logger.setLevel(logging.DEBUG)
   self.logger = logger


  def start (self, enable_events=True, host='https://api.goexp.io', **kwargs):
    self.configure_logging(**kwargs)
    self.logger.info('Starting runtime.')
    if self.is_started:
      raise RuntimeException('Runtime already started.')
    self.is_started = True

    self.options = kwargs
    self.options['host'] = host
    self.options['enable_events'] = enable_events

    if not self.options.get('port'):
      if self.options.get('host').startswith('http:'):
        self.options['port'] = 80
      else:
        self.options['port'] = 443

    thread = threading.Thread(target=lambda: self.fork())
    thread.daemon = True
    thread.start()
    self.event.wait()

    if self.exception:
      raise self.exception
    self.logger.info('Connected to EXP.')

  def fork (self):
    try:
      self.validate()
      self.login()
    except Exception as exception:
      self.logger.critical('Runtime aborted due to error: %s', exception)
      self.exception = exception
      self.event.set()

  def validate (self):
    self.logger.debug('Validating runtime options: %s', self.options)
    if self.options.get('type') is 'user' or self.options.get('username') or self.options.get('password') or self.options.get('organization'):
      self.logger.debug('Validating user credentials.')
      self.options['type'] = 'user'
      if not self.options.get('username'):
        raise RuntimeException('Please specify the username.')
      if not self.options.get('password'):
        raise RuntimeException('Please specify the password.')
      if not self.options.get('organization'):
        raise RuntimeException('Please specify the organization.')
    elif self.options.get('type') is 'device' or self.options.get('secret'):
      self.logger.debug('Validating device credentials.')
      self.options['type'] = 'device'
      if not self.options.get('uuid') and not self.options.get('allow_pairing'):
        raise RuntimeException('Please specify the device uuid.')
      if not self.options.get('secret') and not self.options.get('allow_pairing'):
        raise RuntimeException('Please specify the device secret.')
    elif self.options.get('type') is 'consumer_app' or self.options.get('api_key'):
      self.logger.debug('Validating consumer app credentials.')
      self.options['type'] = 'consumer_app'
      if not self.options.get('uuid'):
        raise RuntimeException('Please specify the consumer app uuid.')
      if not self.options.get('api_key'):
        raise RuntimeException('Please specify the consumer app api key.')
    else:
      raise RuntimeException('Please specify authentication type.')


  def login (self):
    payload = {}
    if self.options.get('type') is 'user':
      self.logger.debug('Authenticating as a user.')
      payload['type'] = 'user'
      payload['username'] = self.options.get('username')
      payload['password'] = self.options.get('password')
      payload['organization'] = self.options.get('organization')
    elif self.options.get('type') is 'device':
      self.logger.debug('Authenticating as a device.')
      token_payload = {}
      token_payload['type'] = 'device'
      token_payload['uuid'] = self.options.get('uuid', '_')
      token_payload['allowPairing'] = self.options.get('allow_paiing')
      payload['token'] = self.generate_jwt(token_payload, self.options.get('secret', '_'))
    elif self.options.get('type') is 'consumer_app':
      self.logger.debug('Authenticating as a consumer app.')
      token_payload = {}
      token_payload['type'] = 'consumerApp'
      token_payload['uuid'] = self.options.get('uuid', '_')
      payload['token'] = self.generate_jwt(token_payload, self.options.get('apiKey', '_'))
    response = requests.request('POST', self.options.get('host') + '/api/auth/login', json=payload)
    if response.status_code is 401:
      self.logger.critical('Credentials invalid. Runtime cannot continue.')
      raise RuntimeException('Invalid credentials.')
    elif response.status_code is 200:
      self.logger.debug('Login successful.')
      self.on_update(response)
    else:
      self.logger.warning('Unknown error trying to login. Retrying in five seconds.')
      time.sleep(5)
      self.login()

  def refresh (self):
    self.logger.debug('Refresing authentication token.')
    headers = { 'Authorization': 'Bearer ' + self.auth['token'] }
    response = requests.request('POST', self.options.get('host') + '/api/auth/token', headers=headers)
    if response.status_code is 401:
      self.logger.warning('Token refresh failed due to invalid authentication.')
      self.login()
    elif response.status_code is 200:
      self.logger.debug('Token refresh successful.')
      self.on_update(response)
    else:
      self.logger.warning('Token refresh failed for unknown reason.')
      time.sleep(5)
      self.refresh()

  def on_update(self, response):
    self.auth = response.json()
    self.logger.debug('Authentication updated: %s', json.dumps(self.auth, indent=4, separators=(',', ': ')))
    self.event.set()
    time.sleep((self.auth['expiration'] - int(time.time())*1000.0) / 2.0 / 1000.0)
    self.refresh()

  @staticmethod
  def generate_jwt (payload, secret):

    algorithm = { 'alg': 'hs256', 'typ': 'JWT' }
    algorithm_json = json.dumps(algorithm, separators(',', ':')).encode('utf-8')
    algorithm_b64 = base64.urlsafe_b64encode(algorithm_json)

    payload['exp'] = (int(time.time()) + 30) * 1000
    payload_json = json.dumps(payload, separators(',', ':')).encode('utf-8')
    payload_b64 = base64.urlsafe_b64encode(payload_json).rstrip('=')

    signature = hmac.new(secret.encode('utf-8'), '.'.join([algorithm_b64, payload_b64]), hashlib.sha256).digest()
    signature_b64 = urlsafe_b64encode(signature).rstrip('=')

    return '.'.join([algorithm_b64, payload_b64, signature_b64])

runtime = Runtime()
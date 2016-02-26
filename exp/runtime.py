


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


class RuntimeException (Exception):
    pass

class Runtime (object):

  def __init__ (self):
    self.is_started = False
    self.auth = None
    self.semaphore = threading.Semaphore()
    self.exception = None

  @property
  def RuntimeException ():
    return RuntimeException

  def start (self, enable_events=True, host='https://api.goexp.io', **kwargs):
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

    if self.exception:
      raise self.exception

    self.semaphore.acquire()

    if self.exception:
      raise self.exception


  def fork (self):
    try:
      self.validate()
      self.login()
    except Exception as exception:
      self.exception = exception
    finally:
      self.semaphore.release()


  def validate (self):
    if self.options.get('type') is 'user' or self.options.get('username') or self.options.get('password') or self.options.get('organization'):
      self.options['type'] = 'user'
      if not self.options.get('username'):
        self.abort(RuntimeException('Please specify the username.'))
      if not self.options.get('password'):
        raise RuntimeException('Please specify the password.')
      if not self.options.get('organization'): raise RuntimeException('Please specify the organization.')
    elif self.options.get('type') is 'device' or self.options.get('secret'):
      self.options['type'] = 'device'
      if not self.options.get('uuid') and not self.options.get('allow_pairing'): raise RuntimeException('Please specify the device uuid.')
      if not self.options.get('secret') and not self.options.get('allow_pairing'): raise RuntimeException('Please specify the device secret.')
    elif self.options.get('type') is 'consumer_app' or self.options.get('api_key'):
      self.options['type'] = 'consumer_app'
      if not self.options.get('uuid'): raise RuntimeException('Please specify the consumer app uuid.')
      if not self.options.get('api_key'): raise RuntimeException('Please specify the consumer app api key.')
    else:
      raise RuntimeException('Please specify authentication type.')


  def login (self):
    print 'Logging in to exp.'
    payload = {}
    if self.options.get('type') is 'user':
      payload['type'] = 'user'
      payload['username'] = self.options.get('username')
      payload['password'] = self.options.get('password')
      payload['organization'] = self.options.get('organization')
    elif self.options.get('type') is 'device':
      token_payload = {}
      token_payload['type'] = 'device'
      token_payload['uuid'] = self.options.get('uuid', '_')
      token_payload['allowPairing'] = self.options.get('allow_paiing')
      payload['token'] = self.generate_jwt(token_payload, self.options.get('secret', '_'))
    elif self.options.get('type') is 'consumer_app':
      token_payload = {}
      token_payload['type'] = 'consumerApp'
      token_payload['uuid'] = self.options.get('uuid', '_')
      payload['token'] = self.generate_jwt(token_payload, self.options.get('apiKey', '_'))
    response = requests.request('POST', self.options.get('host') + '/api/auth/login', json=payload)
    if response.status_code is 401:
      raise RuntimeException('Invalid credentials.')
    elif response.status_code is 200:
      print 'GOT CREDS'
      self.auth = response.json()
      # Release the semaphore
      time.sleep((self.auth['expiration'] - int(time.time())) / 2.0 / 1000.0)
      self.refresh()
    else:
      print 'REQUEST FAILED'
      time.sleep(5)
      self.login()

  def refresh (self):
    print 'Refresh'
    headers = { 'Authorization': 'Bearer ' + self.auth['token'] }
    response = requests.request('POST', self.options.get('host') + '/api/auth/token', headers=headers)
    if response.status_code is 401:
      self.login()
    elif response.status_code is 200:
      self.auth = response.json()
      time.sleep((self.auth['expiration'] - int(time.time())) / 2.0 / 1000.0)
    else:
      time.sleep(5)
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

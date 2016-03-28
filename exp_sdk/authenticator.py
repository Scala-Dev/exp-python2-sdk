import time
import traceback
import requests
import json
import base64
import hmac
import hashlib
import threading

from exp_sdk import exceptions


class Authenticator (object):

  def __init__(self, sdk):
    self._sdk = sdk
    self._auth = None
    self._time = None
    self._failed = False
    self._lock = threading.Lock()

  def get_auth(self):
    self._lock.acquire()
    if self._failed:
      self._lock.release()
      raise exceptions.AuthenticationError('Invalid credentials. Please restart the SDK with valid credentials.')
    try:
      if not self._auth:
        self._login()
      elif self._time < int(time.time()):
        self._refresh()
    except:
      self._lock.release()
      raise
    self._lock.release()
    return self._auth

  def _login (self):
    payload = {}
    self._sdk.logger.debug('Login starting.')
    if self._sdk.options.get('type') is 'user':
      self._sdk.logger.debug('Login generating user payload.')
      payload['username'] = self._sdk.options.get('username')
      payload['password'] = self._sdk.options.get('password')
      payload['organization'] = self._sdk.options.get('organization')
    elif self._sdk.options.get('type') is 'device':
      self._sdk.logger.debug('Login generating device payload.')
      token_payload = {}
      token_payload['uuid'] = self._sdk.options.get('uuid') or '_'
      token_payload['type'] = 'device'
      token_payload['allowPairing'] = self._sdk.options.get('allow_pairing')
      payload['token'] = self.generate_jwt(token_payload, self._sdk.options.get('secret') or '_')
    elif self._sdk.options.get('type') is 'consumer_app':
      self._sdk.logger.debug('Login generating consumer app payload.')
      token_payload = {}
      token_payload['type'] = 'consumerApp'
      token_payload['uuid'] = self._sdk.options.get('uuid') or '_'
      payload['token'] = self.generate_jwt(token_payload, self._sdk.options.get('api_key'))
    url = self._sdk.options.get('host') + '/api/auth/login'
    self._sdk.logger.debug('Sending login payload: %s' % payload)
    try:
      response = requests.request('POST', url, json=payload)
    except Exception as exception:
      self._sdk.logger.warn('Login encountered an unexpected error.')
      self._sdk.logger.debug('Login encountered an unexpected error: %s', traceback.format_exc())
      self._auth = None
      self._time = None
      raise exceptions.UnexpectedError('Login encountered an unexpected error.')
    if response.status_code == 200:
      self._sdk.logger.debug('Login request successful.')
      self._on_success(response)
    elif response.status_code == 401:
      self._sdk.logger.critical('Invalid credentials.')
      self._sdk.logger.debug('Invalid credentials.')
      self._sdk.network.stop()
      self._auth = None
      self._time = None
      self._failed = True
      raise exceptions.AuthenticationError('Invalid credentials.')
    else:
      self._sdk.logger.warn('Login received an unexpected HTTP status code: %s.' % response.status_code)
      self._sdk.logger.debug('Login received an unexpected HTTP status code: %s' % response.status_code)
      self._auth = None
      self._time = None
      raise exceptions.UnexpectedError('Login received an unexpected HTTP status code: %s.' % response.status_code)

  def _refresh (self):
    self._sdk.logger.debug('Authentication token refresh starting.')
    url = self._sdk.options.get('host') + '/api/auth/token'
    headers = { 'Authorization': 'Bearer ' + self._auth.get('token') }
    self._sdk.logger.debug('Sending token refresh request.')
    try:
      response = requests.request('POST', url, headers=headers)
    except Exception as exception:
      self._sdk.logger.warn('Token refresh encountered an unexpected error.')
      self._sdk.logger.debug('Token refresh encountered an unexpected error: %s.', traceback.format_exc())
      self._auth = None
      self._time = None
      raise UnexpectedError('Token refresh encountered an unexpected error.')
    if response.status_code == 200:
      self._sdk.logger.debug('Token refresh request successful.')
      self._on_success(response)
    elif response.status_code == 401:
      self._sdk.logger.warn('Token refresh request failed due to expired or invalid token.')
      self._sdk.logger.debug('Token refresh request failed due to expired or invalid token.')
      self._auth = None
      self._time = None
      self._login()
    else:
      self._sdk.logger.warn('Token refresh request received an unexpected HTTP status code: %s.' % response.status_code)
      self._sdk.logger.debug('Token refresh request receive an unexpected HTTP status code: %s' % response.status_code)
      self._auth = None
      self._time = None
      raise exceptions.UnexpectedError('Token refresh request receive an unexpected HTTP status code: %d' % response.status_code)

  def _on_success (self, response):
    self._sdk.logger.debug('Authentication update starting.')
    try:
      auth = response.json()
    except Exception as exception:
      self._sdk.logger.warn('Authentication update encountered an unexpected error.')
      self._sdk.logger.debug('Authentication updated encountered an unexpected error:' % traceback.format_exc())
      self._auth = None
      self._time = None
      raise exceptions.UnexpectedError('Authentication update encountered an unexpected error.')
    self._auth = auth
    self._time = (int(time.time()) + auth['expiration'] * 3.0 / 1000.0 ) / 4.0
    self._sdk.logger.debug('Authentication update successful: %s' % auth)

  @staticmethod
  def generate_jwt (payload, secret):

    algorithm = { 'alg': 'HS256', 'typ': 'JWT' }
    algorithm_json = json.dumps(algorithm, separators=(',', ':')).decode('utf-8')
    algorithm_b64 = base64.urlsafe_b64encode(algorithm_json).rstrip('=')

    payload['exp'] = (int(time.time()) + 30) * 1000
    payload_json = json.dumps(payload, separators=(',', ':'))
    payload_b64 = base64.urlsafe_b64encode(payload_json).rstrip('=')

    signature = hmac.new(secret, '.'.join([algorithm_b64, payload_b64]), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).rstrip('=')

    return '.'.join([algorithm_b64, payload_b64, signature_b64])



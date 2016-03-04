import time
import traceback
import requests
import json
import base64
import hmac
import hashlib

from .logger import logger
from .exceptions import AuthenticationError, UnexpectedError, RuntimeError

class _Authenticator (object):

  def __init__(self):
    self._auth = None
    self._options = None
    self._time = None

  def configure (self, **options):
    self._options = options
    self._auth = None

  def get_auth(self):
    if not self._options:
      raise RuntimeError('SDK has not been configured.')
    elif not self._auth:
      self._login()
    elif self._time < int(time.time()):
      self._refresh()
    return self._auth

  def _login (self):
    payload = {}
    if self._options.get('type') is 'user':
      logger.debug('Login started as a user.')
      payload['username'] = self._options.get('username')
      payload['password'] = self._options.get('password')
      payload['organization'] = self._options.get('organization')
    elif self._options.get('type') is 'device':
      logger.debug('Login started as a device.')
      token_payload = {}
      token_payload['uuid'] = self._options.get('uuid') or '_'
      token_payload['allowPairing'] = self._options.get('allow_pairing')
      payload['token'] = self.generate_jwt(token_payload, self._options.get('secret') or '_')
    elif self._options.get('type') is 'consumer_app':
      logger.debug('Login started as a consumer app.')
      token_payload = {}
      token_payload['uuid'] = self._options.get('uuid') or '_'
      payload['token'] = self.generate_jwt(token_payload, self._options.get('api_key'))
    url = self._options.get('host') + '/api/auth/login'
    response = requests.request('POST', url, json=payload)
    if response.status_code == 200:
      self._on_success(response)
      logger.debug('Login successful.')
    elif response.status_code == 401:
      raise AuthenticationError('Login failed due to invalid credentials.')
    else:
      raise UnexpectedError('Login failed due to an unexpected HTTP status code: %s.' % response.status_code)

  def _refresh (self):
    logger.debug('Authentication token refresh starting.')
    url = self._options.get('host') + '/api/auth/token'
    headers = { 'Authorization': 'Bearer ' + self._auth.get('token') }
    try:
      response = requests.request('POST', url, headers=headers)
    except Exception as exception:
      raise UnexpectedError('Authentication token refresh encountered an unexpected error.')
    if response.status_code is 200:
      self._on_success(response)
      logger.debug('Authentication token refresh successful.')
    elif response.status_code is 401:
      logger.debug('Authentication token refresh failed due to expired or invalid token.')
      self._login()
    else:
      raise UnexpectedError('Authentication token refresh request failed due to an unexpected HTTP status code: %d' % response.status_code)

  def _on_success (self, response):
    logger.debug('Authentication update starting.')
    try:
      auth = response.json()
    except Exception as exception:
      raise UnexpectedError('An unexpected error has occured parsing authentication response.')
    else:
      logger.critical(auth)
      logger.critical(response.status_code)
      self._auth = auth
      self._time = (int(time.time()) + auth['expiration'] * 3.0 / 1000.0 ) / 4.0
      logger.debug('Authentication update successful: %s' % auth)

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


authenticator = _Authenticator()
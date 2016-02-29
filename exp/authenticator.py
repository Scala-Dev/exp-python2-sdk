import time
import traceback
import requests

from .logger import logger
from .exceptions import AuthenticationError, UnexpectedError, NotAuthenticatedError

class _Authenticator (object):

  def __init__(self):
    self._auth = None
    self._do_stop = False
    self._exception = None
    self._options = None

  def get_auth(self):
    if not self._auth:
      raise NotAuthenticatedError()
    return self._auth


  def start (self, **options):
    self._options = options
    self._main_event_loop()


  def stop (self):
    self._do_stop = True


  def wait (self):
    while not self._auth and not self._do_stop and not self._exception:
      time.sleep(.5)
    if self._exception:
      raise self._exception


  def _main_event_loop (self):
    while not self._do_stop:
      if self._auth and self._is_refresh_needed:
        self._auth = self._refresh()
      elif not self._auth:
        self._auth = self._login()
      time.sleep(1)

  @property
  def _is_refresh_needed (self):
    return self._auth.get('expiration') / 1000.0 - int(time.time()) < 3600


  def _login (self):
    logger.info('Logging into EXP.')
    try:
      auth = self._get_login_response()
    except AuthenticationError as exception:
      logger.critical('Authentication failed. Credentials are invalid.')
      self._exception = exception
    except Exception as exception:
      logger.warning('Authentication failed for unexpected reason. See debug log for more information.')
      logger.debug(traceback.format_exc())
    else:
      logger.info('Login successful.')
      return auth

  def _refresh (self):
    logger.info('Refreshing authentication token.')
    try:
      auth = self._get_refresh_response()
    except Exception as exception:
      logger.warning('Authentication token refresh failed.')
      logger.debug(traceback.format_exc())
    else:
      logger.info('Authentication token refresh successful.')
      return auth


  def _get_login_payload (self):
    if self._options.get('type') is 'user':
      return self._get_user_login_payload()
    elif self._options.get('type') is 'device':
      return self._get_device_login_payload()
    elif self._options.get('type') is 'consumer_app':
      return self._get_consumer_app_login_payload()


  def _get_user_login_payload (self):
    payload = {}
    payload['username'] = self._options.get('username')
    payload['password'] = self._options.get('password')
    payload['organization'] = self._options.get('organization')
    return payload


  def _get_device_login_payload (self):
    payload = {}
    token_payload = {}
    token_payload['uuid'] = self._options.get('uuid') or '_'
    token_payload['allowPairing'] = self._options.get('allow_pairing')
    payload['token'] = self.generate_jwt(token_payload, self._options.get('secret') or '_')
    return payload


  def _get_consumer_app_login_payload (self):
    payload = {}
    token_payload = {}
    token_payload['uuid'] = self._options.get('uuid') or '_'
    payload['token'] = self.generate_jwt(token_payload, self._options.get('api_key'))
    return payload


  def _get_login_url (self):
    return self._options.get('host') + '/api/auth/login'


  def _get_refresh_url (self):
    return self._options.get('host') + '/api/auth/token'


  def _get_login_response (self):    
    response = requests.request('POST', self._get_login_url(), json=self._get_login_payload())
    if response.status_code == 200:
      return response.json()
    elif response.status_code == 401:
      raise AuthenticationError('Authentiation failed.')
    else:
      raise UnexpectedError('Authentication failed due to an unexpected status code: %s.' % response.status_code)


  def _get_refresh_headers (self):
    return { 'Authorization': 'Bearer ' + self._auth.get('token') }


  def _get_refresh_response (self):
    response = requests.request('POST', self._get_refresh_url(), headers=self._get_refresh_headers())
    if response.status_code is 200:
      return response.json()
    elif response.status_code is 401:
      raise AuthenticationError('Authentication failed.')
    else:
      raise UnexpectedError('Authentication token refresh failed due to an unexpected status code: %d.' % response.status_code)


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


authenticator = _Authenticator()
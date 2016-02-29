
from .logger import logger
from .exceptions import AuthenticationError, UnexpectedError

class _Authenticator (object):

  def start (self, **options):
    pass

  def wait (self):
    pass

  @classmethod
  def login (cls, **kwargs):
    return cls._get_login_response(**kwargs)

  @classmethod
  def refresh (cls, **kwargs):
    try:
      return cls._get_refresh_response(**kwargs)
    except AuthenticationError as exception:
      logger.warning('Authentication token refresh failed.')
      logger.debug(traceback.format_exc())
      return cls._login(**kwargs)


  def on_update(self, response):
    self.auth = response.json()
    self.logger.debug('Authentication updated: %s', json.dumps(self.auth, indent=4, separators=(',', ': ')))
    network.connect(self.auth)
    self.event.set()
    time.sleep((self.auth['expiration'] - int(time.time())*1000.0) / 2.0 / 1000.0)
    self.refresh()

  @classmethod
  def _get_login_response (cls, type=None, host=None,
    username=None, password=None, organization=None,
    uuid=None, secret=None, api_key=None, allow_pairing=None, **kwargs):
    payload = {}
    if type is 'user':
      logger.debug('Logging in as a user.')
      payload['type'] = 'user'
      payload['username'] = username
      payload['password'] = password
      payload['organization'] = organization
    elif type is 'device':
      logger.debug('Logging in as a device.')
      token_payload = {}
      token_payload['type'] = 'device'
      token_payload['uuid'] = uuid or '_'
      token_payload['allowPairing'] = allow_pairing
      payload['token'] = self.generate_jwt(token_payload, secret or '_')
    elif self.options.get('type') is 'consumer_app':
      logger.debug('Logging in as a consumer app.')
      token_payload = {}
      token_payload['type'] = 'consumerApp'
      token_payload['uuid'] = uuid
      payload['token'] = self.generate_jwt(token_payload, api_key)
    response = requests.request('POST', host + '/api/auth/login', json=payload)
    if response.status_code is 200:
      logger.debug('Login successful.')
      return response.json()
    elif response.status_code is 401:
      raise exceptions.AuthenticationFailed('Authentication failed.')
    else:
      raise exceptions.UnexpectedError('Authentication failed due to an unexpected status code: %s.' % response.status_code)

  @classmethod
  def _get_refresh_response (cls, token=None, host=None, **kwargs):
    headers = { 'Authorization': 'Bearer ' + token }
    response = requests.request('POST', host + '/api/auth/token', headers=headers)
    if response.status_code is 200:
      logger.debug('Authentication token refresh sucessful.')
      return response.json()
    elif response.status_code is 401:
      raise exceptions.AuthenticationFailed('Authentication token refresh failed due to invalid or expired token.')
    else:
      raise exceptions.UnexpectedError('Authentication token refresh failed due to an unexpected status code: %d.' % response.status_code)

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
import time
import requests
import json
import hmac
from hashlib import sha256
from base64 import urlsafe_b64encode


_vars = {}
_vars["uuid"] = None
_vars["secret"] = None
_vars["username"] = None
_vars["password"] = None
_vars["token"] = None
_vars["time"] = 0
_vars["networkUuid"] = None
_vars["apiKey"] = None

def _reset():
  _vars["uuid"] = None
  _vars["secret"] = None
  _vars["username"] = None
  _vars["password"] = None
  _vars["organization"] = None
  _vars["token"] = None
  _vars["time"] = 0
  _vars["networkUuid"] = None
  _vars["apiKey"] = None

def _jwtHS256encode(payload, secret):
  alg = urlsafe_b64encode('{"alg":"HS256","typ":"JWT"}')
  if not isinstance(payload, basestring):
    payload = json.dumps(payload, separators=(',', ':'))
  payload = urlsafe_b64encode(payload.encode("utf-8")).rstrip('=')
  sign = urlsafe_b64encode(hmac.new(secret.encode("utf-8"), '.'.join([alg, payload]), sha256).digest()).rstrip('=')
  return '.'.join([alg, payload, sign])

def set_user_credentials(username, password, organization):
  _reset()
  _vars["username"] = username
  _vars["password"] = password
  _vars["organization"] = organization

def set_device_credentials(uuid, secret):
  _reset()
  _vars["uuid"] = uuid
  _vars["secret"] = secret

def set_network_credentials(uuid, apiKey):
  _reset()
  _vars["networkUuid"] = uuid
  _vars["apiKey"] = apiKey

def set_token(token):
  _reset()
  _vars["token"] = token
  _vars["time"] = float("inf")

def get_token():
  if not _vars["token"] or time.time() - _vars["time"] < 120:
    _generate_token()
  return _vars["token"]

def _generate_token():
  if _vars["uuid"] and _vars["secret"]:
    _generate_device_token()
  elif _vars["username"] and _vars["password"]:
    _generate_user_token()
  elif _vars["networkUuid"] and _vars["apiKey"]:
    _generate_network_token()
  else:
    _vars["token"] = ''
    _vars["time"] = 0

def _generate_user_token():
  from . import api_utils  # Avoid circular import.
  _vars["token"] = api_utils.authenticate(_vars["username"], _vars["password"], _vars["organization"])
  _vars["time"] = time.time()

def _generate_device_token():
  payload = {}
  payload["uuid"] = cls._uuid
  _vars["token"] = _jwtHS256encode(payload, _vars["secret"])
  _vars["time"] = time.time()

def _generate_network_token():
  payload = {}
  payload["networkUuid"] = _vars["networkUuid"]
  _vars["token"] = _jwtHS256encode(payload, _vars["apiKey"])
  _vars["time"] = time.time()
      

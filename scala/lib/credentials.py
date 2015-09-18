import time
import requests
import jwt


_vars = {}
_vars["uuid"] = None
_vars["secret"] = None
_vars["username"] = None
_vars["password"] = None
_vars["token"] = None
_vars["time"] = 0

def _reset():
  _vars["uuid"] = None
  _vars["secret"] = None
  _vars["username"] = None
  _vars["password"] = None
  _vars["organization"] = None
  _vars["token"] = None
  _vars["time"] = 0

def set_user_credentials(username, password, organization):
  _reset()
  _vars["username"] = username
  _vars["password"] = password
  _vars["organization"] = organization

def set_device_credentials(uuid, secret):
  _reset()
  _vars["uuid"] = uuid
  _vars["secret"] = secret

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
  _vars["token"] = jwt.encode(payload, _vars["secret"], algorithm="HS256")
  _vars["time"] = time.time()
      

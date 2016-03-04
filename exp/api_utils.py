import requests
import urllib

from .logger import logger
from .exceptions import ApiError, UnexpectedError
from .authenticator import authenticator

def _on_error(exception):
  if hasattr(exception, 'response'):
    try:
      payload = exception.response.json()
    except Exception:
      raise UnexpectedError()
    else:
      raise ApiError(payload)
  else:
    raise UnexpectedError()


def get(path, params=None):
  try:
    url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
    headers = {}
    headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
    response = requests.get(url, timeout=10, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
  except Exception as exception:
    return _on_error(exception)

def post(path, payload=None, params=None):
  try:
    url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
    headers = {}
    headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
    response = requests.post(url, timeout=10, params=params, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
  except Exception as exception:
    return _on_error(exception)

def patch(path, payload=None, params=None):
  try:
    url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
    headers = {}
    headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
    response = requests.patch(url, timeout=10, params=params, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
  except Exception as exception:
    return _on_error(exception)

def put(path, payload=None, params=None):
  try:
    url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
    headers = {}
    headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
    response = requests.put(url, timeout=10, params=params, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
  except Exception as exception:
    return _on_error(exception)

def delete(path, payload=None, params=None):
  try:
    url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
    headers = {}
    headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
    response = requests.delete(url, timeout=10, params=params, json=payload, headers=headers)
    response.raise_for_status()
    return None
  except Exception as exception:
    return _on_error(exception)


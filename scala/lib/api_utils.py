import requests

from . import config
from . import credentials

def _generate_url(path):
  url = config.get("host")
  if config.get("port"):
    url = url + ':' + str(config.get("port"))
  url = url + path
  return url

def authenticate(username, password, organization):
  url = _generate_url("/api/auth/login")
  payload = {}
  payload["username"] = username
  payload["password"] = password
  payload["org"] = organization
  response = requests.post(url, json=payload)
  response.raise_for_status()
  body = response.json()
  return body["token"]

def get(path, params=None):
  url = _generate_url(path)
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.get(url, params=params, headers=headers)
  response.raise_for_status()
  return response.json()

def post(path, payload=None, params=None):
  url = _generate_url(path)
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.post(url, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def patch(path, payload=None, params=None):
  url = _generate_url(path)
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.patch(url, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def delete(path, payload=None, params=None):
  url = _generate_url(path)
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.delete(url, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()


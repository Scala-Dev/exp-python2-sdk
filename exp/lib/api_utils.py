import requests
import urllib

from . import config
from . import credentials

def get_timeout():
  return config.get('timeout') or 10

def generate_url(path):
  base = config.get("host")
  if config.get("port"):
    base = "{0}:{1}".format(base, config.get("port"))
  return "{0}{1}".format(base, urllib.quote(path))

def authenticate(username, password, organization):
  url = generate_url("/api/auth/login")
  payload = {}
  payload["username"] = username
  payload["password"] = password
  payload["org"] = organization
  response = requests.post(url, json=payload)
  response.raise_for_status()
  body = response.json()
  return body["token"]

def get(path, params=None):
  url = generate_url(path)
  headers = {}
  timeout = get_timeout()  
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.get(url, timeout=timeout, params=params, headers=headers)
  response.raise_for_status()
  return response.json()

def post(path, payload=None, params=None):
  url = generate_url(path)
  timeout = get_timeout()
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.post(url, timeout=timeout, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def patch(path, payload=None, params=None):
  url = generate_url(path)
  timeout = get_timeout()
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.patch(url, timeout=timeout, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def put(path, payload=None, params=None):
  url = generate_url(path)
  timeout = get_timeout()
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.put(url, timeout=timeout, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def delete(path, payload=None, params=None):
  url = generate_url(path)
  timeout = get_timeout()
  headers = {}
  headers["Authorization"] = "Bearer " + credentials.get_token()
  response = requests.delete(url, timeout=timeout, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()


import requests
import urllib

from .authenticator import authenticator


def get(path, params=None):
  url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
  headers = {}
  headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
  response = requests.get(url, timeout=10, params=params, headers=headers)
  response.raise_for_status()
  return response.json()

def post(path, payload=None, params=None):
  url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
  headers = {}
  headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
  response = requests.post(url, timeout=10, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def patch(path, payload=None, params=None):
  url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
  headers = {}
  headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
  response = requests.patch(url, timeout=10, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def put(path, payload=None, params=None):
  url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
  headers = {}
  headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
  response = requests.put(url, timeout=10, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()

def delete(path, payload=None, params=None):
  url = "{0}{1}".format(authenticator.get_auth()['api']['host'], urllib.quote(path))
  headers = {}
  headers["Authorization"] = "Bearer " + authenticator.get_auth()['token']
  response = requests.delete(url, timeout=10, params=params, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()


import requests
import json

from . import config
from . import credentials

def _generate_url(path):
  url = config.get("host")
  if config.get("port"):
    url = url + ':' + config.get("port")
  url = url + path
  return url

def authenticate(username, password):
  url = _generate_url("/api/auth/login")
  payload = {}
  payload["username"] = _vars["username"]
  payload["password"] = _vars["password"]
  payload["org"] = _vars["organization"]
  response = requests.post(url, data=json.dumps(payload))
  response.raise_for_status()
  body = response.json()
  return body["token"]

def post(path, payload=payload):
  url = _generate_url(path)
  headers["Authorization"] = "Bearer " + credentials.get_token()



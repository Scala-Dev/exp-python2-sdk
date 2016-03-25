import urllib
import requests
import traceback



class Api (object):

  def __init__(self, sdk):
    self._sdk = sdk

  def _get_url (self, path):
    return '{0}{1}'.format(self._sdk.authenticator.get_auth()['api']['host'], urllib.quote(path))

  def _get_headers (self):
    return { 'Authorization': 'Bearer ' + self._sdk.authenticator.get_auth()['token'] }

  def _on_error(self, exception):
    if hasattr(exception, 'response'):
      try:
        payload = exception.response.json()
      except:
        self._sdk.logger.warn('API call encountered an unexpected error.')
        self._sdk.logger.debug('API call encountered an unexpected error: %s' % traceback.format_exc())
        raise self._sdk.exceptions.UnexpectedError('API call encountered an unexpected error.')
      else:
        raise self._sdk.exceptions.ApiError(payload)
    else:
      self._sdk.logger.warn('API call encountered an unexpected error.')
      self._sdk.logger.debug('API call encountered an unexpected error: %s' % traceback.format_exc())
      raise self._sdk.exceptions.UnexpectedError('API call encountered an unexpected error.')


  def get(self, path, params=None, timeout=10):
    try:
      response = requests.get(self._get_url(path), timeout=timeout, params=params, headers=self._get_headers())
      if response.status_code == 404:
        return None
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def post(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.post(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def patch(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.patch(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def put(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.put(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def delete(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.delete(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

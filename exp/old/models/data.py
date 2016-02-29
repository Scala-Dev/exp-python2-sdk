import urllib

from .. import api_utils

class Data(object):

  def __init__(self, key=None, group=None, value=None, **kwargs):
    self.key = key
    self.group = group
    self.value = value
    encoded_key = urllib.quote_plus(key)
    encoded_group = urllib.quote_plus(group)
    self._path = '/api/data/{0}/{1}'.format(encoded_group, encoded_key)

  def save(self):
    api_utils.put(self._path, payload=self.value)
    return self

  def delete(self):
    api_utils.delete(self._path)
    return self


  

import urllib

from .. import api_utils

class Data(object):

  def __init__(self, key=None, group=None, value=None, **kwargs):
    self.key = key
    self.group = group
    self.value = value

  def save(self):
    key = urllib.quote_plus(self.key)
    group = urllib.quote_plus(self.group)
    api_utils.put("/api/data/{0}/{1}".format(group, key), payload=self.value)
    return self

  def delete(self):
    key = urllib.quote_plus(self.key)
    group = urllib.quote_plus(self.group)
    api_utils.delete("/api/data/{0}/{1}".format(group, key))
    return self


  

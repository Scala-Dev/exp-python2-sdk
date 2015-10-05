from .. import api_utils

class Data(object):

  def __init__(self, key=None, group=None, value=None, **kwargs):
    self.key = key
    self.group = group
    self.value = value

  def save(self):
    api_utils.put("/api/data/{0}/{1}".format(self.group, self.key), payload=self.value)
    return self

  def delete(self):
    api_utils.delete("/api/data/{0}/{1}".format(self.group, self.key))
    return self


  

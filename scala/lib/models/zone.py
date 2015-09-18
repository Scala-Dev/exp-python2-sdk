from scala.lib import api_utils

class Zone(object):

  def __init__(self, document, _new=True):
    self.document = document
    self._new = _new

  def save(self):
    if self._new:
      self.document = api_utils.post("/api/zones", payload=self.document)
      self._new = False
    else:
      self.document = api_utils.patch("/api/zones/" + self.document["uuid"], payload=self.document)
    return self

  def delete(self):
    api_utils.delete("/api/zones/" + self.document["uuid"])
    return self


  

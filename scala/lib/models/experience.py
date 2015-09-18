from scala.lib import api_utils

class Experience(object):

  def __init__(self, document, _new=True):
    self.document = document
    self._new = _new

  def save(self):
    if self._new:
      self.experience = api_utils.post("/api/experiences", payload=self.document)
      self._new = False
    else:
      self.document = api_utils.patch("/api/experiences/" + self.document["uuid"], payload=self.document)
    return self

  def delete(self):
    api_utils.delete("/api/experiences/" + self.document["uuid"])
    return self

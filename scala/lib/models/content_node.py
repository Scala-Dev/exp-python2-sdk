from scala.lib import api_utils

class ContentNode(object):

  def __init__(self, document):
    self.document = document

  def get_url(self):
    return api_utils.generate_url("/api/delivery" + self.document.get("path"))

  def get_children(self):
    if self.document.get("itemCount", 0) != len(self.document.get("children", [])):
      self.document = api_utils.get('/api/content/' + self.document.get("uuid") + '/children')
    return [ContentNode(x) for x in self.document.get("children")]

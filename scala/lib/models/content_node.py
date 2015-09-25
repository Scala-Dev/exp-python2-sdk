from scala.lib import api_utils

class ContentNode(object):

  def __init__(self, document, _isChildrenPopulated=False):
    self.document = document
    self._isChildrenPopulated = _isChildrenPopulated

  def get_url(self):
    return api_utils.generate_url("/api/delivery" + self.document.get("path"))

  def get_children(self):
    if not self._isChildrenPopulated:
      self.document = api_utils.get('/api/content/' + self.document.get("uuid") + '/children')
      self._isChildrenPopulated = True
    return [ContentNode(x) for x in self.document.get("children")]
      


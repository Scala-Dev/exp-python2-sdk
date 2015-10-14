import urllib

from .. import api_utils

class ContentNode(object):

  def __init__(self, document, _isChildrenPopulated=False):
    self.document = document
    self._isChildrenPopulated = _isChildrenPopulated

  def get_url(self):
    subtype = self.document['subtype']
    if subtype == 'scala:content:file':
      path = urllib.quote_plus(self.document['path'])
      return api_utils.generate_url('/api/delivery' + path)
    elif subtype == 'scala:content:app':
      path = urllib.quote_plus(self.document['path'] + '/index.html')
      return api_utils.generate_url('/api/devliery' + path)
    elif subtype == 'scala:content:url':
      return self.document['url']
    raise Exception('Cannot get url for this subtype.')

  def get_variant_url(self, variant_name):
    subtype = self.document['subtype']
    path = self.document['path']
    variants = self.document.get('variants', {}).get(name, None)
    if not variants:
      raise Exception('Content has no variants.')
    if subtype == 'scala:content:file':
      query = '?variant={0}'.format(urllib.quote(variant_name))
      return api_utils.generate_url('/api/delivery' + path) + query
    raise Exception('Variant not found.')

  def get_children(self):
    if not self._isChildrenPopulated:
      self.document = api_utils.get('/api/content/' + self.document.get("uuid") + '/children')
      self._isChildrenPopulated = True
    return [ContentNode(x) for x in self.document.get("children")]
      


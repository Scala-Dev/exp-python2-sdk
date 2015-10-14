import urllib

from .. import api_utils

class Content(object):

  def __init__(self, document, _is_children_populated=False):
    self.document = document
    self._is_children_populated = _is_children_populated

  def get_url(self):
    subtype = self.document['subtype']
    if subtype == 'scala:content:file':
      path = urllib.quote_plus(self.document['path'])
      return api_utils.generate_url('/api/delivery' + path)
    elif subtype == 'scala:content:app':
      path = urllib.quote_plus(self.document['path'] + '/index.html')
      return api_utils.generate_url('/api/delivery' + path)
    elif subtype == 'scala:content:url':
      return self.document['url']
    raise NotImplementedError('Cannot get url for this subtype.')

  def get_variant_url(self, variant_name):
    subtype = self.document['subtype']
    path = self.document['path']
    variants = self.document.get('variants', {}).get(name, None)
    if not variants:
      raise NameError('Variant not found.')
    if subtype == 'scala:content:file':
      query = '?' + urllib.urlencode({ 'variant' : variant_name })
      return api_utils.generate_url('/api/delivery' + path) + query
    raise NameError('Variant not found.')

  def get_children(self):
    if not self._is_children_populated:
      path = '{0}{1}{2}'.format('/api/content/', self.document.get("uuid"), '/children')
      self.document = api_utils.get(path)
      self._is_children_populated = True
    return [ContentNode(x) for x in self.document.get("children")]
      


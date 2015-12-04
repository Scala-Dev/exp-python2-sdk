from .. import api_utils

class Feed(object):

  def __init__(self, document, _new=True):
    self.document = document
    self._new = _new

  def save(self):
    if self._new:
      self.document = api_utils.post('/api/connectors/feeds', payload=self.document)
      self._new = False
    else:
      self.document = api_utils.patch('/api/connectors/feeds' + self.document['uuid'], payload=self.document)
    return self

  def get_data (self):
    return api_utils.get('/api/connectors/feeds/' + self.document['uuid'] + '/data')


  def delete(self):
    api_utils.delete('/api/locations/' + self.document['uuid'])
    return self


  

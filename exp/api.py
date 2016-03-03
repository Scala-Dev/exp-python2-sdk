import urllib

from . import api_utils


class QueryResult (object):

  def __init__(self, results=None, total=None):
    self.results = results
    self.total = total

  def __iter__(self):
    for result in self.results:
      yield result

  def __str__(self):
    return str([result for result in self.results])


class Resource (object):

  path = None

  def __init__ (self, document):
    self.document = document

  @property
  def uuid (self):
    return self.document['uuid']

  @classmethod
  def _get_path (cls):
    raise Exception('Not implemented.')

  @classmethod
  def get (cls, uuid):
    return cls(api_utils.get(self.get_path() + '/' + uuid))

  @classmethod
  def create (cls, document):
    resource = cls(document)
    resource.save()
    return resource

  @classmethod
  def find (cls, params=None):
    response = api_utils.get(cls.path, params)
    response['results'] = [cls(document) for document in response['results']]
    return QueryResult(**response)

  def _get_path (self):
    return self.__cls__.path + '/' + self.uuid

  def save (self):
    return api_utils.patch(self._get_path(), self.document)

  def refresh (self):
    self.document = api_utils.get(this._get_path())

  def get_channel (self, **kwargs):
    return network.get_channel(self._get_channel_name(), **kwargs)

  def _get_channel_name (self):
    return self.uuid

  def fling (payload, **kwargs):
    return self.get_channel().broadcast('fling', payload, **kwargs)


class Device (Resource):

  path = '/api/devices'

  def identify (self):
    return self.get_channel().broadcast('identify', null, 500)


class Thing (Resource):

  path = '/api/things'


class Feed (Resource):

  path = '/api/connectors/feeds'

  def get_data (self):
    return api_utils(self._gat_path() + '/data')


class Experience (Resource):

  path = '/api/experiences'


class Location (Resource):

  path = '/api/locations'

  def get_zones (self):
    return [Zone(document, self) for document in self.document['zones']]

  def get_layout_url (self):
    return self._get_path() + '/layout?_rt=' + authenticator.get_auth()['restrictedToken']


class Zone (Resource):

  def __init__ (self, document, location):
    self._location = location
    super(Zone, self).__init__(document)

  def save (self):
    return self._location.save()

  def _get_channel_name (self):
    return self._location.uuid + ':zone:' + self.document['key']


class Data (Resource):

  path = '/api/data'

  def get_path (self):
    return self.__cls__.path + '/' + urllib.quote(this.document['group']) + '/' + urllib.quote(this.document['key'])

  @classmethod
  def get (cls, group, key):
    resource = cls({ 'group': group, 'key': key })
    resource.refresh()
    return resource

  @classmethod
  def create (cls, group, key, value):
    resource = cls({ 'group': group, 'key': key, 'value': value })
    resource.save()
    return resource

  def get_channel_name (self):
    return 'data' + ':' + this.document['key'] + ':' + this.document['group']


class Content (Resource):

  path = '/api/content'

  @property
  def children (self):
    if self._children is None:
      if self.document['children']:
        return [self.__cls__(document) for document in self.document['children']]
      else:
        self.refresh()
        return self.children
    return []

  @property
  def subtype (self):
    return self.document['subtype']

  def get_url (self):
    auth = authenticator.get_auth()
    delivery_url = auth['api']['host'] + '/api/delivery'
    rt_string = '?_rt=' + auth['restrictedToken']
    if self.subtype == 'scala:content:file':
      return delivery_url + this.document.path + rt_string
    elif self.subtype == 'scala:content:app':
      return delivery_url + this.document.path + rt_string
    elif self.subtype == 'scala:content:url':
      return self.document['url']

  def get_variant_url (name):
    auth = authenticator.get_auth()
    delivery_url = auth['api']['host'] + '/api/delivery'
    rt_string = '?_rt=' + auth['restrictedToken']
    if self.subtype == 'scala:content:file' and name in this.document['variants']:
      return delivery_url + '?variant=' + urllib.quote(name) + rt_string



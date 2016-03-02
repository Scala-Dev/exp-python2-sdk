import urllib

#from .. lib import api_utils
#from .. lib.models.device import Device
#from .. lib.models.location import Location
#from .. lib.models.experience import Experience
#from .. lib.models.content import Content
#from .. lib.models.data import Data
#from .. lib.models.thing import Thing
#from .. lib.models.feed import Feed

from . import api_utils



class Resource (object):

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
  def find (cls, params):
    response = api_utils.get(self._get_path(), params)
    query = [cls(document) for document in response['results']]
    query.total = response['total']
    return query

  def _get_path (self):
    return self.__cls__.get_path() + '/' + self.uuid

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


""" Content """

def get_content(uuid):
  return Content(
    api_utils.get("/api/content/" + uuid + "/children"),
    _is_children_populated=True)

def find_content(**params):
  query = api_utils.get('/api/content', params=params)
  empty = []
  return [Content(x, _is_children_populated=False) for x in query.get("results", empty)]


""" Devices """

def find_devices(**params):
  query = api_utils.get('/api/devices', params=params)
  empty = []
  return [Device(x, _new=False) for x in query.get("results", empty)]

def get_device(uuid):
  return Device(api_utils.get('/api/devices/' + uuid), _new=False)

def create_device(document):
  return Device(document).save()


""" Things """

def find_things(**params):
  query = api_utils.get('/api/things', params=params)
  empty = []
  return [Thing(x, _new=False) for x in query.get("results", empty)]

def get_thing(uuid):
  return Thing(api_utils.get('/api/things/' + uuid), _new=False)

def create_thing(document):
  return Thing(document).save()


""" Experiences """

def find_experiences(**params):
  query = api_utils.get('/api/experiences', params=params)
  empty = []
  return [Experience(x, _new=False) for x in query.get("results", empty)]

def get_experience(uuid):
  return Experience(api_utils.get('/api/experiences/' + uuid), _new=False)

def create_experience(document):
  return Experience(document).save()


""" Locations """

def find_locations(**params):
  query = api_utils.get('/api/locations', params=params)
  empty = []
  return [Location(x, _new=False) for x in query.get("results", empty)]

def get_location(uuid):
  return Location(api_utils.get('/api/locations/' + uuid), _new=False)

def create_location(document):
  return Location(document).save()


""" Data """

def get_data(key, group):
    key = urllib.quote(key, safe='')
    group = urllib.quote(group, safe='')
    return Data(**api_utils.get('/api/data/' + group + '/' + key))

def find_data(**params):
    query = api_utils.get('/api/data', params=params)
    return [Data(**x) for x in query.get('results', [])]

def create_data(**params):
    return Data(**params).save()
    

""" Feeds """

def find_feeds(**params):
  query = api_utils.get('/api/connectors/feeds', params=params)
  empty = []
  return [Feed(x, _new=False) for x in query.get("results", empty)]

def get_feed(uuid):
  return Feed(api_utils.get('/api/connectors/feeds/' + uuid), _new=False)

def create_feed(document):
  return Feed(document).save()

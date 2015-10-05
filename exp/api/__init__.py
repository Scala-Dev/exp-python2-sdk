from .. lib import api_utils
from .. lib.models.device import Device
from .. lib.models.location import Location
from .. lib.models.experience import Experience
from .. lib.models.content_node import ContentNode
from .. lib.models.data import Data


""" Content """

def get_content_node(uuid):
    return ContentNode(
        api_utils.get("/api/content/" + uuid + "/children"),
        _isChildrenPopulated=True)


""" Devices """

def get_devices(**params):
  query = api_utils.get('/api/devices', params=params)
  empty = []
  return [Device(x, _new=False) for x in query.get("results", empty)]

def get_device(uuid):
  return Device(api_utils.get('/api/devices/' + uuid), _new=False)

def create_device(document):
  return Device(document).save()


""" Experiences """

def get_experiences(**params):
  query = api_utils.get('/api/experiences', params=params)
  empty = []
  return [Experience(x, _new=False) for x in query.get("results", empty)]

def get_experience(uuid):
  return Experience(api_utils.get('/api/experiences/' + uuid), _new=False)

def create_experience(document):
  return Experience(document).save()


""" Locations """

def get_locations(**params):
  query = api_utils.get('/api/locations', params=params)
  empty = []
  return [Location(x, _new=False) for x in query.get("results", empty)]

def get_location(uuid):
  return Location(api_utils.get('/api/locations/' + uuid), _new=False)

def create_location(document):
  return Location(document).save()


""" Zones """

def get_zones(**params):
  query = api_utils.get('/api/zones', params=params)
  empty = []
  return [Zone(x, _new=False) for x in query.get("results", empty)]

def get_zone(uuid):
  return Zone(api_utils.get('/api/zones/' + uuid), _new=False)

def create_zone(document):
  return Zone(document).save()


""" Data """

def get_data(key, group):
    return Data(**api_utils.get('/api/data/' + group + '/' + key))

def find_data(**params):
    query = api_utils.get('/api/data', params=params)
    return [Data(**x) for x in query.get('results', [])]

def create_data(**params):
    return Data(**params).save()
    

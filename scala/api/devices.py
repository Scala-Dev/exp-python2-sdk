from scala.lib import api_utils
from scala.lib.models.device import Device

def search(**params):
  query = api_utils.get('/api/devices', params=params)
  empty = []
  return [Device(x, _new=False) for x in query.get("results", empty)]

def get(uuid):
  return Device(api_utils.get('/api/devices' + uuid), _new=False)

def create(document):
  return Device(document).save()




  

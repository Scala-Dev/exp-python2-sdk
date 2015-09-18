from scala.lib import api_utils
from scala.lib.models.location import Location

def search(**params):
  query = api_utils.get('/api/locations', params=params)
  empty = []
  return [Location(x, _new=False) for x in query.get("results", empty)]

def get(uuid):
  return Location(api_utils.get('/api/locations' + uuid), _new=False)

def create(document):
  return Location(document).save()

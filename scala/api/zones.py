from scala.lib import api_utils
from scala.lib.models.zone import Zone

def search(**params):
  query = api_utils.get('/api/zones', params=params)
  empty = []
  return [Zone(x, _new=False) for x in query.get("results", empty)]

def get(uuid):
  return Zone(api_utils.get('/api/zones' + uuid), _new=False)

def create(document):
  return Zone(document).save()

from scala.lib import api_utils
from scala.lib.models.experience import Experience

def search(**params):
  query = api_utils.get('/api/experiences', params=params)
  empty = []
  return [Experience(x, _new=False) for x in query.get("results", empty)]

def get(uuid):
  return Experience(api_utils.get('/api/experiences' + uuid), _new=False)

def create(document):
  return Experience(document).save()




  

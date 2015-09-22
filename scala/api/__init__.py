from scala.lib import api_utils
from scala.lib.models.device import Device
from scala.lib.models.location import Location
from scala.lib.models.experience import Experience


""" Devices """

def getDevices(**params):
  query = api_utils.get('/api/devices', params=params)
  empty = []
  return [Device(x, _new=False) for x in query.get("results", empty)]

def getDevice(uuid):
  return Device(api_utils.get('/api/devices' + uuid), _new=False)

def createDevice(document):
  return Device(document).save()


""" Experiences """

def getExperiences(**params):
  query = api_utils.get('/api/experiences', params=params)
  empty = []
  return [Experience(x, _new=False) for x in query.get("results", empty)]

def getExperience(uuid):
  return Experience(api_utils.get('/api/experiences' + uuid), _new=False)

def createExperience(document):
  return Experience(document).save()


""" Locations """

def getLocations(**params):
  query = api_utils.get('/api/locations', params=params)
  empty = []
  return [Location(x, _new=False) for x in query.get("results", empty)]

def getLocation(uuid):
  return Location(api_utils.get('/api/locations' + uuid), _new=False)

def createLocation(document):
  return Location(document).save()


""" Zones """

def getZones(**params):
  query = api_utils.get('/api/zones', params=params)
  empty = []
  return [Zone(x, _new=False) for x in query.get("results", empty)]

def getZone(uuid):
  return Zone(api_utils.get('/api/zones' + uuid), _new=False)

def createZone(document):
  return Zone(document).save()

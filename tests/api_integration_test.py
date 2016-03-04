import unittest
import exp
import os
from exp.network import network
from exp.runtime import runtime
import time

import random
import string

user_credentials = {}
user_credentials['username'] = os.environ['EXP_USERNAME']
user_credentials['password'] = os.environ['EXP_PASSWORD']
user_credentials['organization'] = os.environ['EXP_ORGANIZATION']
user_credentials['host'] = os.environ['EXP_HOST']
user_credentials['enable_network'] = False



device_credentials = {}
device_credentials['uuid'] = os.environ['EXP_DEVICE_UUID']
device_credentials['secret'] = os.environ['EXP_SECRET']
device_credentials['host'] = os.environ['EXP_HOST']
device_credentials['enable_network'] = False




class AutoReloader (object):

  def setUp (self):
    exp.start(**self.credentials)

  def tearDown (self):
    pass#time.sleep(1)



class UserAuthenticator (AutoReloader):

  credentials = device_credentials # Temp because stormpath is slow.


def random_word ():
  return ''.join(random.choice(string.lowercase) for i in range(20))



class Devices (object):


  def test_create (self):
    device = exp.create_device({ 'name': random_word() })
    device.delete()

  def test_get(self):
    device = exp.create_device({ 'name': random_word() })
    exp.get_device(device.document['uuid'])
    device.delete()

  def test_save (self):
    device = exp.create_device({ 'name': random_word() })
    device.save()
    device.delete()

  def test_identify (self):
    device = exp.create_device({ 'name': random_word() })
    device.identify()

  def test_find (self):
    devices = exp.find_devices()


class Experiences (object):

  def test_create (self):
    experience = exp.create_experience({ 'name': random_word() })
    experience.delete()

  def test_get(self):
    experience = exp.create_experience({ 'name': random_word() })
    exp.get_experience(experience.document['uuid'])
    experience.delete()

  def test_save (self):
    experience = exp.create_experience({ 'name': random_word() })
    experience.save()
    experience.delete()

  def test_find (self):
    experiences = exp.find_experiences()



class Feeds (object):

  @unittest.skip
  def test_create (self):
    feed = exp.create_feed({ 'name': random_word() })
    feed.delete()

  @unittest.skip
  def test_get(self):
    feed = exp.create_feed({ 'name': random_word() })
    exp.get_feed(feed.document['uuid'])
    feed.delete()

  @unittest.skip
  def test_save (self):
    feed = exp.create_feed({ 'name': random_word() })
    feed.save()
    feed.delete()

  def test_find (self):
    feeds = exp.find_feeds()



class Locations (object):

  def test_create (self):
    location = exp.create_location({ 'name': random_word() })
    location.delete()

  def test_get(self):
    location = exp.create_location({ 'name': random_word() })
    exp.get_location(location.document['uuid'])
    location.delete()

  def test_save (self):
    location = exp.create_location({ 'name': random_word() })
    location.save()
    location.delete()

  def test_find (self):
    locations = exp.find_locations()



class Things (object):

  @unittest.skip
  def test_create (self):
    thing = exp.create_thing({ 'name': random_word() })
    thing.delete()

  @unittest.skip
  def test_get(self):
    thing = exp.create_thing({ 'name': random_word() })
    exp.get_thing(thing.document['uuid'])
    thing.delete()

  @unittest.skip
  def test_save (self):
    thing = exp.create_thing({ 'name': random_word() })
    thing.save()
    thing.delete()

  def test_find (self):
    things = exp.find_things()



class Content (object):
  pass



class Data (object):
  pass



class Zones (object):
  pass


class TestUserDevices (Devices, UserAuthenticator, AutoReloader): pass
class TestUserExperiences (Experiences, UserAuthenticator, AutoReloader): pass
class TestUserLocations (Locations, UserAuthenticator, AutoReloader): pass
class TestUserFeeds (Feeds, UserAuthenticator, AutoReloader): pass
class TestUserThings (Things, UserAuthenticator, AutoReloader): pass
class TestUserContent (Content, UserAuthenticator, AutoReloader): pass
class TestUserData (Data, UserAuthenticator, AutoReloader): pass
class TestUserZones (Zones, UserAuthenticator, AutoReloader): pass
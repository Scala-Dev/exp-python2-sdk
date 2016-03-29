
import unittest

from . import utils

class Test(utils.Device, utils.ResourceBase):

  class_ = utils.api.Zone
  creatable = False
  findable = False


  def create (self, junk=None):
    return self.exp.create_location({ 'zones': [{ 'key': self.generate_name(), 'name': self.generate_name() }]}).get_zones()[0]



  def test_get_devices (self):
    zone = self.create_valid()
    device = self.exp.create_device({ 'location': { 'uuid': zone.get_location().uuid, 'zones': [{ 'key': zone.key }]}})
    devices = zone.get_devices()
    if device.uuid not in [x.uuid for x in devices]:
      raise Exception
    if len(devices) > 1:
      raise Exception


  def test_get_things (self):
    zone = self.create_valid()
    thing = self.exp.create_thing({ 'location': { 'uuid': zone.get_location().uuid, 'zones': [{ 'key': zone.key }]}, 'id': self.generate_name(), 'name': self.generate_name(), 'subtype': 'scala:thing:rfid'})
    things = zone.get_things()
    if thing.uuid not in [x.uuid for x in things]:
      raise Exception
    if len(things) > 1:
      raise Exception

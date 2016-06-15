
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

  def test_get_current (self):
    device = self.exp.get_current_device()
    device.document['location'] = {}
    device.document['location']['uuid'] = None
    device.save()
    if len(self.exp.get_current_zones()) != 0:
      raise Exception

    location = self.exp.create_location({ 'zones': [{ 'key': 'a1' }, { 'key': 'b1' }] })

    device.document['location'] = {}
    device.document['location']['uuid'] = location.uuid
    device.document['location']['zones'] = [{ 'key': 'a1' }]
    device.save()

    zones = self.exp.get_current_zones()
    if zones[0].key != 'a1':
      raise Exception
    
    exp = self.exp_sdk.start(**self.consumer_credentials)
    if len(exp.get_current_zones()) != 0:
      raise Exception
    exp = self.exp_sdk.start(**self.user_credentials)
    if len(exp.get_current_zones()) != 0:
      raise Exception()
  

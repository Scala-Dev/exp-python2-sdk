
import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_location'
  find_name = 'find_locations'
  create_name = 'create_location'
  class_ = utils.api.Location

  def test_get_devices (self):
    location = self.create_valid()
    device = self.exp.create_device({ 'location': { 'uuid': location.uuid } })
    devices = location.get_devices()
    if devices.total < 1:
      raise Exception
    if device.uuid not in [x.uuid for x in devices]:
      raise Exception

  def test_get_things (self):
    location = self.create_valid()
    thing = self.exp.create_thing({ 'location': { 'uuid': location.uuid }, 'name': self.generate_name(), 'subtype': 'scala:thing:rfid', 'id': '123'})
    things = location.get_things()
    if things.total < 1:
      raise Exception
    if thing.uuid not in [x.uuid for x in things]:
      raise Exception

  def test_layout_url (self):
    location = self.create_valid()
    url = location.get_layout_url()
    if not url:
      raise Exception

  def test_get_current (self):
    device = self.exp.get_current_device()
    device.document['location'] = {}
    device.document['location']['uuid'] = None
    device.save()
    if self.exp.get_current_location():
      raise Exception
    location = self.create_valid()
    device.document['location'] = location.document
    device.save()
    location_new = self.exp.get_current_location()
    if location_new.uuid != location.uuid:
      raise Exception

    exp = self.exp_sdk.start(**self.consumer_credentials)
    if exp.get_current_location():
      raise Exception
    exp = self.exp_sdk.start(**self.user_credentials)
    if exp.get_current_location():
      raise Exception()

  def test_delete (self):
    location = self.create_valid()
    uuid = location.uuid
    location.delete()
    if self.exp.get_location(uuid):
      raise Exception
    location = self.create_valid()
    uuid = location.uuid
    self.exp.delete_location(uuid)
    if self.exp.get_location(uuid):
      raise Exception

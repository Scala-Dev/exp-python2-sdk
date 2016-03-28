
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
    if device.uuid not in [x.uuid for x in devices]:
      raise Exception

  def test_get_things (self):
    location = self.create_valid()
    thing = self.exp.create_thing({ 'location': { 'uuid': location.uuid }, 'name': self.generate_name(), 'subtype': 'scala:thing:rfid', 'id': '123'})
    things = location.get_things()
    if thing.uuid not in [x.uuid for x in things]:
      raise Exception

  def test_layout_url (self):
    location = self.create_valid()
    url = location.get_layout_url()
    if not url:
      raise Exception

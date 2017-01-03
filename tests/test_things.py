import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_thing'
  find_name = 'find_things'
  create_name = 'create_thing'
  class_ = utils.api.Thing

  def generate_valid_document (self):
    return { 'subtype': 'scala:thing:rfid', 'id': self.generate_name(), 'name': self.generate_name()}

  def test_get_location (self):
    thing = self.create_valid()
    location = self.exp.create_location()
    thing.document['location'] = {}
    thing.document['location']['uuid'] = location.uuid
    thing.save()
    location = thing.get_location()
    if not location:
      raise Exception

  def test_get_zones (self):
    location = self.exp.create_location({ 'zones': [{ 'key': 'key_1' }, { 'key': 'key_2' }]})
    document = self.generate_valid_document()
    document['location'] = { 'uuid': location.uuid, 'zones': [{ 'key': 'key_2'}] }
    thing = self.create(document)
    zones = thing.get_zones()
    if zones[0].key != 'key_2':
      raise Exception

  def test_delete (self):
    thing = self.create_valid()
    uuid = thing.uuid
    thing.delete()
    if self.exp.get_thing(uuid):
      raise Exception
    thing = self.create_valid()
    uuid = thing.uuid
    self.exp.delete_thing(uuid)
    if self.exp.get_thing(uuid):
      raise Exception

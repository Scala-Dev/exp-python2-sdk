
import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_device'
  find_name = 'find_devices'
  create_name = 'create_device'
  class_ = utils.api.Device

  def test_get_location (self):
    device = self.create_valid()
    location = self.exp.create_location()
    device.document['location'] = {}
    device.document['location']['uuid'] = location.uuid
    device.save()
    location = device.get_location()
    if not location:
      raise Exception

  def test_get_experience (self):
    device = self.create_valid()
    experience = self.exp.create_experience()
    device.document['experience'] = {}
    device.document['experience']['uuid'] = experience.uuid
    device.save()
    experience = device.get_experience()
    if not experience:
      raise Exception

  def test_get_zones (self):
    location = self.exp.create_location({ 'zones': [{ 'key': 'key_1' }, { 'key': 'key_2' }]})
    device = self.create({ 'location': { 'uuid': location.uuid, 'zones': [{ 'key': 'key_2'}] }})
    zones = device.get_zones()
    if zones[0].key != 'key_2':
      raise Exception

  def test_get_current (self):
    device = self.exp.get_current_device()
    if not device:
      raise Exception
    exp = self.exp_sdk.start(**self.consumer_credentials)
    if exp.get_current_device():
      raise Exception
    exp = self.exp_sdk.start(**self.user_credentials)
    if exp.get_current_device():
      raise Exception()
  
    

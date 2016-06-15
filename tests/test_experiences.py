
import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_experience'
  find_name = 'find_experiences'
  create_name = 'create_experience'
  class_ = utils.api.Experience

  def test_get_devices (self):
    experience = self.create_valid()
    device = self.exp.create_device({ 'experience': { 'uuid': experience.uuid } })
    devices = experience.get_devices()
    if device.uuid not in [x.uuid for x in devices]:
      raise Exception


  def test_get_current (self):
    device = self.exp.get_current_device()
    device.document['experience'] = {}
    device.document['experience']['uuid'] = None
    device.save()
    if self.exp.get_current_experience():
      raise Exception
    experience = self.create_valid()
    device.document['experience'] = experience.document
    device.save()
    experience_new = self.exp.get_current_experience()
    if experience_new.uuid != experience.uuid:
      raise Exception
    exp = self.exp_sdk.start(**self.consumer_credentials)
    if exp.get_current_experience():
      raise Exception
    exp = self.exp_sdk.start(**self.user_credentials)
    if exp.get_current_experience():
      raise Exception()
      

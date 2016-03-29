
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

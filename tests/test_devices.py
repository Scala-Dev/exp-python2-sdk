
import unittest

from . import utils

class Test(utils.Device, utils.ResourceBase):

  get_name = 'get_device'
  find_name = 'find_devices'
  create_name = 'create_device'
  class_ = utils.api.Device

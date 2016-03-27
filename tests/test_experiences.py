
import unittest

from . import utils

class Test(utils.Device, utils.ResourceBase):

  get_name = 'get_experience'
  find_name = 'find_experiences'
  create_name = 'create_experience'
  class_ = utils.api.Experience

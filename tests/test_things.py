
import unittest

from . import utils

class Test(utils.Device, utils.ResourceBase):

  get_name = 'get_thing'
  find_name = 'find_things'
  create_name = 'create_thing'
  class_ = utils.api.Thing

  def generate_valid_document (self):
    return { 'subtype': 'scala:thing:rfid', 'id': self.generate_name(), 'name': self.generate_name()}

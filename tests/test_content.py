
import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_content'
  find_name = 'find_content'
  creatable = False
  class_ = utils.api.Content

  def create(self, _=None):
    return self.exp.find_content()[0]


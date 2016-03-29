
import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_feed'
  find_name = 'find_feeds'
  create_name = 'create_feed'
  class_ = utils.api.Feed

  def generate_valid_document (self):
    return { 'subtype': 'scala:feed:weather', 'searchValue': '19713', 'name': self.generate_name() }

  def test_get_data (self):
    feed = self.create_valid()
    data = feed.get_data()
    if not isinstance(data, dict):
      raise Exception
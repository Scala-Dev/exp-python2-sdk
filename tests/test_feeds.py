
import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_feed'
  find_name = 'find_feeds'
  create_name = 'create_feed'
  class_ = utils.api.Feed

  def generate_valid_document (self):
    return { 'subtype': 'scala:feed:weather', 'dataType': 'static', 'searchValue': '19713', 'name': self.generate_name() }

  def test_get_data (self):
    feed = self.create_valid()
    data = feed.get_data()
    if not isinstance(data, dict):
      raise Exception

  def test_dynamic (self):
    feed = self.exp.create_feed({ 'subtype': 'scala:feed:weather', 'searchValue': '', 'dataType': 'dynamic', 'name': self.generate_name() })
    data = feed.get_data(searchValue='19713')
    if data['search']['search'] != '19713':
      raise Exception

  def test_delete (self):
    feed = self.create_valid()
    uuid = feed.uuid
    feed.delete()
    if self.exp.get_feed(uuid):
      raise Exception
    feed = self.create_valid()
    uuid = feed.uuid
    self.exp.delete_feed(uuid)
    if self.exp.get_feed(uuid):
      raise Exception


import unittest

from . import utils

class Test(utils.Device, utils.CommonResourceBase):

  get_name = 'get_content'
  find_name = 'find_content'
  creatable = False
  savable = False
  class_ = utils.api.Content

  def create(self, _=None):
    return self.exp.find_content()[0]

  def create_valid (self):
    return self.create()

  def test_subtype (self):
    items = self.exp.find_content()
    for item in items:
      if not item.subtype:
        raise Exception

  def test_get_url_url (self):
    items = [item for item in self.exp.find_content() if item.subtype == 'scala:content:url']
    if not items:
      raise Exception('No url content items found for testing.')
    if not items[0].get_url():
      raise Exception

  def test_has_variant (self):
    items = self.exp.find_content()
    for item in items:
      variants = item.document.get('variants', [])
      if variants:
        for variant in variants:
          if not item.has_variant(variant['name']):
            raise Exception
      if item.has_variant('not a variant'):
        raise Exception

  def test_get_url_file (self):
    items = [item for item in self.exp.find_content() if item.subtype == 'scala:content:file']
    if not items:
      raise Exception('No url content items found for testing.')
    if not items[0].get_url():
      raise Exception


  def test_get_url_app (self):
    items = [item for item in self.exp.find_content() if item.subtype == 'scala:content:app']
    if not items:
      raise Exception('No url content items found for testing.')
    if not items[0].get_url():
      raise Exception

  def test_get_variant_url (self):
    items = self.exp.find_content()
    for item in items:
      if not item.get_variant_url('test_variant'):
        raise Exception


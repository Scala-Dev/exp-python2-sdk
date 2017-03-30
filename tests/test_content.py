
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
    items = self.exp.find_content({ 'subtype': 'scala:content:url' })
    for item in items:
      if item.subtype != 'scala:content:url':
        raise Exception
    if not items or items.total == 0:
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
    items = self.exp.find_content({ 'subtype': 'scala:content:file' })
    for item in items:
      if item.subtype != 'scala:content:file':
        raise Exception
    if not items or items.total == 0:
      raise Exception('No file content items found for testing.')
    if not items[0].get_url():
      raise Exception

  def test_get_url_app (self):
    items = self.exp.find_content({ 'subtype': 'scala:content:app' })
    for item in items:
      if item.subtype != 'scala:content:app':
        raise Exception
    if not items or items.total == 0:
      raise Exception('No file content items found for testing.')
    if not items[0].get_url():
      raise Exception


  def test_get_variant_url (self):
    items = self.exp.find_content()
    print len(items)
    for item in items:
      if not item.get_variant_url('test_variant'):
        raise Exception


  def test_children (self):
    folders = self.exp.find_content({ 'subtype': 'scala:content:folder' })
    if folders.total == 0:
      raise Exception
    for folder in folders:
      children = folder.get_children({ 'subtype': 'scala:content:folder' })
      for child in children:
        if child.subtype != 'scala:content:folder':
          raise Exception
      if not children.total and children.total != 0:
        raise Exception

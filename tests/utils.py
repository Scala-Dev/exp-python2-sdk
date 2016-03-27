import exp as exp_sdk
import string
import random


from exp import api


class Base (object):

  exp_sdk = exp_sdk

  def setUp(self):
    self.device_credentials = { 'uuid': 'test-uuid', 'secret': 'test-secret', 'host': 'http://localhost:9000' }
    self.user_credentials = { 'username': 'test@goexp.io', 'password': 'test-Password1', 'organization': 'scala', 'host': 'http://localhost:9000' }
    self.consumer_credentials = { 'uuid': 'test-uuid', 'api_key': 'test-api-key', 'host': 'http://localhost:9000' }

  def tearDown (self):
    self.exp_sdk.stop()

  @staticmethod
  def generate_name():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))



class Device (Base):

  def setUp (self):
    super(Device, self).setUp()
    self.exp = exp_sdk.start(**self.device_credentials)


class User (Base):

  def setUp (self):
    super(User, self).setUp()
    self.exp = exp_sdk.start(**self.user_credentials)


class Consumer (Base):

  def setUp (self):
    super(Consumer, self).setUp()
    self.exp = exp_sdk.start(**self.consumer_credentials)






class ResourceBase (object):

  class_ = None
  get_name = ''
  create_name = ''
  find_name = ''


  def get (self, *args, **kwargs):
    return getattr(self.exp, self.get_name)(*args, **kwargs)

  def create (self, *args, **kwargs):
    return getattr(self.exp, self.create_name)(*args, **kwargs)

  def find (self, *args, **kwargs):
    return getattr(self.exp, self.find_name)(*args, **kwargs)

  def create_valid (self):
    return self.create(self.generate_valid_document())

  def generate_valid_document (self):
    return {}

  def assert_isinstance (self, resource):
    if not isinstance(resource, self.class_):
      raise Exception


  def test_get (self):
    resource_1 = self.create_valid()
    resource_2 = self.get(resource_1.uuid)
    self.assert_isinstance(resource_2)

  def test_get_with_invalid_uuid (self):
    if self.get('invalid uuid') is not None:
      raise Exception

  def test_get_none (self):
    if self.get(None) is not None:
      raise Exception

  def test_get_empty (self):
    if self.get() is not None:
      raise Exception


  def test_find_without_params (self):
    self.create_valid()
    [self.assert_isinstance(resource) for resource in self.find()]

  def test_find_with_params (self):
    resource = self.create_valid()
    resources = self.find({ 'name': resource.name })
    if not resources:
      raise Exception
    self.assert_isinstance(resources[0])

  def test_find_with_wrong_type (self):
    self.create(self.generate_valid_document())
    [self.assert_isinstance(resource) for resources in self.find('test')]


  def test_create_with_valid_document (self):
    self.assert_isinstance(self.create(self.generate_valid_document()))

  def test_create_empty (self):
    try:
      self.create()
    except self.exp_sdk.ApiError:
      pass

  def test_create_none (self):
    try:
      self.create()
    except self.exp_sdk.ApiError:
      pass

  def test_save (self):
    name = self.generate_name()
    resource_1 = self.create_valid()
    resource_1.name = name
    resource_1.save()
    resource_2 = self.get(resource_1.uuid)
    if resource_2.name != name:
      raise Exception


  def test_refresh (self):
    name = self.generate_name()
    resource_1 = self.create_valid()
    resource_2 = self.get(resource_1.uuid)
    resource_1.name = name
    resource_1.save()
    resource_2.refresh()
    if resource_2.name != name:
      raise Exception

  def test_uuid_getter (self):
    resource = self.create_valid()
    if resource.uuid != resource.document['uuid']:
      raise Exception

  def test_name_getter_setter (self):
    name = self.generate_name()
    resource = self.create_valid()
    resource.name = name
    if resource.name != name:
      raise Exception
    if resource.document['name'] != name:
      raise Exception


  def test_document (self):
    resource = self.create_valid()
    if not isinstance(resource.document, dict):
      raise Exception
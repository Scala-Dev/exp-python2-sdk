import exp_sdk
import string
import random


from exp_sdk import api


class Base (object):

  exp_sdk = exp_sdk

  def setUp(self):
    self.device_credentials = { 'uuid': 'test-uuid', 'secret': 'test-secret', 'host': 'http://localhost:8081' }
    self.user_credentials = { 'username': 'test@test.com', 'password': '12345test', 'organization': 'scala', 'host': 'http://localhost:8081' }
    self.consumer_credentials = { 'uuid': 'test-uuid', 'api_key': 'test-api-key', 'host': 'http://localhost:8081' }

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
  create_name = ''
  find_name = ''
  findable = True
  savable = True
  creatable = True

  def create (self, document=None):
    return getattr(self.exp, self.create_name)(document)

  def find (self, params=None):
    return getattr(self.exp, self.find_name)(params)

  def create_valid (self):
    return self.create(self.generate_valid_document())

  def generate_valid_document (self):
    return {}

  def assert_isinstance (self, resource):
    if not isinstance(resource, self.class_):
      raise Exception

  def test_create (self):
    if self.creatable:
      self.assert_isinstance(self.create_valid())
      try:
        self.create()
      except self.exp_sdk.ApiError:
        pass
      try:
        self.create({})
      except self.exp_sdk.ApiError:
        pass

  def test_document (self):
    resource = self.create_valid()
    if not isinstance(resource.document, dict):
      raise Exception

  def test_find (self):
    if not self.findable:
      return
    self.create_valid()
    collection = self.find()
    [self.assert_isinstance(resource) for resource in collection]
    if not collection.total:
      raise Exception
    resources = self.find({ 'name': resource.name })
    if not resources.results[0] == resources[0].document:
      raise Exception
    if not resources.total and resources.total != 0:
      raise Exception
    if not resources:
      raise Exception
    self.assert_isinstance(resources[0])

  def test_save (self):
    if self.savable:
      self.create_valid().save()

  def test_refresh (self):
    self.create_valid().refresh()

  def test_get_channel (self):
    resource = self.create_valid()
    channel = resource.get_channel(consumer=False, system=True)
    if not channel.broadcast:  # Duck typed.
      raise Exception


class CommonResourceBase (ResourceBase):

  get_name = ''

  def get (self, uuid=None):
    return getattr(self.exp, self.get_name)(uuid)

  def test_get (self):
    resource_1 = self.create_valid()
    resource_2 = self.get(resource_1.uuid)
    self.assert_isinstance(resource_2)
    if self.get('invalid uuid') is not None:
      raise Exception
    if self.get() is not None:
      raise Exception
    if getattr(self.exp, self.get_name)() is not None:
      raise Exception

  def test_save (self):
    if self.savable:
      name = self.generate_name()
      resource_1 = self.create_valid()
      resource_1.name = name
      resource_1.save()
      resource_2 = self.get(resource_1.uuid)
      if resource_2.name != name:
        raise Exception
    super(CommonResourceBase, self).test_save()

  def test_refresh (self):
    if self.savable:
      name = self.generate_name()
      resource_1 = self.create_valid()
      resource_2 = self.get(resource_1.uuid)
      resource_1.name = name
      resource_1.save()
      resource_2.refresh()
      if resource_2.name != name:
        raise Exception
    super(CommonResourceBase, self).test_refresh()

  def test_uuid (self):
    resource = self.create_valid()
    if not resource.uuid or resource.uuid != resource.document['uuid']:
      raise Exception

  def test_name (self):
    name = self.generate_name()
    resource = self.create_valid()
    if resource.document['name'] != resource.name:
      raise Exception
    resource.name = name
    if resource.name != name:
      raise Exception
    if resource.document['name'] != name:
      raise Exception


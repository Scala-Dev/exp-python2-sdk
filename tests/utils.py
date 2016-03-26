import exp as exp_sdk
import string
import random


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


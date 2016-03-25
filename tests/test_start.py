import unittest
import requests
import time

from . import utils

from exp import exceptions

class StartFailBase (object):

  def test_start (self):
    try:
      self.exp_sdk.start(**self.credentials)
    except self.exp_sdk.RuntimeError:
      pass
    else:
      raise Exception

class StartSuccessBase (object):

  def test_start (self):
    self.exp_sdk.start(**self.credentials)


class DeviceStartBase (utils.Base):

  def setUp (self):
    super(DeviceStartBase, self).setUp()
    self.credentials = self.device_credentials

class UserStartBase (utils.Base):

  def setUp(self):
    super(UserStartBase, self).setUp()
    self.credentials = self.user_credentials

class ConsumerStartBase (utils.Base):

  def setUp(self):
    super(ConsumerStartBase, self).setUp()
    self.credentials = self.consumer_credentials


class TestNoDeviceUuid (StartFailBase, DeviceStartBase, unittest.TestCase):

  def setUp(self):
    super(TestNoDeviceUuid, self).setUp()
    self.credentials['uuid'] = None



class TestNoDeviceSecret (StartFailBase, DeviceStartBase, unittest.TestCase):

  def setUp(self):
    super(TestNoDeviceSecret, self).setUp()
    self.credentials['secret'] = None



class TestAllowPairing (StartSuccessBase, DeviceStartBase, unittest.TestCase):

  def setUp(self):
    super(TestAllowPairing, self).setUp()
    self.credentials['uuid'] = None
    self.credentials['allow_pairing'] = True
    self.credentials['secret'] = None


class TestNoUsername (StartFailBase, UserStartBase, unittest.TestCase):

  def setUp(self):
    super(TestNoUsername, self).setUp()
    self.credentials['username'] = None


class TestNoPassword (StartFailBase, UserStartBase, unittest.TestCase):

  def setUp(self):
    super(TestNoPassword, self).setUp()
    self.credentials['password'] = None


class TestNoOrganization (StartFailBase, UserStartBase, unittest.TestCase):

  def setUp(self):
    super(TestNoOrganization, self).setUp()
    self.credentials['username'] = None


class TestNoConsumerUuid (StartFailBase, ConsumerStartBase, unittest.TestCase):

  def setUp(self):
    super(TestNoConsumerUuid, self).setUp()
    self.credentials['uuid'] = None


class TestNoConsumerApiKey (StartFailBase, ConsumerStartBase, unittest.TestCase):

  def setUp(self):
    super(TestNoConsumerApiKey, self).setUp()
    self.credentials['api_key'] = None
import unittest
import exp
from exp.network import network
from exp.runtime import runtime
from exp.authenticator import authenticator

def noop(*args, **kwargs):
  pass

original_network_configure = network.configure
original_authenticator_configure = authenticator.configure
original_authenticator_get_auth = authenticator.get_auth

class Base(object):

  type_ = None

  username = None
  password = None
  organization = None

  uuid = None
  secret = None
  api_key = None

  allow_pairing = None
  enable_network = True

  def setUp (self):
    runtime.is_started = False
    self.stub()

  def tearDown (self):
    runtime.is_started = False
    self.unstub()

  def stub (self):
    network.configure = noop
    authenticator.configure = noop
    authenticator.get_auth = noop

  def unstub (self):
    network.configure = original_network_configure
    authenticator.configure = original_authenticator_configure
    authenticator.get_auth = original_authenticator_get_auth

  def start (self):
    return exp.start(type=self.type_,
      username=self.username, password=self.password, organization=self.organization,
      uuid=self.uuid, secret=self.secret, api_key=self.api_key,
      allow_pairing=self.allow_pairing, enable_network=self.enable_network)


class ErrorBase(Base):

  exception = exp.RuntimeError

  def test (self):
    self.assertRaises(self.exception, lambda: self.start())


class NoOptions (ErrorBase, unittest.TestCase):
  pass


class NoUsername (ErrorBase, unittest.TestCase):
  password = '_'
  organization = '_'


class NoPassword (ErrorBase, unittest.TestCase):
  username = '_'
  organization = '_'


class NoOrganization (ErrorBase, unittest.TestCase):
  username = '_'
  password = '_'


class NoDeviceUuid (ErrorBase, unittest.TestCase):
  secret = '_'


class NoConsumerAppUuid (ErrorBase, unittest.TestCase):
  api_key = '_'


class NoDeviceSecret (ErrorBase, unittest.TestCase):
  type_ = 'device'
  uuid = '_'

class NoConsumerAppApiKey (ErrorBase, unittest.TestCase):
  type_ = 'consumer_app'
  uuid = '_'

class NoSecretOrApiKey (ErrorBase, unittest.TestCase):
  uuid = '_'


class SuccessBase (Base):

  def test (self):
    self.start()


class UserCredentials (SuccessBase, unittest.TestCase):
  username = '_'
  password = '_'
  organization = '_'

class UserTypedCredentials (SuccessBase, unittest.TestCase):
  type_ = 'user'
  username = '_'
  password = '_'
  organization = '_'

class DeviceCredentials (SuccessBase, unittest.TestCase):
  uuid = '_'
  secret = '_'

class DeviceTypedCredentials (SuccessBase, unittest.TestCase):
  type_ = 'device'
  uuid = '_'
  secret = '_'

class PairingCredentials (SuccessBase, unittest.TestCase):
  allow_pairing = True

class ConsumerAppCredentials (SuccessBase, unittest.TestCase):
  uuid = '_'
  api_key = '_'

class ConsumerAppTypedCredentials (SuccessBase, unittest.TestCase):
  type_ = 'consumer_app'
  uuid = '_'
  api_key = '_'



if __name__ == '__main__':
  unittest.main()

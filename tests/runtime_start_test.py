

import unittest
import exp

class TestException (Exception):
  pass


def fail_stub():
  raise TestException()

def noop(*args, **kwargs):
  pass

original_network_start = exp._network.start
original_network_wait = exp._network.wait
original_authenticator_start = exp._authenticator.start
original_authenticator_wait = exp._authenticator.wait



class Base(object):

  type_ = None

  username = None
  password = None
  organization = None

  uuid = None
  secret = None
  api_key = None

  allow_pairing = None
  enable_events = True

  did_network_wait = False
  did_authenticator_wait = False

  def on_network_wait (self):
    self.did_network_wait = True

  def on_authenticator_wait(self):
    self.did_authenticator_wait = True

  def setUp (self):
    self.stub()

  def tearDown (self):
    exp._runtime._is_started = False
    self.unstub()

  def stub (self):
    exp._network.start = noop
    exp._network.wait = lambda: self.on_network_wait()
    exp._authenticator.start = noop
    exp._authenticator.wait = lambda: self.on_authenticator_wait()

  def unstub (self):
    exp._network.start = original_network_start
    exp._network.wait = original_network_wait
    exp._authenticator.start = original_authenticator_start
    exp._authenticator.wait = original_authenticator_wait

  def start (self):
    return exp.start(type=self.type_,
      username=self.username, password=self.password, organization=self.organization,
      uuid=self.uuid, secret=self.secret, api_key=self.api_key,
      allow_pairing=self.allow_pairing, enable_events=self.enable_events)


class ErrorBase(Base):

  exception = Exception

  def test (self):
    self.assertRaises(self.exception, lambda: self.start())


class RuntimeErrorBase(ErrorBase):

  exception = exp.RuntimeError


class OptionsErrorBase(ErrorBase):

  exception = exp.OptionsError


class StartTwice (RuntimeErrorBase, unittest.TestCase):

  username = '_'
  password = '_'
  organization = '_'

  def test (self):
    try:
      self.start()
    except:
      pass
    super(StartTwice, self).test()


class NoOptions (OptionsErrorBase, unittest.TestCase):
  pass


class NoUsername (OptionsErrorBase, unittest.TestCase):
  password = '_'
  organization = '_'


class NoPassword (OptionsErrorBase, unittest.TestCase):
  username = '_'
  organization = '_'


class NoOrganization (OptionsErrorBase, unittest.TestCase):
  username = '_'
  password = '_'


class NoDeviceUuid (OptionsErrorBase, unittest.TestCase):
  secret = '_'


class NoConsumerAppUuid (OptionsErrorBase, unittest.TestCase):
  api_key = '_'


class NoDeviceSecret (OptionsErrorBase, unittest.TestCase):
  type_ = 'device'
  uuid = '_'

class NoConsumerAppApiKey (OptionsErrorBase, unittest.TestCase):
  type_ = 'consumer_app'
  uuid = '_'

class NoSecretOrApiKey (OptionsErrorBase, unittest.TestCase):
  uuid = '_'


class SuccessBase (Base):

  should_network_start = True

  def test (self):
    self.start()
    self.assertEquals(self.did_authenticator_wait, True)
    self.assertEquals(self.did_network_wait, self.should_network_start)

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

"""

class RuntimeExceptionsTestCase(BaseTestCase):

  def setUp (self):
    exp._network.start = noop
    exp._network.wait = noop
    exp._authenticator.start = noop
    exp._authenticator.wait = noop

  def tearDown (self):
    exp._runtime._is_started = False
    unstub()

  def test_start_with_no_options(self):
    self.assertRaises(exp.OptionsError, start_with_no_options)

  def test_double_start (self):
    self.assertRaises(exp.OptionsError, start_with_no_options)
    self.assertRaises(exp.RuntimeError, start_with_no_options)

  def test_start_with_no_username(self):
    self.assertRaises(exp.OptionsError, start_with_no_username)

  def test_start_with_no_password(self):
    self.assertRaises(exp.OptionsError, start_with_no_password)

  def test_start_with_no_organization(self):
    self.assertRaises(exp.OptionsError, start_with_no_password)

  def test_start_as_user (self):
    start_as_user()

  def test_starts_network (self):
    pass

  def test_starts_runtime (self):
    pass

class RuntimeSuccessTestCase(unittest.TestCase):

  def tearDown (self):
    exp._runtime._is_started = False


"""

if __name__ == '__main__':
  unittest.main()

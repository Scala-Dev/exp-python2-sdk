import unittest
import requests
import time

from . import utils

from exp import exceptions

class AuthBase (object):


  def test_authentication (self):
    self.exp.get_auth()

  def test_token_refresh (self):
    self.exp._sdk.authenticator._login()
    self.exp._sdk.authenticator._refresh()

  def test_refresh_401 (self):
    auth = self.exp.get_auth()
    auth['token'] = auth['token'] + 'blah'
    self.exp._sdk.options['uuid'] = 'blah'
    self.exp._sdk.options['username'] = 'blah'
    try:
      self.exp._sdk.authenticator._refresh()
    except self.exp_sdk.AuthenticationError:
      pass
    else:
      raise Exception



class TestDeviceAuth (AuthBase, utils.Device, unittest.TestCase): pass
class TestUserAuth (AuthBase, utils.User, unittest.TestCase): pass
class TestConsumerAuth (AuthBase, utils.Consumer, unittest.TestCase): pass


class TestDevice401 (utils.Base, unittest.TestCase):

  def test_login_401 (self):
    self.device_credentials['uuid'] = 'wrong uuid'
    try:
      exp = self.exp_sdk.start(**self.device_credentials)
    except self.exp_sdk.AuthenticationError:
      pass
    else:
      raise Exception


import unittest

import utils

class Test(utils.Base, unittest.TestCase):
  def test_stop_all (self):
    exp1 = self.exp_sdk.start(**self.consumer_credentials)
    exp2 = self.exp_sdk.start(**self.consumer_credentials)
    self.exp_sdk.stop()
    try:
      exp1.get_auth()
    except self.exp_sdk.RuntimeError:
      pass
    else:
      raise Error

  def test_stop (self):
    exp1 = self.exp_sdk.start(**self.consumer_credentials)
    exp2 = self.exp_sdk.start(**self.consumer_credentials)
    exp1.stop()
    try:
      exp1.get_auth()
    except self.exp_sdk.RuntimeError:
      pass
    else:
      raise Error
    exp2.get_auth()


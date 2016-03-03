import unittest
import exp
import os

class TestException (Exception):
  pass



user_credentials = {}
user_credentials['username'] = os.environ['EXP_USERNAME']
user_credentials['password'] = os.environ['EXP_PASSWORD']
user_credentials['organization'] = os.environ['EXP_ORGANIZATION']
user_credentials['host'] = os.environ['EXP_HOST']






class AutoReloader (object):

  def setUp (self):
    #exp.stop()
    reload(exp)
    exp.start(**self.credentials)

  def tearDown (self):
    exp.stop()


class UserAuthenticator (AutoReloader):

  credentials = user_credentials




class Broadcasting (object):
  pass

class Responding (object):
  pass

class Listening (object):
  pass


class Test1 (UserAuthenticator, unittest.TestCase):

  def test_something (self):
    pass
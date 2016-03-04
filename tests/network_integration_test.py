import unittest
import exp
import os
from exp.network import network
from exp.runtime import runtime
import time


user_credentials = {}
user_credentials['username'] = os.environ['EXP_USERNAME']
user_credentials['password'] = os.environ['EXP_PASSWORD']
user_credentials['organization'] = os.environ['EXP_ORGANIZATION']
user_credentials['host'] = os.environ['EXP_HOST']




class AutoReloader (object):

  def setUp (self):
    exp.start(**self.credentials)

  def tearDown (self):
    pass#time.sleep(1)



class UserAuthenticator (AutoReloader):

  credentials = user_credentials




class Broadcasting (object):

  def test_broadcasting(self):
    channel = exp.get_channel('test1')
    channel.broadcast('test2')
    channel.broadcast('test2', None)
    channel.broadcast('test2', payload=None)
    channel.broadcast('test2', timeout=1)

class Responding (object):
  pass

class Listening (object):

  def test_listening (self):
    channel = exp.get_channel('test3')
    listener = channel.listen('test4')
    channel.broadcast('test4')
    broadcast = listener.wait(3)
    if not broadcast:
      raise Exception()


class Cancelling (object):

  def test_listener_cancel (self):
    channel = exp.get_channel('test51')
    listener = channel.listen('test4')
    listener.cancel()
    channel.broadcast('test4')
    broadcast = listener.wait(1)
    if broadcast:
      raise Exception()




class TestUserBroadcasting (Broadcasting, UserAuthenticator, unittest.TestCase): pass
class TestUserListening (Listening, UserAuthenticator, unittest.TestCase): pass
class TestUserCancelling (Cancelling, UserAuthenticator, unittest.TestCase): pass




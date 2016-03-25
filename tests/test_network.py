import utils
import random
import string
import threading
import time

class Test1 (utils.Device):

  def test_simple_message_pattern (self):
    channel = self.exp.get_channel('test_channel')
    listener = channel.listen('test_message')
    channel.broadcast('test_message', { 'a': 1 })
    broadcast = listener.wait()
    if broadcast.payload['a'] != 1:
      raise


class Test2 (utils.Base):

  def test_responding (self):
    exp1 = self.exp_sdk.start(**self.consumer_credentials)
    exp2 = self.exp_sdk.start(**self.consumer_credentials)

    channel1 = exp1.get_channel('test_channel_2', consumer=True)
    channel2 = exp2.get_channel('test_channel_2', consumer=True)

    self.listener = channel1.listen('test_message_2')

    threading.Thread(target=lambda: self.responder()).start()
    time.sleep(.5)
    response = channel1.broadcast('test_message_2', { 'a': 1 })
    if response[0]['b'] != 2:
      raise Exception

  def responder (self):
    broadcast = self.listener.wait(60)
    if broadcast.payload['a'] == 1:
      broadcast.respond({ 'b': 2 })


  def test_listener_cancelling (self):
    pass  # TODO
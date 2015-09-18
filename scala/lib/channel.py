import random
import time
import threading
from . import socket

class Timeout(Exception):
  pass

class Error(Exception):
  pass

class Channel(object):

  Timeout = Timeout
  Error = Error  

  def __init__(self, name):
    self._name = name
    self._listeners = []
    self._responses = {}
    self._lock = threading.Lock()
    socket.Socket.events.on('message', self._on_message)

  def _clean_responses(self):
    """ Clean up responses that have not been processed """
    self._lock.acquire()
    now = time.time()
    for id, response in self._responses.iteritems():
      if now - response["time"] > 10:
        responses.pop(id, None)
    self._lock.release()
    
  def _on_message(self, message):
    self._clean_responses()
    self._lock.acquire()
    if message["type"] == "response":
      message["time"] = time.time()
      self._responses[message["id"]] = message
    self._lock.release()
    
  def request(self, name=None, target=None, payload=None):
    message = {}
    message["type"] = "request"
    message["id"] = str(random.random())
    message["channel"] = self._name
    message["name"] = name
    message["payload"] = payload
    message["device"] = {} # This will be deprecated
    message["device"]["target"] = target
    socket.Socket.send(message)
    start = time.time()
    while time.time() - start < 10:
      self._lock.acquire()
      response = self._responses.get(message["id"], None)
      if response:
        self._responses.pop(message["id"], None)
        self._lock.release()
        if response.get('error', None):
          raise Error(response.get('error'))
        return response.get('payload', None)
      self._lock.release()
      time.sleep(.1)
    self._lock.acquire()
    self._responses.pop(message["id"], None)
    self._lock.release()
    raise self.Timeout()


  def broadcast(self, name=None, payload=None):
    socket.Socket.send({
      'type': 'broadcast',
      'channel': self._name,
      'name': name,
      'payload': payload
    })

  def listen(self, name=None, callback=None):
    if not self._listeners.get(name):
      self._listeners[name] = []
    self._listeners[name].append(callback)


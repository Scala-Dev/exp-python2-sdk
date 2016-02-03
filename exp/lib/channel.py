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
    self._listeners = {}
    self._responses = {}
    self._responders = {}
    self._lock = threading.Lock()
    socket.on('message', self._on_message)

  def _clean_responses(self):
    """ Clean up responses that have not been processed """
    self._lock.acquire()
    now = time.time()
    for id, response in self._responses.iteritems():
      if now - response["time"] > 10:
        self._responses.pop(id, None)
    self._lock.release()

  def _on_response(self, message):
    self._lock.acquire()
    message["time"] = time.time()
    self._responses[message["id"]] = message
    self._lock.release()

  def _on_broadcast(self, message):
    self._lock.acquire()
    callbacks = self._listeners.get(message["name"], None)
    if not callbacks:
      return self._lock.release()
    for callback in callbacks:
      try:
        callback(message['payload'])
      except:
        pass
    self._lock.release()

  def _on_request(self, message):
    self._lock.acquire()
    if not self._responders.get(message["name"]):
      return self._lock.release()
    callback = self._responders.get(message["name"])
    try:
      payload = callback(message['payload'])
    except:
      socket.send({
        "type": "response",
        "id": message["id"],
        "error": "An error occured"
      })
    else:
      socket.send({
        "type": "response",
        "id": message["id"],
        "payload": payload
      })
    self._lock.release()
    
  def _on_message(self, message):
    if message["type"] == "response":
      self._clean_responses()
      return self._on_response(message)
    if message["channel"] != self._name:
      return
    if message["type"] == "broadcast":
      self._on_broadcast(message)
    elif message["type"] == "request":
      self._on_request(message)
      
  def request(self, name=None, target=None, payload=None):
    message = {}
    message["type"] = "request"
    message["id"] = str(random.random())
    message["channel"] = self._name
    message["name"] = name
    message["payload"] = payload
    message["device"] = {} # This will be deprecated
    message["device"]["target"] = target
    socket.send(message)
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
    socket.send({
      'type': 'broadcast',
      'channel': self._name,
      'name': name,
      'payload': payload
    })

  def listen(self, name=None, callback=None):
    if not self._listeners.get(name):
      self._listeners[name] = []
    self._listeners[name].append(callback)

  def fling(self, uuid=None):
    return self.broadcast(name='fling', payload={'uuid': uuid})

  def respond(self, name=None, callback=None):
    self._responders[name] = callback

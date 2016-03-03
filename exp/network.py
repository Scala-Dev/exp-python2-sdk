import time
import threading
import uuid

from .logger import logger

import urlparse
from socketIO_client import SocketIO, BaseNamespace
import json
import base64

from . import api_utils



from .authenticator import authenticator
from .exceptions import NotAuthenticatedError

class Broadcast (object):

  def __init__(self, message):
    self._message = message
    self.time = int(time.time())

  @property
  def payload(self):
    return self._message.get('payload', None)

  def respond(self, payload):
    message = {}
    message['id'] = self._message['id']
    message['channel'] = self._message['channel']
    message['payload'] = payload
    return api_utils.post('/api/networks/current/responses', payload=message)


class Listener (object):

  def __init__(self, id, namespace, max_age=60):
    self._id = id
    self._namespace = namespace
    self._event = threading.Event()
    self._broadcasts = []
    self._max_age = max_age

  def receive (self, message):
    broadcast = Broadcast(message)
    now = int(time.time())
    self._broadcasts = [broadcast for broadcast in self._broadcasts if now - broadcast.time < self._max_age]
    self._broadcasts.append(broadcast)
    self._event.set()

  def wait (self, timeout=None):
    try:
      return self._broadcasts.pop(0)
    except IndexError:
      self._event.clear()
      self._event.wait(timeout)
    try:
      return self._broadcasts.pop(0)
    except IndexError:
      return None

  def cancel(self):
    self._namespace.cancel(self._id)


class Namespace (object):

  def __init__(self):
    self._listeners = {}

  def receive (self, message):
    for id, listener in self._listeners.iteritems():
      listener.receive(message)

  def cancel (self, id):
    del self._listeners[id]

  def listen (self, **kwargs):
    id = str(uuid.uuid4())
    self._listeners[id] = Listener(id, self, **kwargs)
    return self._listeners[id]

  @property
  def has_listeners(self):
    return bool(self._listeners)



class Channel (object):

  def __init__(self, id):
    self._id = id
    self._namespaces = {}
    self._subscription = threading.Event()

  def receive (self, message):
    if message.get('name') in self._namespaces:
      self._namespaces[message['name']].receive(message)

  def broadcast (self, name, payload, timeout=5):
    message = {}
    message['channel'] = self._id
    message['name'] = name
    message['payload'] = payload
    return api_utils.post('/api/networks/current/broadcasts', payload=message, params={ 'timeout': timeout })

  def listen (self, name, **kwargs):
    if not self._namespaces.get(name):
      self._namespaces[name] = Namespace()
    listener = self._namespaces[name].listen(**kwargs)
    if not self._subscription.is_set():
      network.subscribe(self._id)
      self._subscription.wait()
    return listener

  @property
  def has_listeners (self):
    return any([namespace.has_listeners for key, namespace in self._namespaces.iteritems()])



class Network (object):

  def __init__(self):
    self._options = None
    self._socket = None
    self._auth = None
    self._do_stop = False
    self._channels = {}
    self._parent_thread = threading.currentThread()

    network_thread = threading.Thread(target=lambda: self._main_event_loop())
    network_thread.start()

  def set_options (self, **options):
    self._options = options

  def get_channel(self, name, system=False, consumer=False):
    id = self._generate_channel_id(name, system, consumer)
    if not self._channels.get(id):
      self._channels[id] = Channel(id)
    return self._channels[id]

  def _generate_channel_id (self, name, system, consumer):
    organization = authenticator.get_auth()['identity']['organization']
    raw_id = [organization, name, 1 if system else 0, 1 if consumer else 0]
    json_id = json.dumps(raw_id, separators=(',', ':'))
    return base64.b64encode(json_id)

  def on_connect(self):
    ids = []
    for id, channel in self._channels.iteritems():
      if channel.has_listeners:
        ids.append(id)
    if ids and self.is_connected:
      self._socket.emit('subscribe', ids)

  def on_disconnect(self):
    for id, channel in self._channels.iteritems():
      channel._subscription.clear()

  def on_subscribed(self, ids):
    for id in ids:
      if not self._channels.get(id):
        self._channels[id] = Channel(id)
      self._channels[id]._subscription.set()

  def on_broadcast (self, message):
    if message.get('channel') in self._channels:
      self._channels[message['channel']].receive(message)

  def subscribe (self, id):
    if self.is_connected:
      self._socket.emit('subscribe', [id])


  def wait (self):
    while not self.is_connected:
      time.sleep(1)

  def _disconnect (self):
    if self._socket:
      self._socket.disconnect()
      self._socket = None

  @property
  def is_connected(self):
    return self._socket and self._socket.connected

  def _main_event_loop (self):
    while True:
      if not self._parent_thread.is_alive():
        self._disconnect()
        break;
      elif not self._options:
        time.sleep(1)
      elif not self._options.get('enable_events'):
        self._disconnect()
        time.sleep(1)

      try:
        auth = authenticator.get_auth()
      except NotAuthenticatedError:
        auth = None
        return
      if auth != self._auth:
        self._auth = auth
        if self._socket:
          self._socket.disconnect()
        parsed_host = urlparse.urlparse(self._auth.get('network', {}).get('host'))
        self._socket = SocketIO(parsed_host.hostname, parsed_host.port, params={ "token": self._auth.get('token') }, Namespace=SocketNamespace, hurry_interval_in_seconds=10)
      if self.is_connected:
        self._socket.wait(seconds=1)
      else:
        time.sleep(1)


class SocketNamespace(BaseNamespace):

  def on_broadcast(self, message):
    network.on_broadcast(message)

  def on_connect(self):
    network.on_connect()

  def on_disconnect(self):
    network.on_disconnect()

  def on_subscribed(self, ids):
    network.on_subscribed(ids)


network = Network()
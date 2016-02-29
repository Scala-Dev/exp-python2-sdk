import time
import threading
import uuid

from .authenticator import authenticator
from .exceptions import NotAuthenticatedError

class Broadcast (object):

  def __init__(self, message):
    self._message = message
    self._time = int(time.time())

  @property
  def time(self):
      return self._time

  @property
  def payload(self):
    return self._message.get('payload', None)

  def respond(self, payload):
    try:
      # TODO: Make API call to respond to message.
      pass
    except Exception as exception:
      # TODO: Warn about failure to send response.
      # TODO: Rethrow a network exception.
      pass



class Listener (object):

  def __init__(self, max_age=60):
    self._event = threading.Event()
    self._broadcasts = []
    self._max_age = max_age
    self._is_active = True

  def receive (self, broadcast):
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

  @property
  def is_active(self):
    return self._is_active

  def cancel(self):
    self._is_active = False


class Namespace (object):

  def __init__(self):
    self._listeners = {}

  def cancel (self, id):
    del self._listeners[id]

  def listen (self):
    id = str(uuid.uuid4())
    self._listeners[id] = Listener()
    return self._listeners[id]

  @property
  def has_active_listeners(self):
    return any([listener.is_active for id, listener in self._listeners.iteritems()])



class Channel (object):

  def __init__(self, id):
    self._id = id
    self._namespaces = {}
    self._subscription = threading.Event()

  def broadcast (self, name, payload):
    # Emit and return API response.
    pass

  def listen (self, name):
    if not self._namespaces.get(name):
      self._namespaces[name] = Namespace()
    listener = self._namespaces[name].listen()
    if not self._subscription.is_set():
      network.subscribe(self._id)
      self._subscription.wait()
    return listener

  @property
  def has_listeners (self):
    return all([namepsace.has_listeners for key, namepsace in self._namespaces.iteritems()])



import urlparse
from socketIO_client import SocketIO, BaseNamespace
import json
import base64


class Network (object):

  def __init__(self):
    self._time_since_sync = 0
    self._options = None
    self._socket = None
    self._auth = None
    self._do_stop = False
    self._channels = {}
    self._subscriptions = {}

  def get_channel(self, name, system=False, consumer=False):
    id = self._generate_channel_id(name, system, consumer)
    if not self._channels.get(id):
      self._channels[id] = Channel(id)
    return self._channels[id]

  def _generate_channel_id (self, name, system, consumer):
    organization = authenticator.get_auth().get('identity', {}).get('organization')
    raw_id = [name, organization, 1 if system else 0, 1 if consumer else 0]
    json_id = json.dumps(raw_id)
    return base64.b64encode(json_id)

  def on_disconnect(self):
    for id, channel in self._channels.iteritems():
      channel._subscription.clear()

  def on_connect(self):
    ids = [id for id, channel in self._channels.iteritems() if channel.has_listeners]
    if ids:
      self._socket.emit('subscribe', ids)

  def on_subscribed(self, ids):
    for id in ids:
      if not self._channels.get(id):
        self._channels[id] = Channel(id)
      self._channels[id]._subscription.set()

  def subscribe (self, id):
    if self._socket and self._socket.connected:
      print id
      self._socket.emit('subscribe', [id])

  @property
  def is_connected(self):
    return self._socket and self._socket.connected

  def start (self, **options):
    self._options = options
    self._main_event_loop()

  def wait (self):
    while not self.is_connected:
      time.sleep(1)

  def _main_event_loop (self):
    while not self._do_stop:
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

  def stop (self):
    self._do_stop = True    

network = Network()


class SocketNamespace(BaseNamespace):

  #def on_broadcast(self, message):
  #  network.on_broadcast(message)

  def on_connect(self):
    network.on_connect()

  #def on_disconnect(self):
  #  network.on_disconnect()

  def on_subscribed(self, ids):
    network.on_subscribed(ids)

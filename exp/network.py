import time
import threading
import uuid

from .logger import logger

import urlparse
from socketIO_client import SocketIO, BaseNamespace
import json
import base64

from . import api_utils

import traceback

from .authenticator import authenticator



class _Broadcast (object):

  _path = '/api/networks/current/response'

  def __init__(self, message):
    self._message = message
    self._time = int(time.time())

  @property
  def payload(self):
    return self._message['payload']

  def respond(self, payload):
    response = { 'id': self._message['id'], 'channel': self._message['channel'], 'payload': payload }
    return api_utils.post(self._path, response)


class _Listener (object):

  def __init__(self, namespace, max_age=60):
    self._namespace = namespace
    self._max_age = max_age
    self._event = threading.Event()
    self._broadcasts = []

  def _receive (self, message):
    broadcast = _Broadcast(message)
    now = int(time.time())
    self._broadcasts = [broadcast for broadcast in self._broadcasts if now - broadcast._time < self._max_age]
    self._broadcasts.append(broadcast)
    self._event.set()

  def wait (self, timeout=None):
    if not self._broadcasts:
      self._event.clear()
      self._event.wait(timeout)
    if self._broadcasts:
      return self._broadcasts.pop(0)

  def cancel(self):
    self._namespace.cancel_listener(self)


class _Namespace (object):

  def __init__(self):
    self._listeners = []

  def listen (self, **kwargs):
    listener = _Listener(self, **kwargs)
    self._listeners.append(listener)
    return listener

  def cancel_listener(self, listener):
    if listener in self._listeners:
      self._listeners.remove(listener)

  def receive (self, message):
    [listener._receive(message) for listener in self._listeners]

  @property
  def has_listeners (self):
    return bool(self._listeners)


class _Channel (object):

  def __init__ (self, id):
    self._id = id
    self._namespaces = {}
    self._subscription = threading.Event()

  def broadcast (self, name, payload=None, timeout=5):
    path = '/api/networks/current/broadcasts'
    message = {'channel': self._id, 'name': name, 'payload': payload}
    params = {'timeout': timeout}
    return api_utils.post(path, message, params)

  def listen (self, name, **kwargs):
    if not self._namespaces.get(name):
      self._namespaces[name] = _Namespace()
    listener = self._namespaces[name].listen(**kwargs)
    if not self._subscription.is_set():
      socket.emit('subscribe', [self._id])
    self._subscription.wait()
    return listener

  def _receive (self, message):
    if message['name'] in self._namespaces:
      self._namespaces[message['name']].receive(message)

  @property
  def _has_listeners (self):
    return any([namespace.has_listeners for name, namespace in self._namespaces.iteritems()])









class _Network (object):

  def __init__(self):
    self._channels = {}
    self._auth = None
    self._options = None
    self._parent = threading.currentThread()
    self._thread = None
    self._lock = threading.Lock()
    self._is_started = False

  def start (self):
    self._lock.aquire()
    if self._is_started:
      return
    self._is_started = True
    self._parent = threading.currentThread()
    self._thread = threading.Thread(target=lambda: self._main_event_loop())
    self._thread.start()
    self._lock.release()

  def configure (self, **options):
    self._lock.acquire()
    self._auth = None
    self._options = options
    self._lock.release()

  def get_channel(self, name, system=False, consumer=False):
    channel_id = self._generate_channel_id(name, system, consumer)
    return self.get_channel_by_id(channel_id)

  def get_channel_by_id (self, channel_id):
    if channel_id not in self._channels:
      self._channels[channel_id] = _Channel(channel_id)
    return self._channels[channel_id]

  @staticmethod
  def _generate_channel_id (name, system=False, consumer=False):
    organization = authenticator.get_auth()['identity']['organization']
    raw_id = [organization, name, 1 if system else 0, 1 if consumer else 0]
    json_id = json.dumps(raw_id, separators=(',', ':'))
    return base64.b64encode(json_id)

  """ Callbacks on socket events """

  def on_connect(self):
    ids = [id for id, channel in self._channels.iteritems() if channel._has_listeners]
    socket.emit('subscribe', ids)

  def on_disconnect(self):
    [channel._subscription.clear() for id, channel in self._channels.iteritems()]

  def on_subscribed(self, ids):
    [self.get_channel_by_id(id)._subscription.set() for id in ids]

  def on_broadcast (self, message):
    self.get_channel_by_id(message['channel'])._receive(message)


  def _main_event_loop (self):

    while True:

      self._lock.acquire()

      """ If network is not enabled or options aren't set, disconnect and wait. """
      if not self._options or not self._options['enable_network']:
        socket.disconnect()
        self._lock.release()
        time.sleep(1)
        continue

      """ If parent thread is dead, disconnect and break event loop. """
      if self._parent and not self._parent.is_alive():
        socket.disconnect()
        self._lock.release()
        break;

      """ Attempt to retrieve current auth. If auth has changed, reconnect. """
      try:
        auth = authenticator.get_auth()
        if auth != self._auth:
          self._auth = auth
          socket.connect(**self._auth)
      except Exception:
        socket.disconnect()
        self._lock.release()
        time.sleep(1)
        continue

      """ Listen for socket events. """
      try:
        socket.wait(1)
      except Exception:
        self._lock.release()
        time.sleep(1)
        continue
      else:
        self._lock.release()



class _Socket (object):

  def __init__(self):
    self._socket = None

  @property
  def is_connected (self):
    return self._socket and self._socket.connected

  def connect (self, **auth):
    self.disconnect()
    params = { 'token': auth['token'] }
    parsed_host = urlparse.urlparse(auth['network']['host'])
    self._socket = SocketIO(parsed_host.hostname,
      parsed_host.port,
      params=params,
      Namespace=_SocketHandler,
      hurry_interval_in_seconds=10)

  def disconnect (self):
    if self._socket:
      network.on_disconnect()
      try:
        self._socket.disconnect()
        self._socket = None
      except:
        pass
      network.on_disconnect()

  def wait (self, seconds):
    if self.is_connected:
      try:
        self._socket.wait(seconds=seconds)
      except Exception:
        logger.warning('Error in network thread.')
        logger.debug('Error in network thread: %s', traceback.format_exc())
        time.sleep(seconds)
    else:
      time.sleep(seconds)

  def emit (self, name, payload):
    if self.is_connected:
      self._socket.emit(name, payload)



class _SocketHandler(BaseNamespace):

  def on_broadcast(self, message):
    network.on_broadcast(message)

  def on_connect(self):
    network.on_connect()

  def on_disconnect(self):
    network.on_disconnect()

  def on_subscribed(self, ids):
    network.on_subscribed(ids)



socket = _Socket()
network = _Network()
import time
import threading
import uuid


import urlparse
from socketIO_client import SocketIO, BaseNamespace
import json
import base64

import traceback


class _Broadcast (object):

  def __init__(self, sdk, message):
    self._sdk = sdk
    self._message = message
    self.time = int(time.time())

  @property
  def payload(self):
    return self._message['payload']

  def respond(self, response):
    self._sdk.api.post('/api/networks/current/responses', {'id': self._message['id'], 'channel': self._message['channel'], 'payload': response })


class _Listener (object):

  def __init__(self, namespace, sdk, max_age=60, **kwargs):
    self._namespace = namespace
    self._sdk = sdk
    self._max_age = max_age
    self._event = threading.Event()
    self._broadcasts = []

  def _prune (self):
    now = int(time.time())
    self._broadcasts = [broadcast for broadcast in self._broadcasts if now - broadcast.time < self._max_age]

  def receive (self, message):
    self._prune()
    self._broadcasts.append(_Broadcast(self._sdk, message))
    self._event.set()

  def wait (self, timeout=0, **kwargs):
    self._prune()
    if not self._broadcasts:
      self._event.clear()
      self._event.wait(timeout)
    if self._broadcasts:
      broadcast = self._broadcasts.pop(0)
      return broadcast

  def cancel(self):
    self._namespace.cancel_listener(self)


class _Namespace (object):

  def __init__(self, sdk):
    self._listeners = []
    self._sdk = sdk

  def listen (self, **kwargs):
    listener = _Listener(self, self._sdk, **kwargs)
    self._listeners.append(listener)
    return listener

  def cancel_listener(self, listener):
    if listener in self._listeners:
      self._listeners.remove(listener)

  def receive (self, message):
    [listener.receive(message) for listener in self._listeners]

  @property
  def has_listeners (self):
    return bool(self._listeners)


class _Channel (object):

  def __init__ (self, id, sdk):
    self._id = id
    self._sdk = sdk
    self._namespaces = {}
    self.subscription = threading.Event()

  def broadcast (self, name, payload=None, timeout=0.1):
    path = '/api/networks/current/broadcasts'
    payload = {'channel': self._id, 'name': name, 'payload': payload}
    params = {'timeout': timeout * 1000 }
    return self._sdk.api.post(path, payload, params)

  def listen (self, name, **kwargs):
    if not self._namespaces.get(name):
      self._namespaces[name] = _Namespace(self._sdk)
    listener = self._namespaces[name].listen(**kwargs)
    if not self.subscription.is_set():
      self._sdk.network.emit('subscribe', [self._id])
    self.subscription.wait()
    return listener

  def receive (self, message):
    if message['name'] in self._namespaces:
      self._namespaces[message['name']].receive(message)

  @property
  def has_listeners (self):
    return any([namespace.has_listeners for name, namespace in self._namespaces.iteritems()])









class Network (object):

  def __init__(self, sdk):
    self._sdk = sdk
    self._channels = {}
    self._auth = None
    self._socket = None
    self._abort = False
    self._parent = threading.currentThread()
    self._thread = threading.Thread(target=lambda: self._main_event_loop())
    self._lock = threading.Lock()

  def start (self):
    self._thread.start()

  def stop (self):
    self._abort = True

  def get_channel(self, name, system=False, consumer=False):
    channel_id = self._generate_channel_id(name, system, consumer)
    channel = self._get_channel_by_id(channel_id)
    return channel

  def emit (self, name, payload):
    if not self._socket:
      return False
    return self._socket.emit(name, payload)

  def _get_channel_by_id (self, channel_id):
    if channel_id not in self._channels:
      self._channels[channel_id] = _Channel(channel_id, self._sdk)
    return self._channels[channel_id]

  def _generate_channel_id (self, name, system=False, consumer=False):
    organization = self._sdk.authenticator.get_auth()['identity']['organization']
    raw_id = [organization, name, 1 if system else 0, 1 if consumer else 0]
    json_id = json.dumps(raw_id, separators=(',', ':'))
    return base64.b64encode(json_id)

  def on_connect(self, socket):
    if socket != self._socket:
      return
    [channel.subscription.clear() for id, channel in self._channels.iteritems()]
    self._socket.emit('subscribe', [id for id, channel in self._channels.iteritems() if channel.has_listeners])

  def on_disconnect(self, socket):
    if socket != self._socket:
      return
    [channel.subscription.clear() for id, channel in self._channels.iteritems()]

  def on_subscribed(self, socket, ids):
    if socket != self._socket:
      return
    [self._get_channel_by_id(id).subscription.set() for id in ids]

  def on_broadcast (self, socket, message):
    if socket != self._socket:
      return
    self._get_channel_by_id(message['channel']).receive(message)


  def _main_event_loop (self):

    while True:

      """ If parent thread is dead or network is inactive, disconnect and break thread. """
      if not self._parent.is_alive() or self._abort:
        if self._socket:
          self._socket.stop()
          self._socket = None
        break

      """ Attempt to retrieve current auth. """
      try:
        auth = self._sdk.authenticator.get_auth()
      except Exception:
        self._auth = None
        time.sleep(1)
        continue

      """ Disconnect if auth has changed. """
      if auth != self._auth:
        self._auth = auth
        if self._socket:
          self._socket.stop()
          self._socket = None

      """ Do nothing if there is no auth. """
      if not self._auth:
        time.sleep(1)
        continue

      """ Start the socket if not started. """
      if not self._socket:
        try:
          self._socket = _Socket(self._sdk)
          self._socket.start(**self._auth)
        except:
          self._sdk.logger.warning('Socket failed to start.')
          self._sdk.logger.warning('Socket failed to start: %s', traceback.format_exc())
          self._socket = None
          time.sleep(1)
          continue

      """ Listen for socket events. """
      try:
        self._socket.wait(1)
      except:
        self._sdk.logger.warning('Socket failed to wait for messages.')
        self._sdk.logger.warning('Socket failed to wait for messages: %s', traceback.format_exc())
        time.sleep(1)





class _Socket (object):

  def __init__(self, sdk):
    self._sdk = sdk
    self._socket = None

  def start (self, **auth):


    class Namespace (BaseNamespace):

      def on_broadcast (self, message):
        self.socket._sdk.network.on_broadcast(self.socket, message)

      def on_connect (self):
        self.socket._sdk.network.on_connect(self.socket)

      def on_disconnect (self):
        self.socket._sdk.network.on_disconnect(self.socket)

      def on_subscribed (self, message):
        self.socket._sdk.network.on_subscribed(self.socket, message)

    Namespace.socket = self

    params = { 'token': auth['token'] }
    parsed_host = urlparse.urlparse(auth['network']['host'])
    self._socket = SocketIO(parsed_host.hostname, parsed_host.port, Namespace, params=params, hurry_interval_in_seconds=10)

  def stop (self):
    self._sdk.logger.debug('Disconnecting from network.')
    try:
      self._socket.disconnect()
      self._sdk.logger.debug('Disconnected from network')
    except:
      self._sdk.logger.warning('Failed to disconnect from network.')
      self._sdk.logger.debug('Failed to disconnect from network: %s', traceback.format_exc())

  def wait (self, seconds):
    if not self.is_connected:
      return time.sleep(seconds)
    try:
      self._socket.wait(seconds)
    except:
      self._sdk.logger.warning('Failed to wait for socket messages.')
      self._sdk.logger.debug('Failed to wait for socket messages: %s', traceback.format_exc())
      time.sleep(seconds)

  def emit (self, name, payload):
    if not self.is_connected:
      self._sdk.logger.debug('Failed to emit socket message: Device is offline.')
      return False
    try:
      self._sdk.logger.debug('Emitting socket message: %s,%s', name, payload)
      self._socket.emit(name, payload)
      return True
    except:
      self._sdk.logger.warning('Failed to emit socket message.')
      self._sdk.logger.debug('Failed to emit socket message: %s', traceback.format_exc())
      return False

  @property
  def is_connected (self):
    return self._socket and self._socket.connected

import time

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
    listener = Listener(id, self)
    self._listeners.append(listener)
    return listener

  @property
  def has_active_listeners(self):
    return any([listener.is_active for id, listener in self._listeners.iteritems()])



class Channel (object):

  def __init__(self, id):
    self._id = id
    self._namespaces = {}

  def broadcast (self, name, payload):
    # Emit and return API response.
    pass

  def listen (self, name):

    return self.get_channel(channel_id).listen(name)

  @property
  def has_listeners (self):
      return all([namepsace.has_listeners for key, namepsace in self._namespaces.iteritems()])


class Subscription (object):
  pass

class SocketHandler (object):
  pass


import urlparse
from socketIO_client import SocketIO, BaseNamespace

"""class SocketNamespace(BaseNamespace):

  def on_message(self, message):
    print 'BRO'

  def on_connect(self):
    print 'CON'

  def on_disconnect(self):
    print 'DIS'

  def on_subscribed(self, message):
    print 'SUB'

  def on_channels(self, message):
    print 'CHAN'"""

class Network (object):

  def __init__(self):
    self._options = None
    self._socket = None
    self._is_connected = False
    self._auth = None
    self._do_stop = False

  def start (self, **options):
    self._options = options
    self._main_event_loop()

  def wait (self):
    while not self._is_connected:
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
      if self._socket:
        self._socket.wait_for_callbacks(1)
      else:
        time.sleep(1)

  def stop (self):
    self._do_stop = True


  def _reconnect(self):
    



network = Network()

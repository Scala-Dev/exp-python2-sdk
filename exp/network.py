


class Listener (object):
  pass


class Channel (object):
  pass


class Subscription (object):
  pass


class Network (object):

  def __init__(self):
    self.channels = {}
    self.subscriptions = {}
    self.socket = None

  @property
  def isConnected (self):
    return self.socket not None


  def connect (self, auth):
    self.disconnect()
    self.auth = auth
    # Establish socket connection.

  def disconnect (self):
    if self.socket:
      self.socket.disconnect()
      self.socket = None

  def broadcast (self, message):
    pass

  def listen (self):
    pass

  def get_channel (self):
    pass


  def digest (self):
    if not self.socket:
      if self.auth:
        pass
    else:
      if self.outoing


    if self.auth and not self.socket:
      try:
        self.socket = None ## Create socket
      except Exception:
        return



    # Connect if auth has been updated
    # Disconnect if we are to terminate.
    # Send outgoing messages
    # Receive and route incoming messages to channels


network = Network()

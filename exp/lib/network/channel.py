
class Listener:

  def __init__(self, namespace):
    this._namespace = namespace
    this._messages = []

  def receive (message):
    pass

  def cancel (self):
    pass



class Namespace:

  def __init__(self, channel):
    this._listeners = []
    this._channel = channel

  def unlisten (self, listener):
    try:
      this._listeners.remove(listener)
    except ValueError:
      pass
    if not this._listeners:
      this._channel.unlisten(self)

  def listen (self):
    this._listeners.append(Listener())
    return this._listeners[-1]

  def receive (message):
    return [listener.receive(message) for listener in this._listeners]


class Channel:

  def __init__(self, id):
    this._id = id
    this._namespaces = {}

  def recieve (self, message):
    namespace = this._namespaces.get(message.get('name'))
    if not namespace: return
    return namespace.receive(message)

  def broadcast (self, **kwargs):
    kwargs['id'] = self._id
    return Network.broadcast(**kwargs)

  def listen (self, name):
    Network._subscribe(self._id)
    if not self._namespaces[name]:
      self._namespaces[name] = Namespace()
    return self._namespaces[name].listen()

  def _subscribe (self):
    return Network.subscribe(self._id)

  def _unsubscribe (self):
    return Network.unsubscribe(self._id)

  def _unlisten (self, namespace):
    self._namespaces.pop(namespace, None)
    if not bool(self._namespaces):
      self._unsubscribe()

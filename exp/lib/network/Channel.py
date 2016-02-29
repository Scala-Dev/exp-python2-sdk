
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

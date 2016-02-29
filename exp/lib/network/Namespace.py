
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


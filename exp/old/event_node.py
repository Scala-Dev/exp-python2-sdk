import threading
import inspect

class EventNode(object):

  def __init__(self):
    self.callbacks = {}

  def on(self, name, callback):
    if not self.callbacks.get(name):
      self.callbacks[name] = []
    self.callbacks[name].append(callback)

  def trigger(self, name, payload=None):
    if not self.callbacks.get(name): return
    for callback in self.callbacks.get(name):
      spec = inspect.getargspec(callback)
      if len(spec.args) == 0:
        thread = threading.Thread(target=callback)
      else:
        thread = threading.Thread(target=callback, args=[payload])
      thread.daemon = True
      thread.start()
    

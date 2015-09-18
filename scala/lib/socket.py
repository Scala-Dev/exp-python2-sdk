import Queue
import threading
import time
import logging
import random

from socketIO_client import SocketIO, BaseNamespace

from . import event_node


logging.getLogger('request').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

_events = event_node.EventNode()

_vars = {}
_vars["io"] = None
_vars["threadId"] = None

_outgoing = Queue.Queue()
_lock = threading.Lock()

on = _events.on

class _Namespace(BaseNamespace):

  def on_message(self, message):
    if type(message) != dict: return
    _events.trigger('message', message)

  def on_connect(self):
    _events.trigger('connected')

  def on_disconnect(self):
    _events.trigger('disconnected')
    

class Timeout(Exception):
  pass  


def _disconnect():
  _lock.acquire()
  if _vars["io"]:
    _vars["io"].disconnect()
    _vars["io"] = None
  _lock.release()

def _connect(host, port, token):
  _disconnect()
  _lock.acquire()
  start = time.time()
  while time.time() - start < 5:
    if not _vars["io"]:
      try:
        _vars["io"] = SocketIO(host, port, params={ "token": token }, Namespace=_Namespace)
      except:
        _vars["io"] = None
        time.sleep(1)
        continue
    if _vars["io"].connected:
      return _lock.release()
    time.sleep(.1)
  _lock.release()
  _disconnect()

def send(message):
  _outgoing.put(message)

def _process_incoming():
  if not _vars["io"]:
    return
  try:
    _vars["io"].wait(.1)
  except:
    time.sleep(1)

def _process_outgoing():
  try:
    message = _outgoing.get_nowait()
  except Queue.Empty:
    return
  if not _vars["io"]:
    return
  _vars["io"].emit('message', message)
    
def _loop():
  threadId = _vars["threadId"]
  _lock.release()
  while True:
    _lock.acquire()
    if threadId != _vars["threadId"]:
      _lock.release()
      return
    _process_incoming()
    _process_outgoing()
    _lock.release()
    time.sleep(.1)

def start(*args):
  _lock.acquire()
  _vars["threadId"] = random.random()
  threading.Thread(target=_loop).start()
  _connect(*args)

def stop():
  _lock.acquire()
  _threadId = None
  _lock.release()
  _disconnect()


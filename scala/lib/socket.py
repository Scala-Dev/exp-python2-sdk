import Queue
import threading
import time
import logging
import random

from socketIO_client import SocketIO, BaseNamespace

from . import event_node


logging.getLogger('request').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class Namespace(BaseNamespace):

  def on_message(self, message):
    if type(message) != dict: return
    Socket.events.trigger('message', message)

  def on_connect(self):
    Socket.events.trigger('connected')

  def on_disconnect(self):
    Socket.events.trigger('disconnected')
    

class Timeout(Exception):
  pass


class Socket(object):

  events = event_node.EventNode()

  isRunning = False
    
  _lock = threading.Lock()
  _io = None
  _outgoing = Queue.Queue()


  @classmethod
  def _disconnect(cls):
    cls._lock.acquire()
    if cls._io:
      cls._io.disconnect()
      cls._io = None
    cls._lock.release()

  @classmethod
  def _connect(cls, host='http://localhost', port=9000, token=None):
    cls._lock.acquire()
    if cls._io:
      cls._io.disconnect()
      cls._io = None
    start = time.time()
    while True:
      if time.time() - start > 5:
        if cls._io:
          cls._io.disconnect()
          cls._io = None
        cls._lock.release()        
        raise Timeout()
      if not cls._io:
        try:
          cls._io = SocketIO(host, port, Namespace=Namespace, wait_for_connection=False)
        except:
          cls._io = None
          time.sleep(1)
        continue
      if cls._io.connected:
        cls._lock.release()
        break
      time.sleep(.1)

  @classmethod
  def send(cls, message):
    cls._outgoing.put(message)

  @classmethod
  def _processIncoming(cls):
    if not cls._io:
      return
    try:
      cls._io.wait(.1)
    except:
      time.sleep(1)

  @classmethod
  def _processOutgoing(cls):
    try:
      message = cls._outgoing.get_nowait()
    except Queue.Empty:
      return
    if not cls._io:
      return
    cls._io.emit('message', message)
    
  @classmethod
  def _loop(cls):
    threadId = cls._threadId
    cls._lock.release()
    while True:
      cls._lock.acquire()
      if threadId != cls._threadId:
        cls._lock.release()
        return
      cls._processIncoming()
      cls._processOutgoing()
      cls._lock.release()
      time.sleep(.1)

  @classmethod
  def start(cls, **kwargs):
    cls._lock.acquire()
    cls._threadId = random.random()
    thread = threading.Thread(target=cls._loop)
    thread.start()
    cls._connect(**kwargs)

  @classmethod
  def stop(cls):
    cls._lock.acquire()
    cls._threadId = None
    cls._lock.release()
    cls._disconnect()


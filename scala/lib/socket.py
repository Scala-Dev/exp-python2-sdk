import Queue
import threading
import time
import logging
from socketIO_client import SocketIO, BaseNamespace
logging.getLogger('request').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class Socket(object):
  socketIO = None

  @classmethod
  def connect(cls, host='', port=9000):
    cls.socketIO = SocketIO('http://localhost', 9000)

  def disconnect():
    pass

incoming = Queue.Queue()
outgoing = Queue.Queue()
operations = Queue.Queue()

def loop():
  while True:
    processOperations()
    processOutgoing()
    processIncoming()

def processOperations():
  try:
    operation = operations.get_nowait()
  except Queue.Empty:
    return
  if operation['type'] == 'connect':
    Socket.socketIO = SocketIO('http://localhost', 9000)
  elif operation['type'] == 'disconnect':
    pass

def processOutgoing():
  try:
    message = outgoing.get_nowait()
  except Queue.Empty:
    return
  if not Socket.socketIO: return
  Socket.socketIO.emit('message', message)

def processIncoming():
  if not Socket.socketIO: return
  Socket.socketIO.wait(1)



def emit():
  print 'EMITTING'
  socketIO.emit('message', {
    'name': 'getCurrentExperience',
    'channel': 'system',
    'type': 'request',
    'id': '12312424'
  })
  socketIO = None
  time.sleep(1)
  emit()

def connect():
  print 'WAITING'
  socketIO.wait()

def start():
  thread = threading.Thread(target=loop)
  thread.start()


operations.put({'type': 'connect'})
outgoing.put({ 'type': 'request', 'name': 'getCurrentExperience', 'channel': 'system', 'id': '123'})
outgoing.put({ 'type': 'request', 'name': 'getCurrentExperience', 'channel': 'system', 'id': '123'})
outgoing.put({ 'type': 'request', 'name': 'getCurrentExperience', 'channel': 'system', 'id': '123'})
outgoing.put({ 'type': 'request', 'name': 'getCurrentExperience', 'channel': 'system', 'id': '123'})  

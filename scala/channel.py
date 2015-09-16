import threading
import Queue
import time
import logging
from socketIO_client import SocketIO, BaseNamespace
logging.getLogger('request').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


queue = Queue.Queue()

def loop():
  while True: digest()

def digest():
  connect()
  event = queue.get()
  if item: process(event)

def loop():
  while True: digest()

def connect():
  pass


def connect():
  print 'A'
  print 'B'
  socketIO = SocketIO('http://localhost', 9000)
  

  print 'C'



  #socketIO.on('message', p)

  print 'M'
  socketIO.emit('message', {
    'name': 'getCurrentExperience',
    'channel': 'system',
    'type': 'request',
    'id': '12312424'
  })
  print 'W'
  socketIO.wait(3)

def disconnect():
  pass

class SocketEvent(object):
  def __init__(obj):
    pass
  
def start():
  thread = threading.Thread(target=connect)
  thread.daemon = True
  thread.start()


  

from lib import socket as _socket
from lib import event_node as _event_node

_events = _event_node.EventNode()

def _trigger_online():
  _events.trigger('online')

def _trigger_offline():
  _events.trigger('offline')
  
_socket.Socket.events.on('connected', _trigger_online)
_socket.Socket.events.on('disconnected', _trigger_offline)

on = _events.on

def start(host='localhost', port=9000, uuid=None, secret=None):
  _socket.Socket.start(host=host, port=port)

def stop():
  _socket.Socket.stop()


  

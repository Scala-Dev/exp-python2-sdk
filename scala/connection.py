""" Proxy for socket online/offline events. """

from lib import socket
from lib import event_node

events = event_node.EventNode()

class Connection(object):
  on = events.on

def _trigger_online():
  events.trigger('online')

def _trigger_offline():
  events.trigger('offline')

socket.Socket.events.on('online', _trigger_online)
socket.Socket.events.on('offline', _trigger_offline)    
  
  

  





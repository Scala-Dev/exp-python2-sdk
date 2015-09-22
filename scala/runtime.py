from lib import socket
from lib import event_node
from lib import credentials
from lib import config

_events = event_node.EventNode()
on = _events.on

def _trigger_online():
  _events.trigger('online')

def _trigger_offline():
  _events.trigger('offline')
  
socket.on('connected', _trigger_online)
socket.on('disconnected', _trigger_offline)

def start(
    host='http://api.exp.scala.com',
    port=80,
    uuid=None,
    secret=None,
    username=None,
    password=None,
    organization=None,
    token=None,
    **kwargs):
  config.set(host=host, port=port)
  if uuid and secret:
    credentials.set_device_credentials(uuid, secret)
  elif username and password and organization:
    credentials.set_user_credentials(username, password, organization)
  elif token:
    credentials.set_token(token)
  socket.start(host, port, credentials.get_token())
  
def stop():
  socket.stop()


  

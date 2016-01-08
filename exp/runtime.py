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
    host='https://api.exp.scala.com',
    port=None,
    uuid=None,
    deviceUuid=None,
    secret=None,
    username=None,
    password=None,
    organization=None,
    token=None,
    networkUuid=None,
    consumerAppUuid=None,
    apiKey=None,
    timeout=None,
    **kwargs):

  if port is None:
    if host.startswith('http:'):
      port = 80
    else:
      port = 443

  config.set(host=host, port=port, timeout=timeout)

  if uuid and secret:
    credentials.set_device_credentials(uuid, secret)
  elif deviceUuid and secret:
    credentials.set_device_credentials(deviceUuid, secret)
  elif uuid and apiKey:
    credentials.set_consumer_app_credentials(uuid, apiKey)
  elif networkUuid and apiKey:
    credentials.set_consumer_app_credentials(networkUuid, apiKey)
  elif consumerAppUuid and apiKey:
    credentials.set_consumer_app_credentials(consumerAppUuid, apiKey)
  elif username and password and organization:
    credentials.set_user_credentials(username, password, organization)
  elif token:
    credentials.set_token(token)

  socket.start(host, port, credentials.get_token())

  
def stop():
  socket.stop()


  

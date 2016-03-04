""" Main module for Scala EXP SDK """

import signal
import sys

from .runtime import runtime as _runtime
from .network import network as _network
from .network import socket as _socket
from .authenticator import authenticator as _authenticator
from .exceptions import *
from . import api
from . import api_utils


# Start the SDK.
def start (*args, **kwargs):
  return _runtime.start(*args, **kwargs)

def get_auth ():
  return _authenticator.get_auth()

def get_channel(*args, **kwargs):
  return _network.get_channel(*args, **kwargs)

def get_connection_status(*args, **kwargs):
  return _socket.is_connected


def get (*args, **kwargs):
  return api_utils.get(*args, **kwargs)

def post (*args, **kwargs):
  return api_utils.post(*args, **kwargs)

def patch (*args, **kwargs):
  return api_utils.patch(*args, **kwargs)

def put (*args, **kwargs):
  return api_utils.put(*args, **kwargs)

def delete (*args, **kwargs):
  return api_utils.delete(*args, **kwargs)


def get_device (*args, **kwargs):
  return api.Device.get(*args, **kwargs)

def find_devices (*args, **kwargs):
  return api.Device.find(*args, **kwargs)

def create_device (*args, **kwargs):
  return api.Device.create(*args, **kwargs)


def get_thing (*args, **kwargs):
  return api.Thing.get(*args, **kwargs)

def find_things (*args, **kwargs):
  return api.Thing.find(*args, **kwargs)

def create_thing (*args, **kwargs):
  return api.Thing.create(*args, **kwargs)


def get_experience (*args, **kwargs):
  return api.Experience.get(*args, **kwargs)

def find_experiences (*args, **kwargs):
  return api.Experience.find(*args, **kwargs)

def create_experience (*args, **kwargs):
  return api.Experience.create(*args, **kwargs)


def get_location (*args, **kwargs):
  return api.Location.get(*args, **kwargs)

def find_locations (*args, **kwargs):
  return api.Location.find(*args, **kwargs)

def create_location (*args, **kwargs):
  return api.Location.create(*args, **kwargs)


def get_data (*args, **kwargs):
  return api.Data.get(*args, **kwargs)

def find_data (*args, **kwargs):
  return api.Data.find(*args, **kwargs)

def create_data (*args, **kwargs):
  return api.Data.create(*args, **kwargs)


def get_feed (*args, **kwargs):
  return api.Feed.get(*args, **kwargs)

def find_feeds (*args, **kwargs):
  return api.Feed.find(*args, **kwargs)

def create_feed (*args, **kwargs):
  return api.Feed.create(*args, **kwargs)


def get_content (*args, **kwargs):
  return api.Content.get(*args, **kwargs)

def find_content (*args, **kwargs):
  return api.Content.find(*args, **kwargs)


# Terminate the SDK when Ctrl-C is pressed.
signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(1))


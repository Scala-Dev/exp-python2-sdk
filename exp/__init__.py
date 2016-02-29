""" Main module for Scala EXP SDK """

import signal
import sys

from .runtime import runtime as _runtime
from .network import network as _network
from .authenticator import authenticator as _authenticator
from .exceptions import *

# Start the SDK.
def start (*args, **kwargs):
  return _runtime.start(*args, **kwargs)

def stop ():
  _runtime.stop()
  return sys.exit(1) 

def get_auth ():
  return _authenticator.get_auth()


# Terminate the SDK when Ctrl-C is pressed.
signal.signal(signal.SIGINT, lambda signal, frame: stop())


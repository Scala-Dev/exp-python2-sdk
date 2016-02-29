""" Main module for Scala EXP SDK """

import signal
import sys

from .runtime import runtime as _runtime
from .network import network as _network
from .authenticator import authenticator as _authenticator
from .exceptions import *

# Terminate the SDK when Ctrl-C is pressed.
signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(1))

# Start the SDK.
def start (*args, **kwargs):
  return _runtime.start(*args, **kwargs)

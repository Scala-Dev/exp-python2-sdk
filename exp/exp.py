import signal
import sys
from . import network
from .runtime import runtime
import logging
import utils






class Exp (object):

  def start (*args, **kwargs):

    print 'STARTING'
    return runtime.start(**kwargs)

  def stop (*args, **kwargs):
    return runtime.stop(*args, **kwargs)



#def stop():
#  socket.stop()

def signal_handler(signal, frame):
  print 'GOT SIGING'
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
exp = Exp()

#signal.pause()

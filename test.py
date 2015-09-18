from scala import channels
from scala import runtime
import time

def test():
  print 'ONLINE!'

def test2():
  print 'OFFLINE!'
  
runtime.on('online', test)
runtime.on('offline', test2)
runtime.start()
experience = channels.system.request('getCurrentExperience')
runtime.stop()
time.sleep(5)


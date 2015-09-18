import time
import scala

def on_online():
  print "SDK is online. This is a difference thread."

def on_offline():
  print "SDK is offline. This is a different thread."

def on_some_event(payload=None, **kwargs):
  print "Event detected!"

    
scala.runtime.on('online', test)
scala.runtime.on('offline', test2)
scala.runtime.start(username="email@email.com", password="Password12321", organization="scala")

response = scala.channels.system.request(name="getCurrentExperience")

scala.channels.system.broadcast(name="flingThatShit!", payload={})
scala.channels.system.listen(name="event24", callback=on_some_event)

devices = scala.api.devices.search()
devices[0].document["name"] = 'HI MOM!!!!!'
devices[0].save()

experiences = scala.api.experiences.search()
experiences[0].document["name"] = "Experience Test Name"
experiences[0].save()

time.sleep(5)Any
scala.runtime.stop()



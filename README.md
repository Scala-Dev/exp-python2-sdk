# Summary and Example
The SDK is an importable Python module that facilitates API and event bus actions on EXP.

```python
import scala
scala.runtime.start(
  username="joe@scala.com",
  password="joesmoe25",
  host="http://localhost",
  port=9000,
  organization="scala")
devices = scala.api.get_devices()
devices[0].document.name = "My Device"
devices[0].save()
scala.channels.organization.broadcast(name="I changed a device!")
response = scala.channels.experience.request(name="sendMeMoney", target={ 
   "device": devices[0].document["uuid"] })
print response
scala.runtime.stop()
```

# scala.runtime

## scala.runtime.start()
The SDK must be initialized by calling ```scala.runtime.start()``` and passing in configuration options. This starts the event bus and automatically authenticates API calls. The start command will block until a connection is first established. 

```python
# Authenticate with username and password.
scala.runtime.start(
  username="joe@scala.com",
  password="joesmoe25",
  organization="scala")
# Authenticate with device uuid and secret.
scala.runtime.start(uuid="[uuid]", secret="[secret]")
```

## scala.runtime.stop()
A socket connection is made to EXP that is non-blocking. To end the connection and to stop threads spawned by the SDK call ```scala.runtime.stop()```.

## scala.runtime.on()

Can listen for when the event bus is online/offline. Triggers an asynchronous callback.

```python
def on_online():
  print "Online!"
def on_offline():
  print "Offline!"
scala.runtime.on("online", callback=on_online)
scala.runtime.on("offline", callback=on_offline)
```

# scala.api
API abstraction layer.

## Example
```python
devices = scala.api.get_devices(**params)  # Query for device objects (url params).
device = scala.api.get_device(uuid)  # Get device by UUID.
device = scala.api.create_device(document)  # Create a device from a dictionary
```
Other available namespaces: experiences, zones, locations, content_node. Content nodes do not currently support queries or creation, only "get_content_node(uuid)".

## API Resources
Each resource object contains a "document" field which is a dictionary representation of the raw resource, along with "save" and "delete" methods.
```python
device = scala.api.create_device({ "field": value })
device.document["field"] = 123
device.save()
print device.document["field"]
device.delete()
```

The "content_node" resource has a ```get_children()``` method that returns the content node's children (a list of content node objects). Every content node object also has a ```get_url()``` method that returns a delivery url for the content.

# scala.channels
Parent namespace for interaction with the event bus. Available channels are:
```python
scala.channels.system  # Calls to and from the system
scala.channels.experience
scala.channels.location
scala.channels.organization
```

## scala.channels.[channel].request
Send a request on this channel.
```python
response = scala.channels.location.request(
  name="getSomething", 
  target= { "device" : "[uuid]"}, payload= { "info": 123 })
```

## scala.channels.[channel].respond
Attach a callback to handle requests to this device. Return value of callback is response content. Must be JSON serializable.
```python
def get_something(payload=None):
  return "Something"
scala.channels.location.respond(name="getSomething", callback=get_something_callback)
```

## scala.channels.[channel].broadcast
Sends a broadcast message on the channel.
```python
scala.channels.experience.broadcast(name="Hi!", payload={})
```

## scala.channels.[channel].listen
Listens for broadcasts on the channel. Non-blocking, callback is spawned in new thread.
```python
def my_method(payload=None):
  print payload
scala.channels.experience.listen(name="Hi!", callback=my_method)
```










# Summary and Example
The SDK is an importable Python module that facilitates API and event bus actions on EXP.

```python
import exp
exp.runtime.start(
  username="joe@exp.com",
  password="joesmoe25",
  host="http://localhost",
  port=9000,
  organization="exp")
devices = exp.api.get_devices()
devices[0].document.name = "My Device"
devices[0].save()
exp.channels.organization.broadcast(name="I changed a device!")
response = exp.channels.experience.request(name="sendMeMoney", target={ 
   "device": devices[0].document["uuid"] })
print response
exp.runtime.stop()
```

# exp.runtime

## exp.runtime.start()
The SDK must be initialized by calling ```exp.runtime.start()``` and passing in configuration options. This starts the event bus and automatically authenticates API calls. The start command will block until a connection is first established. 

```python
# Authenticate with username and password.
exp.runtime.start(
  username="joe@exp.com",
  password="joesmoe25",
  organization="exp")
# Authenticate with device uuid and secret.
exp.runtime.start(uuid="[uuid]", secret="[secret]")
```

## exp.runtime.stop()
A socket connection is made to EXP that is non-blocking. To end the connection and to stop threads spawned by the SDK call ```exp.runtime.stop()```.

## exp.runtime.on()

Can listen for when the event bus is online/offline. Triggers an asynchronous callback.

```python
def on_online():
  print "Online!"
def on_offline():
  print "Offline!"
exp.runtime.on("online", callback=on_online)
exp.runtime.on("offline", callback=on_offline)
```

# exp.api
API abstraction layer.

## Example
```python
devices = exp.api.find_devices(**params)  # Query for device objects (url params).
device = exp.api.get_device(uuid)  # Get device by UUID.
device = exp.api.create_device(document)  # Create a device from a dictionary
```
Other available namespaces: experiences, locations, content, data. Content nodes do not currently support queries or creation, only "get_content(uuid)".

## API Resources
Each resource object contains a "document" field which is a dictionary representation of the raw resource, along with "save" and "delete" methods.
```python
device = exp.api.create_device({ "field": value })
device.document["field"] = 123
device.save()
print device.document["field"]
device.delete()
```

The "content" resource has a ```get_children()``` method that returns the content node's children (a list of content objects). Every content node object also has a ```get_url()``` method that returns a delivery url for the content.

# exp.channels
Parent namespace for interaction with the event bus. Available channels are:
```python
exp.channels.system  # Calls to and from the system
exp.channels.experience
exp.channels.location
exp.channels.organization
```

## exp.channels.[channel].request
Send a request on this channel.
```python
response = exp.channels.location.request(
  name="getSomething", 
  target= { "device" : "[uuid]"}, payload= { "info": 123 })
```

## exp.channels.[channel].respond
Attach a callback to handle requests to this device. Return value of callback is response content. Must be JSON serializable.
```python
def get_something(payload=None):
  return "Something"
exp.channels.location.respond(name="getSomething", callback=get_something_callback)
```

## exp.channels.[channel].broadcast
Sends a broadcast message on the channel.
```python
exp.channels.experience.broadcast(name="Hi!", payload={})
```

## exp.channels.[channel].listen
Listens for broadcasts on the channel. Non-blocking, callback is spawned in new thread.
```python
def my_method(payload=None):
  print payload
exp.channels.experience.listen(name="Hi!", callback=my_method)
```










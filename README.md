# Summary and Example
The SDK is an importable Python module that facilitates API and event bus actions on EXP.

```python
import exp
exp.start(
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

## exp.start()
The SDK must be initialized by calling ```exp.start()``` and passing in configuration options. This starts the event bus and automatically authenticates API calls. The start command will block until a connection is first established. 

```python
# Authenticate with username and password.
exp.start(
  username="joe@exp.com",
  password="joesmoe25",
  organization="exp")
# Authenticate with device uuid and secret.
exp.start(uuid="[uuid]", secret="[secret]")
# Authenticate with consumer app uuid and api key.
exp.start(uuid="[uuid]", apiKey="[apiKey]")
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
Other available namespaces: experiences, locations, content, data. content does not currently support creation, only "get_content(uuid) and find_content(params)".

## API Resources
Each resource object contains a "document" field which is a dictionary representation of the raw resource, along with "save" and "delete" methods.
```python
device = exp.api.create_device({ "field": value })
device.document["field"] = 123
device.save()
print device.document["field"]
device.delete()
```


```python
data = exp.api.get_data("key1", "group0")
print data.value
data.value = { "generic": 1111 }
data.save()
data.delete()

data = exp.api.create_data(key="4", group="cats", { "name": "fluffy" })

```

The "content" resource has a ```get_children()``` method that returns the content's children (a list of content objects). Every content object also has a ```get_url()``` and ```get_variant_url(name)``` method that returns a delivery url for the content.

The "feed" resource has a ```get_data()``` method that returns a the feed's decoded JSON document.






## The EXP Network

The EXP network facilitates real time communication between entities connected to EXP. A user or device can broadcast a JSON serializable payload to users and devices in your organization, and listeners to those broadcasts can respond to the broadcasters.

### Channels

All messages on the EXP network are sent over a channel. Channels have a name, and two flags: ```system``` and ```consumer```.

```python
channel = exp.get_channel("my_channel", system=False, consumer=False)
```

Use ```system=True``` to get a system channel. You cannot send messages on a system channels but can listen for system notifications, such as updates to API resources.

Use ```consumer=True``` to get a consumer channel. Consumer devices can only listen or broadcast on consumer channels. When ```consumer=False``` you will not receive consumer device broadcasts and consumer devices will not be able to hear your broadcasts.

Both ```system``` and ```consumer``` default to ```False``` except for consumer devices, where ```consumer``` will always be ```True``` for all channels.


### Broadcasting

Use the broadcast method of a channel object to send a named message with a JSON serializable payload to other entities on the EXP network. You can optionally include a timeout to wait for responses to the broadcast. The broadcast will block for approximately the given timeout and return a list of response payloads. Each response payload can any JSON serializable type.

```python
channel = exp.get_channel("my_channel")
responses = channel.broadcast(name='Hello!', timeout=5, payload=[1, 2, 3])
[print response for response in responses]
```


### Listening

To listen for broadcasts, call the listen method of a channel object. 

```python
channel = exp.get_channel("my_channel")
listener = channel.listen("my_event")

while True:
  broadcast = listener.wait(5)
  if broadcast: 
    print "Message received!"
    print broadcast.payload
```




### Responding

To respond to broadcast, call the respond method on the broadcast object, optionally passing in a JSON serializable response payload.

```python

channel = exp.get_channel("my_channel")
listener = channel.listen(name="my_custom_event")

while True:
  broadcast = listener.wait(5)
  if broadcast and broadcast.payload is "hello!":
    print "Responding to broadcast."
    broadcast.respond("Nice to meet you!")

```









# Starting the SDK

The SDK is started by calling ```exp.start``` and specifying your credentials and configuration options as keyword arguments. ```exp.start``` will start additional threads to process network events. You may supply user, device, or consumer app credentials. You can also authenticate in pairing mode.

When ```exp.start``` returns, you are authenticated and can begin using the SDK. 



## User Credentials

Users must specify their ```username```, ```password```, and ```organization``` as keyword arguments to ```exp.start```.

```python
import exp

exp.start(username='joe@joemail.com', password='JoeRocks42', organization='joesorg')

```

## Device Credentials

Devices must specify their ```uuid``` and ```secret``` as keyword arguments.

```python
import exp

exp.start(uuid='[uuid]', secret='[secret]')

```

## Consumer App Credentials

Consumer apps must specify their ```uuid``` and ```api_key``` as keyword arguments.

```python
import exp

exp.start(uuid='[uuid]', api_key='[api key]')

```

## Pairing Mode

Advanced users can authenticate in pairing mode by setting ```allow_pairing``` to ```False```.

```python
import exp

exp.start(allow_pairing=False)

```


## Additional Options

Name | Default | Description
--- | --- | ---
host | ```'https://api.goexp.io'``` | The api server to authenticate with.
enable_network | ```True``` | Whether to enable real time network communication. If set to ```False``` you will be unable to listen on the [EXP network](# Communicating on the EXP Network).

### Exceptions

If the arguments specified to ```exp.start``` are invalid or incomplete an ```exp.RuntimeError``` will be raised.





# Communicating on the EXP Network

The EXP network facilitates real time communication between entities connected to EXP. A user or device can broadcast a JSON serializable payload to users and devices in your organization, and listeners to those broadcasts can respond to the broadcasters.

### Channels

All messages on the EXP network are sent over a channel. Channels have a name, and two flags: ```system``` and ```consumer```.

```python
channel = exp.get_channel('my_channel', system=False, consumer=False)
```

Use ```system=True``` to get a system channel. You cannot send messages on a system channels but can listen for system notifications, such as updates to API resources.

Use ```consumer=True``` to get a consumer channel. Consumer devices can only listen or broadcast on consumer channels. When ```consumer=False``` you will not receive consumer device broadcasts and consumer devices will not be able to hear your broadcasts.

Both ```system``` and ```consumer``` default to ```False```. Consumer devices will be unable to broadcast or listen to messages on non-consumer channels.


### Broadcasting

Use the broadcast method of a channel object to send a named message containing an optional JSON serializable payload to other entities on the EXP network. You can optionally include a timeout to wait for responses to the broadcast. The broadcast will block for approximately the given timeout and return a ```list``` of response payloads. Each response payload can any JSON serializable type.

```python

channel = exp.get_channel('my_channel')
responses = channel.broadcast(name='my_event', timeout=5, payload='hello')
[print response for response in responses]

```


### Listening

To listen for broadcasts, call the listen method of a channel object and pass in the name of the event you wish to listen for. When EXP listener has been registered and can start receiving events, a ```listener``` object will be returned. 

Call the ```wait``` method of a listener to block until a broadcast is received, passing in a timeout in seconds. If ```timeout``` elaspes and no broadcasts have been received, ```wait``` will return ```None```.

Once a listener is created, it will receive broadcasts in a background thread even when not waiting. Calling ```wait``` will first attempt to return the oldest broadcast in the queue. Queued broadcasts will be discarded after ~60s if not retrieved during a ```wait```.

```python

channel = exp.get_channel('my_channel')
listener = channel.listen('my_event')

while True:
  broadcast = listener.wait(5)
  if broadcast:
    print 'Message received!'
    print broadcast.payload
    listener.cancel()
    break

```


### Responding

To respond to broadcast, call the respond method on the broadcast object, optionally passing in a JSON serializable response payload.

```python

channel = exp.get_channel('my_channel')
listener = channel.listen(name='my_event')

while True:
  broadcast = listener.wait(5)
  if broadcast and broadcast.payload is 'hello':
    print 'Responding to broadcast.'
    broadcast.respond('Nice to meet you!')

```


# SDK Resources

EXP API resources are represented by abstract objects.




# SDK Reference

exp.start(**kwargs)
exp.get_channel(name, system=False, consumer=False)

exp.get_device(uuid)
exp.create_device(document)
exp.find_devices(**params)

exp.get_experience(uuid)




# exp.api
API abstraction layer.

## Example
```python
devices = exp.api.find_devices(**params)  # Query for device objects (url params).
device = exp.api.get_device(uuid)  # Get device by UUID.
device = exp.api.create_device(document)  # Create a device from a dictionary
```
Other available namespaces: experiences, locations, content, data. content does not currently support creation, only "get_content(uuid) and find_content(params)".

# Interacting with API Resources

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





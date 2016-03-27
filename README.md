

# Getting Started

The SDK is started by calling ```exp.start``` and specifying your credentials and configuration options as keyword arguments. ```exp.start``` will start additional threads to process network events. You may supply user, device, or consumer app credentials. You can also authenticate in pairing mode. When ```exp.start``` returns, you are authenticated and can begin using the SDK. 

Users must specify their ```username```, ```password```, and ```organization``` as keyword arguments to ```exp.start```.

```python
exp.start(username='joe@joemail.com', password='JoeRocks42', organization='joesorg')
```

Devices must specify their ```uuid``` and ```secret``` as keyword arguments.

```python
exp.start(uuid='[uuid]', secret='[secret]')
```

Consumer apps must specify their ```uuid``` and ```api_key``` as keyword arguments.

```python
exp.start(uuid='[uuid]', api_key='[api key]')
```

Advanced users can authenticate in pairing mode by setting ```allow_pairing``` to ```False```.

```python
exp.start(allow_pairing=False)
```

Additional options:

Name | Default | Description
--- | --- | ---
host | ```'https://api.goexp.io'``` | The api server to authenticate with.
enable_network | ```True``` | Whether to enable real time network communication. If set to ```False``` you will be unable to listen on the [EXP network](# Communicating on the EXP Network).


# Reference

## Runtime

### exp_sdk.start(**options)

Starts and returns an sdk instance.

```python

import exp_sdk

# Authenticating as a user.
exp = exp_sdk.start(username='joe@scala.com', password='joeIsAwes0me', organization='joeworld')

# Authenticating as a device.
exp = exp_sdk.start(uuid='[uuid]', secret='[secret]')

# Authenticating as a consumer app.
exp = exp_sdk.start(uuid='[uuid]', api_key='[api-key]')

```

`start` can be called multiple times to start multiple independent instances of the sdk. The sdk can be started using user, device, or consumer app credentials.

`**options` supports the following keyword arguments:

Name | Default | Description
--- | --- | ---
username | `None` | The username used to log in to EXP. Required user credential.
password | `None` | The password of the user. Required user credential.
organization | `None` | The organization of the user. Required user credential
uuid | `None` | The device or consumer app uuid. Required consumer app credential and required device credential unless `allow_pairing` is `True`.
secret | `None` | The device secret. Required device credential unless `allow_pairing` is `True`.
api_key | `None` | The consumer app api key. Required consumer app credential.
allow_pairing | `False` | Whether to allow authentication to fallback to pairing mode. If `True`, invalid or empty device credentials will start the sdk in pairing mode.
host | `https://api.goexp.io` | The api host to authenticate with.
enable_network | `True` | Whether or not to establish a socket connection with the EXP network. If `False`, you will not be able to listen for broadcasts.


### exp_sdk.stop()

Stops all running instances of the sdk, cancels all listeners and stops all network connections.

```python

exp_1 = exp_sdk.start(**options_1)
exp_2 = exp_sdk.start(**options_2)

exp_sdk.stop()

exp_2.create_device()  # Exception.

```

New instances can still be created by calling `start`.

### exp.stop()

Stops the sdk instance, cancels its listeners, and stops all network connections.

```python

exp = exp_sdk.start(**options)
exp.stop()
exp.get_auth()  # Exception.

```

Sdk instances cannot be restarted and any invokation on the instance will raise an exception.


### exp.is_connected

Whether or not there is an active socket connection to the network.

```python

# Wait for a connection.
while not exp.is_connected:
  time.sleep(1)

```


### exp.get_auth()

Returns the up to date authentication payload. The authentication payload may be updated when invoking this method.

```python

print 'My authentication token is : %s' % exp.get_auth()['token']

```


## Network


### exp.getChannel(name, consumer=False, system=False)

Returns a the channel with the given name and flags.

```python

channel = exp.get_channel('my-consumer-channel', consumer=True)

```


### channel.broadcast(name, payload=None, timeout=0.1)

Sends a broadcast on the channel with the given name and payload. Returns a list of responses. `timeout` is the number of seconds to hold the request open to wait for responses.

```python

channel = exp.get_channel('my-channel')
responses = channel.broadcast('hi!', { 'test': 'nice to meet you!' })
[print response for response in responses]

```


### channel.listen(name, max_age=60)

Returns a listener for events on the channel. `max_age` is the number of seconds the listener will keep events before they are discarded.

```python

channel = exp.get_channel('my-channel')
listener = channel.listen('my-event', max_age=30)

```


## listener.wait(timeout=0)

Wait for `timeout` seconds for broadcasts. Returns a broadcast if a broadcast is in the queue or if a broadcast is received before the timeout. If timeout is reached, returns `None`.

```python
channel = exp.get_channel('my-channel')
listener = channel.listen('my-event')

while True:
  broadcast = listener.wait(60)
  if broadcast:
    print 'I got a broadcast!'

```


## listener.cancel()

Cancels the listener. The listener is unsubscribed from broadcasts and will no longer receive messages. This cannot be undone.

```python

listener.cancel()
broadcast = listener.wait(60)  # Will always be None

```


## broadcast.payload

The payload of the broadcast. Can be any JSON serializable type.

## broadcast.respond(response)

Respond to the broadcast with a JSON serializable response.

```python

channel = exp.get_channel('my-channel')
listener = channel.listen('my-event')

while True:
  broadcast = listener.wait(60)
  if broadcast && broadcast.payload == 'hi!':
    broadcast.respond('hi back at you!')


```





## HTTP Requests

Send custom authenticated API calls. `params` is a dictionary of url params, `payload` is a JSON serializable type, and `timeout` is the duration, in seconds, to wait for the request to complete. `path` is relative to the api host root. All methods will return a JSON serializable type.

### exp.get(path, params=None, timeout=10)

Send a GET request.

```python

# Find devices by name.
result = exp.get('/api/devices', { 'name': 'my-name' })

```

### exp.post(path, payload=None, params=None, timeout=10)

Send a POST request.

```python

# Create a new experience.
document = exp.post('/api/experiences', { 'apps': [] })

```


### exp.patch(path, payload=None, params=None, timeout=10)

Send a PATCH request.

```python

# Change the name of an experience.
document = exp.patch('/api/experiences/[uuid]', { 'name': 'new-name' })

```


### exp.put(path, payload=None, params=None, timeout=10)

Send a PUT request.

```python

# Insert a data value.
document = exp.put('/api/data/cats/fluffy', { 'eyes': 'blue'})

```


### exp.delete(path, payload=None, params=None, timeout=10)

Send a DELETE request.

```python

# Delete a location.
exp.delete('/api/location/[uuid]')

```



## Common Resource Methods and Attributes

### resource.uuid

The uuid of the resource. Cannot be set. Maps to `resource.document['uuid']`

### resource.name

The name of the resource. Can be set directly. Maps to `resource.document['name']`.

### resource.document

The resource's underlying document

### resource.save()

Saves the resource and updates the document in place.

```python

device = exp.get_device('[uuid]')
device.name = 'my-new-name'
device.save()
# device changes are now saved

```


### resource.refresh()

Refreshes the resource's underlying document in place.

```python

device = exp.create_device()
device.name = 'new-name'
device_2 = exp.get_device(device.uuid)
device.save()
device_2.refresh()
print device_2.name  # 'new-name'

```



### resource.get_channel(system=False, consumer=False)

Returns the channel whose name is contextually associated with this resource.

```python

channel = experience.get_channel()
channel.broadcast('hello?')

```

### resource.fling(payload)

Fling an app launch payload on this resource's channel.

```python
location = exp.get_location('[uuid]')
location.fling({ 'appTemplate' : { 'uuid': '[uuid'} })

```

See ??? for more information about app launch payloads.

### resource.identify()

Requests that devices listening for this event on this resource's channel visually identify themselves. Implementation is device specific; this is simply a convience method.

```python
location = exp.get_location('[uuid]')
location.identify()  # Tell all devices at this location to identify themselves!

```







## Devices

Devices inherit all [common resource methods and attributes](#common-resource-methods-and-attributes).


### `exp.get_device(uuid=None)`
Returns the device with the given uuid or `None`.

```python

device1 = exp.get_device('[matching uuid]')
device2 = exp.get_device()  # None
device3 = exp.get_device('[unmatched uuid]')  # None

```

### `exp.create_device(document=None)`

Creates and returns a new device.

```python

device1 = exp.create_device()
device2 = exp.create_device({ 'name': 'my-new-device' })

```


### `exp.find_devices(params=None)`

Returns a list of devices matching the given query parameters. `params` is a dictionary of query parameters.

```python

devices = exp.find_devices({ 'location.zone.key': 'my-zone-key' })
[print device.name for device in devices]

```


### device.get_location()

Returns the device's location or `None`.

### device.get_experience()

Returns the device's experience or `None`




## Things

Devices inherit all [common resource methods and attributes](#common-resource-methods-and-attributes).

### thing.get_location()

Returns the device's location or `None`.

### thing.get_experience()

Returns the device's experience or `None`




### Experiences
### Locations
### Zones
### Feeds
### Data
### Content




## Exceptions

 | Description
 --- | ---
 `exp_sdk.ExpError` | Base class for all EXP exceptions.
 `exp_sdk.UnexpectedError` | Raised when an unexpected error occurs.
 `exp_sdk.RuntimeError` | Raised when [startup options](#startup-options) are incorrect or inconsistent.
 `exp_sdk.AuthenticationError` | Raised when the sdk cannot authenticate due to bad credentials.
 `exp_sdk.ApiError` | Raised when an API call fails. Has properties `message` and `code`. See the [API documentation](#https://docs.goexp.io).




## Things
- ```thing = exp.get_thing(uuid)```: Retrieves a thing by uuid.
- ```thing = exp.create_thing(document)```: Creates a thing from a dictionary.
- ```thing = exp.find_things(params)```: Retrieves a list of things given a dictionary of query parameters. See the API docs.
- ```thing.uuid```: The thing's uuid.
- ```thing.document```: The thing's underying document, a dictionary.
- ```thing.save()```: Saves the thing to EXP.
- ```thing.get_channel(system=False, consumer=False)```: Retrieves a [channel](#Channels) for communication about the thing. 

## Experiences
- ```experience = exp.get_experience(uuid)```: Retrieves an experience by uuid.
- ```experience = exp.create_experience(document)```: Creates an experience from a dictionary.
- ```experiences = exp.find_experiences(params)```: Retrieves a list of experiences given a dictionary of query params. See the API docs.
- ```experience.uuid```: The experience's uuid.
- ```experience.document```: The experience's underlying document, a dictionary.
- ```experience.save()```: Saves the experience to EXP.
- ```experience.get_channel(system=False, consumer=False)```: Get a [channel](#Channels) for communication about this experience.


## Locations
- ```location = exp.get_location(uuid)```: Retrieves a location by uuid.
- ```location = exp.create_location(document)```: Creates a location from a dictionary.
- ```locations = exp.find_locations(params)```: Retrieves a list of locations given a dictionary of query params. See the API docs.
- ```location.uuid```: The locations's uuid.
- ```location.document```: The location's underlying document, a dictionary.
- ```location.get_channel(system=False, consumer=False)```: Get a [channel](#Channels) for communication about this location.
- ```location.get_zones()```: Get a list of [zones](#Zones) that are part of this location.


## Zones
- ```zone.document```: The underlying zone's document, a dictionary.
- ```zone.get_channel(system=False, consumer=False)```: Get a [channel](#Channels) for communication about this zone.

## Content
- ```content = exp.get_content(uuid)```: Retrieves a content resource by uuid.
- ```content_list = exp.find_content(params)```: Returns a list of content using the given query params.
- ```content.get_url()```: Returns a delivery URL for content retrieval.
- ```content.get_variant_url()```: Returns a delivery URL for a variant of the content.
- ```content.children```: A list of child content resources.
- ```content.document```: The underlying zone's document, a dictionary.
- ```content.subtype```: The content subtype. See the API docs.

## Feeds
- ```feed = exp.get_feed(uuid)```: Retrieves a feed resource by uuid.
- ```feeds = exp.find_feeds(params)```: Get a list of feeds given a dictionary of query params. See the API docs.
- ```feed = exp.create_feed(document)```: Create and save a new feed from a feed document.
- ```feed.document```: The underlying feed's document, a dictionary.
- ```feed.get_data()```: Get the feed's data.


## Data
- ```data = exp.get_data(key, group='default')```: Retrieves data by key and group.
- ```data = exp.find_data(params)```: Retrieves a list of data given a dictionary of query params. See the API docs.
- ```data = exp.create_data(key, value, group='default')```: 
- ```data.save()```: Saves the data.
- ```data.value```: The value of the data, a JSON serializable type.
- ```data.key```: The data's key.
- ```data.group```: The data's group.



# Examples

## Creating a Device and Listening for Updates

Updates to API resources are sent out over a system channel with the event name "update".

```python
  device = exp.create_device({ 'name': 'my_sweet_device' })
  device.save()
  channel = device.get_channel(system=True)
  listener = channel.listen('update')
  while True:
    if listener.wait(5):
      print 'The device was updated!'
  
```


## Modifying a Resource in Place

```python
experience = exp.get_experience('[uuid]')
experience.document['name'] = 'new name'
experience.save()
```


## Using The EXP Network

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


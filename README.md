
# Installation

Install the `exp-sdk` package from PyPi via your favorite python package manager.

```bash
pip install exp-sdk
```

This gives your environment access to the ```exp_sdk``` module. 


# Runtime

## Starting the SDK

**`exp_sdk.start(options)`**

Starts and returns an sdk instance. Can be called multiple times to start multiple independent instances of the sdk. The sdk can be started using user, device, or consumer app credentials.`**options` supports the following keyword arguments:

- `username=None` The username used to log in to EXP. Required user credential.
- `password=None` The password of the user. Required user credential.
- `organization=None` The organization of the user. Required user credential
- `uuid=None` The device or consumer app uuid. Required consumer app credential and required device credential unless `allow_pairing` is `True`.
- `secret=None` The device secret. Required device credential unless `allow_pairing` is `True`.
- `api_key=None` The consumer app api key. Required consumer app credential.
- `allow_pairing=False` Whether to allow authentication to fallback to pairing mode. If `True`, invalid or empty device - credentials will start the sdk in pairing mode.
- `host=https://api.goexp.io` The api host to authenticate with.
- `enable_network=True` Whether or not to establish a socket connection with the EXP. If `False`, you will not be - able to listen for broadcasts.

```python
import exp_sdk

# Authenticating as a user.
exp = exp_sdk.start(username='joe@scala.com', password='joeIsAwes0me', organization='joeworld')

# Authenticating as a device.
exp = exp_sdk.start(uuid='[uuid]', secret='[secret]')

# Authenticating as a consumer app.
exp = exp_sdk.start(uuid='[uuid]', api_key='[api-key]')
```



## Stopping the SDK


**`exp_sdk.stop()`**

Stops all running instances of the sdk, cancels all listeners and stops all socket connections.

```python
exp_1 = exp_sdk.start(**options_1)
exp_2 = exp_sdk.start(**options_2)

exp_sdk.stop()
exp_2.create_device()  # Exception.
```

New instances can still be created by calling `start`.

**`exp.stop()`**

Stops the sdk instance, cancels its listeners, and stops all socket connections.

```python
exp = exp_sdk.start(**options)
exp.stop()
exp.get_auth()  # Exception.
```

Sdk instances cannot be restarted and any invokation on the instance will raise an exception.

## Exceptions

 **`exp_sdk.ExpError`**

 Base class for all EXP exceptions.

 **`exp_sdk.UnexpectedError`**

 Raised when an unexpected error occurs.

 **`exp_sdk.RuntimeError`**

 Raised when [startup options](#runtime) are incorrect or inconsistent.

 **`exp_sdk.NetworkError`**

Raised when an error or timeout occurs when attempting to listen on the network.

 **`exp_sdk.AuthenticationError`**

 Raised when the sdk cannot authenticate due to bad credentials.

 **`exp_sdk.ApiError`**

 Raised when an API call fails. Has properties `message` and `code`.


## Authentication Payload


**`exp.get_auth()`**

Returns the up to date authentication payload. The authentication payload may be updated when invoking this method.

```python
print 'My authentication token is : %s' % exp.get_auth()['token']
```


## Logging

The EXP SDK uses the ```exp-sdk``` logger namespace.


# Real Time Communications

## Status

**`exp.is_connected`**

Whether or not there is an active socket connection.

```python
# Wait for a connection.
while not exp.is_connected:
  time.sleep(1)
```


## Channels

**`exp.get_channel(name, consumer=False, system=False)`**

Returns a [channel](#channels) with the given name and flags.

```python
channel = exp.get_channel('my-consumer-channel', consumer=True)
```

**`channel.broadcast(name, payload=None, timeout=0.1)`**

Sends a [broadcast](#broadcast) on the channel with the given name and payload and returns a list of responses. `timeout` is the number of seconds to hold the request open to wait for responses.

```python
responses = channel.broadcast('hi!', { 'test': 'nice to meet you!' })
[print response for response in responses]
```

**`channel.listen(name, timeout=10, max_age=60)`**

Returns a [listener](#listener) for events on the channel. `timeout` is how many seconds to wait for the channel to open. `max_age` is the number of seconds the listener will buffer events before they are discarded. If `timeout` is reached before the channel is opened, a `NetworkError` will be raised.

```python
channel = exp.get_channel('my-consumer-channel', consumer=True)
listener = channel.listen('hi', max_age=30)
```

**`channel.fling(payload)`**

Fling an app launch payload on the channel.

```python
location = exp.get_location('[uuid]')
location.get_channel().fling({ 'appTemplate' : { 'uuid': '[uuid'} })
```


**`channel.identify()`**

Requests that [devices](#device) listening for this event on this channel visually identify themselves. Implementation is device specific; this is simply a convience method.


## Listeners

**`listener.wait(timeout=0)`**

Wait for `timeout` seconds for broadcasts. Returns a [broadcast](#broadcasts) if a [broadcast](#broadcasts) is in the queue or if a [broadcast](#broadcasts) is received before the timeout. If timeout is reached, returns `None`. If timeout is set to 0 (the default), will return immediately.

```python
channel = exp.get_channel('my-channel')
listener = channel.listen('my-event')

while True:
  broadcast = listener.wait(60)
  if broadcast:
    print 'I got a broadcast!'
```

[Broadcasts](#broadcasts) are returned in the order they are received.

**`listener.cancel()`**

Cancels the listener. The listener is unsubscribed from [broadcasts](#broadcast) and will no longer receive messages. This cannot be undone.

## Broadcasts

**`broadcast.payload`**

The payload of the broadcast. Can be any JSON serializable type.

**`broadcast.respond(response)`**

Respond to the broadcast with a JSON serializable response.

```python
channel = exp.get_channel('my-channel')
listener = channel.listen('my-event')

while True:
  broadcast = listener.wait(60)
  if broadcast and broadcast.payload == 'hi!':
    broadcast.respond('hi back at you!')
    break
```


# API


## Devices

Devices inherit all [common resource methods and attributes](#resources).

**`exp.get_device(uuid=None)`** 

Returns the device with the given uuid or `None` if no device could be found.

**`exp.get_current_device()`** 

Returns the current device or `None` if not applicable.

**`exp.create_device(document=None)`**

Returns a device created based on the supplied document.

```python
device = exp.create_device({ 'subtype': 'scala:device:player' })
```

**`exp.find_devices(params=None)`**

Returns an iterable of devices matching the given query parameters. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

**`device.get_location()`**

Returns the device's [location](#locations) or `None`.

**`device.get_zones()`**

Returns a list of the device's [zones](#zones).

**`device.get_experience()`**

Returns the device's [experience](#experiences) or `None`


## Things

Things inherit all [common resource methods and attributes](#resources).

**`exp.get_thing(uuid=None)`**

Returns the thing with the given uuid or `None` if no things could be found.

**`exp.create_thing(document=None)`**

Returns a thing created based on the supplied document.

```python
thing = exp.create_thing({ 'subtype': 'scala:thing:rfid', 'id': '[rfid]', 'name': 'my-rfid-tag' })
```

**`exp.find_things(params=None)`**

Returns an iterable of things matching the given query parameters. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

**`thing.get_location()`**

Returns the thing's [location](#locations) or `None`.

**`thing.get_zones()`**

Returns a list of the thing's [#zones](#zones).

**`thing.get_experience()`**

Returns the device's [experience](#experiences) or `None`


## Experiences

Experiences inherit all [common resource methods and attributes](#resources).

**`exp.get_experience(uuid=None)`**

Returns the experience with the given uuid or `None` if no experience could be found.

**`exp.get_current_experience()`** 

Returns the current experience or `None`.

**`exp.create_experience(document=None)`**

Returns an experience created based on the supplied document.

**`exp.find_experiences(params=None)`**

Returns an iterable of experiences matching the given query parameters. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

**`experience.get_devices(params=None)`**

Returns an iterable of [devices](#devices) that are part of this experience. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).


## Locations
Locations inherit all [common resource methods and attributes](#resources).

**`exp.get_location(uuid=None)`**

Returns the location with the given uuid or `None` if no location could be found.

**`exp.get_current_location()`** 

Returns the current location or `None`.

**`exp.create_location(document=None)`**

Returns a location created based on the supplied document.

**`exp.find_locations(params=None)`**

Returns an iterable of locations matching the given query parameters. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).


**`location.get_devices(params=None)`**

Returns an iterable of [devices](#devices) that are part of this location. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

**`location.get_things(params=None)`**

Returns an iterable of [things](#things) that are part of this location. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

**`location.get_zones()`**

Returns a list of [zones](#zones) that are part of this location.

**`location.get_layout_url()`**

Returns a url pointing to the location's layout image.


## Zones
Zones inherit the [common resource methods and attributes](#resources) `save()`, `refresh()`, and `get_channel()`.

**`exp.get_current_zones()`** 

Returns a list of the current zones or an empty list.

**`zone.key`**

The zone's key.

**`zone.name`**

The zone's name.

**`zone.get_devices()`**

Returns all [devices](#devices) that are members of this zone.

**`zone.get_things()`**

Returns all [things](#things) that are members of this zone.

**`zone.get_location()`**

Returns the zone's [location](#locations)


## Feeds
Feeds inherit all [common resource methods and attributes](#resources).

**`exp.get_feed(uuid=None)`**

Returns the feed with the given uuid or `None` if no feed could be found.

**`exp.create_feed(document=None)`**

Returns a feed created based on the supplied document.

```python
feed = exp.create_feed({ 'subtype': 'scala:feed:weather', 'searchValue': '16902', 'name': 'My Weather Feed'  })
```

**`exp.find_feeds(params=None)`**

Returns an iterable of feeds matching the given query parameters. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

```python
feeds = exp.find_feeds({ 'subtype': 'scala:feed:facebook' })
```

**`feed.get_data(**params)`**

Returns the feed's data. For dynamic feeds specify key value query params in `params`.


## Data

Data items inherit the [common resource methods and attributes](#resources) `save()`, `refresh()`, and `get_channel()`.
There is a limit of 16MB per data document.

*Note that data values must be a javascript object, but can contain other primitives.*



**`exp.get_data(group='default', key=None)`**

Returns the data item with the given group or key or `None` if the data item could not be found.

```python
data = exp.get_data('cats', 'fluffy')
```

**`exp.create_data(group='default', key=None, value=None)`**

Returns a data item created based on the supplied group, key, and value.

```python
data = exp.create_data('cats', 'fluffy', { 'color': 'brown'})
```

**`exp.find_data(params=None)`**

Returns an iterable of data items matching the given query parameters. `params` is a dictionary of query parameters.  Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

```python
items = exp.find_data({ 'group': 'cats' })
```

**`data.key`**

The data item's key. Settable.

**`data.group`**

The data item's group. Settable

**`data.value`**

The data item's value. Settable.


## Content
Content items inherit all [common resource methods and attributes](#resources) except `save()`.

**`exp.get_content(uuid=None)`**

Returns the content item with the given uuid or `None` if no content item could be found.

**`exp.find_content(params=None)`**

Returns a list of content items matching the given query parameters. `params` is a dictionary of query parameters.

**`content.subtype`**

The content item's subtype. Not settable.

**`content.get_url()`**

Returns the delivery url for this content item.

**`content.has_variant(name)`**

Returns a boolean indicating whether or not this content item has a variant with the given name.

**`content.get_variant_url(name)`**

Returns the delivery url for a variant of this content item.

**`content.get_children(params)`**

Returns an iterable of the content items children. `params` is a dictionary of query parameters. Iterable also has attributes matching the raw API response document properties (i.e. `total` and `results`).

## Resources

These methods and attributes are shared by many of the abstract API resources.

**`resource.uuid`**

The uuid of the resource. Cannot be set.

**`resource.name`**

The name of the resource. Can be set directl

**`resource.document`**

The resource's underlying document

**`resource.save()`**

Saves the resource and updates the document in place.

```python
device = exp.get_device('[uuid]')
device.name = 'my-new-name'
device.save()  # device changes are now saved
```

**`resource.refresh()`**

Refreshes the resource's underlying document in place.

```python
device = exp.create_device()
device.name = 'new-name'
device_2 = exp.get_device(device.uuid)
device.save()
device_2.refresh()
print device_2.name  # 'new-name'
```

**`resource.get_channel(system=False, consumer=False)`**

Returns the channel whose name is contextually associated with this resource.

```python
channel = experience.get_channel()
channel.broadcast('hello?')
```

## Custom Requests

These methods all users to send custom authenticated API calls. `params` is a dictionary of url params, `payload` is a JSON serializable type, and `timeout` is the duration, in seconds, to wait for the request to complete. `path` is relative to the api host root. All methods will return a JSON serializable type.

**`exp.get(path, params=None, timeout=10)`**

Send a GET request.

```python
result = exp.get('/api/devices', { 'name': 'my-name' })  # Find devices by name.
```

**`exp.post(path, payload=None, params=None, timeout=10)`**

Send a POST request.

```python
document = exp.post('/api/experiences', {})  # Create a new empty experience.
```

**`exp.patch(path, payload=None, params=None, timeout=10)`**

Send a PATCH request.

```python
document = exp.patch('/api/experiences/[uuid]', { 'name': 'new-name' })  # Rename an experience.
```


**`exp.put(path, payload=None, params=None, timeout=10)`**

Send a PUT request.

```python
document = exp.put('/api/data/cats/fluffy', { 'eyes': 'blue'})  # Insert a data value.
```

**`exp.delete(path, params=None, timeout=10)`**

Send a DELETE request.

```python
exp.delete('/api/location/[uuid]') # Delete a location.
```

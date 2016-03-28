# Python SDK Reference v1.0.0

## Installation

## Runtime

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
- `enable_network=True` Whether or not to establish a socket connection with the EXP network. If `False`, you will not be - able to listen for broadcasts.

```python
import exp_sdk

# Authenticating as a user.
exp = exp_sdk.start(username='joe@scala.com', password='joeIsAwes0me', organization='joeworld')

# Authenticating as a device.
exp = exp_sdk.start(uuid='[uuid]', secret='[secret]')

# Authenticating as a consumer app.
exp = exp_sdk.start(uuid='[uuid]', api_key='[api-key]')
```

**`exp_sdk.stop()`**

Stops all running instances of the sdk, cancels all listeners and stops all network connections.

```python
exp_1 = exp_sdk.start(**options_1)
exp_2 = exp_sdk.start(**options_2)

exp_sdk.stop()
exp_2.create_device()  # Exception.
```

New instances can still be created by calling `start`.


**`exp.stop()`**

Stops the sdk instance, cancels its listeners, and stops all network connections.

```python
exp = exp_sdk.start(**options)
exp.stop()
exp.get_auth()  # Exception.
```

Sdk instances cannot be restarted and any invokation on the instance will raise an exception.

**`exp.is_connected`**

Whether or not there is an active socket connection to the network.

```python
# Wait for a connection.
while not exp.is_connected:
  time.sleep(1)
```


**`exp.get_auth()`**

Returns the up to date authentication payload. The authentication payload may be updated when invoking this method.

```python
print 'My authentication token is : %s' % exp.get_auth()['token']
```


## Custom HTTP Requests

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

**`exp.delete(path, payload=None, params=None, timeout=10)`**

Send a DELETE request.

```python
exp.delete('/api/location/[uuid]') # Delete a location.
```

## Getting a Channel

**`exp.get_channel(name, consumer=False, system=False)`**

Returns a [channel](#channels) with the given name and flags.

```python
channel = exp.get_channel('my-consumer-channel', consumer=True)
```

## API

**`exp.get_device(uuid=None)`** 

Returns the [device](#devices) with the given uuid or `None` if no [device](#devices) could be found.

**`exp.create_device(document=None)`**

Returns a [device](#devices) created based on the supplied document.

```python
device = exp.create_device({ 'subtype': 'scala:device:player' })
```

**`exp.find_devices(params=None)`**

Returns a list of [devices](#devices) matching the given query parameters. `params` is a dictionary of query parameters.

**`exp.get_thing(uuid=None)`**

Returns the [thing](#thing) with the given uuid or `None` if no [thing](#things) could be found.

**`exp.create_thing(document=None)`**

Returns a [thing](#thing) created based on the supplied document.

```python
thing = exp.create_thing({ 'subtype': 'scala:thing:rfid', 'id': '[rfid]', 'name': 'my-rfid-tag' })
```

**`exp.find_things(params=None)`**

Returns a list of [things](#thing) matching the given query parameters. `params` is a dictionary of query parameters.

**`exp.get_experience(uuid=None)`**

Returns the [experience](#experience) with the given uuid or `None` if no [experience](#experience) could be found.

**`exp.create_experience(document=None)`**

Returns a [experience](#experience) created based on the supplied document.

**`exp.find_experiences(params=None)`**

Returns a list of [experiences](#experience) matching the given query parameters. `params` is a dictionary of query parameters.

**`exp.get_location(uuid=None)`**

Returns the [location](#location) with the given uuid or `None` if no [location](#location) could be found.

**`exp.create_location(document=None)`**

Returns a [location](#location) created based on the supplied document.

**`exp.find_locations(params=None)`**

Returns a list of [locations](#location) matching the given query parameters. `params` is a dictionary of query parameters.


**`exp.get_feed(uuid=None)`**

Returns the [feed](#feed) with the given uuid or `None` if no [feed](#feed) could be found.

**`exp.create_feed(document=None)`**

Returns a [feed](#feed) created based on the supplied document.

```python
feed = exp.create_feed({ 'subtype': 'scala:feed:weather', 'searchValue': '16902', 'name': 'My Weather Feed'  })
```

**`exp.find_feeds(params=None)`**

Returns a list of [feeds](#feed) matching the given query parameters. `params` is a dictionary of query parameters.

```python
feeds = exp.find_feeds({ 'subtype': 'scala:feed:facebook' })
```


**`exp.get_data(group='default', key=None)`**

Returns the [data item](#data) with the given group or key or `None` if the [data item] could not be found.

```python
data = exp.get_data('cats', 'fluffy')
```

**`exp.create_data(group='default', key=None, value=None)`**

Returns a [data item](#data) created based on the supplied group, key, and value.

```python
data = exp.create_data('cats', 'fluffy', { 'color': 'brown'})
```

**`exp.find_data(params=None)`**

Returns a list of [data items](#data) matching the given query parameters. `params` is a dictionary of query parameters.

```python
items = exp.find_data({ 'group': 'cats' })
```

**`exp.get_content(uuid=None)`**

Returns the [content item](#content) with the given uuid or `None` if no [content item](#content) could be found.

**`exp.find_content(params=None)`**

Returns a list of [content items](#content) matching the given query parameters. `params` is a dictionary of query parameters.


## Channel

**`channel.broadcast(name, payload=None, timeout=0.1)`**

Sends a [broadcast](#broadcast) on the channel with the given name and payload and returns a list of responses. `timeout` is the number of seconds to hold the request open to wait for responses.

```python
responses = channel.broadcast('hi!', { 'test': 'nice to meet you!' })
[print response for response in responses]
```

**`channel.listen(name, max_age=60)`**

Returns a [listener](#listener) for events on the channel. `max_age` is the number of seconds the listener will buffer events before they are discarded.

```python
channel = exp.get_channel('my-channel')
listener = channel.listen('my-event', max_age=30)
```

**`channel.fling(payload)`**

Fling an app launch payload on the channel.

```python
location = exp.get_location('[uuid]')
location.get_channel().fling({ 'appTemplate' : { 'uuid': '[uuid'} })
```


**`channel.identify()`**

Requests that [devices](#device) listening for this event on this channel visually identify themselves. Implementation is device specific; this is simply a convience method.

```python
location = exp.get_location('[uuid]')
location.get_channel().identify()  # Tell all devices at this location to identify themselves!
```

## Listener

**`listener.wait(timeout=0)`**

Wait for `timeout` seconds for broadcasts. Returns a [broadcast](#broadcast) if a [broadcast](#broadcast) is in the queue or if a [broadcast](#broadcast) is received before the timeout. If timeout is reached, returns `None`. 

```python
channel = exp.get_channel('my-channel')
listener = channel.listen('my-event')

while True:
  broadcast = listener.wait(60)
  if broadcast:
    print 'I got a broadcast!'

```

[Broadcasts](#broadcast) are returned in the order they are received.

**`listener.cancel()`**

Cancels the listener. The listener is unsubscribed from [broadcasts](#broadcast) and will no longer receive messages. This cannot be undone.

```python
listener.cancel()
broadcast = listener.wait(60)  # Will always be None
```

## Broadcast

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

## Resource

These methods and attributes are shared by many of the abstract API resources.

**`resource.uuid`**

The uuid of the resource. Cannot be set. Maps to `resource.document['uuid']`

**`resource.name`**

The name of the resource. Can be set directly. Maps to `resource.document['name']`.

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


## Device
Devices inherit all [common resource methods and attributes](#resource).

**`device.get_location()`**

Returns the device's [location](#location) or `None`.

**`device.get_zones()`**

Returns a list of the device's [zones](#zone).

**`device.get_experience()`**

Returns the device's [experience](#experience) or `None`


## Thing
Things inherit all [common resource methods and attributes](#resource).

**`thing.get_location()`**

Returns the thing's [location](#location) or `None`.

**`thing.get_zones()`**

Returns a list of the thing's [#zones](#zone).

**`thing.get_experience()`**

Returns the device's [experience](#experience) or `None`


### Experience
Experiences inherit all [common resource methods and attributes](#resource).

**`experience.get_devices()`**

Returns a list of [devices](#device) that are part of this experience.


## Location
Locations inherit all [common resource methods and attributes](#resource).

**`location.get_devices()`**

Returns a list of [devices](#device) that are part of this location.

**`location.get_things()`**

Returns a list of [devices](#device) that are part of this location.

**`location.get_zones()`**

Returns a list of [zones](#zone) that are part of this location.

**`location.get_layout_url()`**

Returns a url pointing to the location's layout image.


## Zone
Zones inherit the [common resource methods and attributes](#resource) `save()`, `refresh()`, and `get_channel()`.

**`zone.key`**

The zone's key.

**`zone.name`**

The zone's name.

**`zone.get_devices()`**

Returns all [devices](#device) that are members of this zone.

**`zone.get_things()`**

Returns all [things](#thing) that are members of this zone.

**`zone.get_location()`**

Returns the zone's [location](#location)


## Feed
Feeds inherit all [common resource methods and attributes](#resource).

**`feed.get_data()`**

Returns the feed's data.


## Data
Data items inherit the [common resource methods and attributes](#resource) `save()`, `refresh()`, and `get_channel()`.

**`data.key`**

The data item's key. Settable.

**`data.group`**

The data item's group. Settable

**`data.value`**

The data item's value. Settable.


## Content
Content items inherit all [common resource methods and attributes](#resource) except `save()`.

**`content.subtype`**

The content item's subtype. Not settable.

**`content.get_url()`**

Returns the delivery url for this content item.

**`content.has_variant(name)`**

Returns a boolean indicating whether or not this content item has a variant with the given name.

**`content.get_variant_url(name)`**

Returns the delivery url for a variant of this content item.





## Exceptions

 **`exp_sdk.ExpError`**
 
 Base class for all EXP exceptions.
 
 ---
 
 **`exp_sdk.UnexpectedError`**
 
 Raised when an unexpected error occurs.
 
 ---
 **`exp_sdk.RuntimeError`**
 
 Raised when [startup options](#runtime) are incorrect or inconsistent.
 
 ---
 **`exp_sdk.AuthenticationError`**
 
 Raised when the sdk cannot authenticate due to bad credentials.
 
 ---
 
 **`exp_sdk.ApiError`**
 
 Raised when an API call fails. Has properties `message` and `code`.



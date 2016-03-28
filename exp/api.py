import urllib
import requests
import traceback


class Resource (object):

  _collection_path = None

  def __init__ (self, document, sdk):
    self._document = document
    self._sdk = sdk

  def _get_channel_name (self):
    raise NotImplementedError

  def _get_resource_path (self):
    raise NotImplementedError

  @property
  def document (self):
    if not isinstance(self._document, dict):
      self._document = {}
    return self._document

  def save (self):
    self._document = self._sdk.api.patch(self._get_resource_path(), self.document)

  def refresh (self):
    self._document = self._sdk.api.get(self._get_resource_path())

  @classmethod
  def create (cls, document, sdk):
    return cls(sdk.api.post(cls._collection_path, document), sdk)

  @classmethod
  def find (cls, params, sdk):
    return [cls(document, sdk) for document in sdk.api.get(cls._collection_path, params)['results']]

  def get_channel(self, **kwargs):
    return self._sdk.network.get_channel(self._get_channel_name(), **kwargs)


class CommonResource (Resource):

  @property
  def uuid (self):
    return self.document['uuid']

  @property
  def name(self):
    return self.document['name']

  @name.setter
  def name (self, value):
    self.document['name'] = value

  def _get_channel_name (self):
    return self.uuid

  def _get_resource_path (self):
    return '{}/{}'.format(self._collection_path, self.uuid)

  @classmethod
  def get (cls, uuid, sdk):
    if not uuid or not isinstance(uuid, basestring):
      return None
    path = '{}/{}'.format(cls._collection_path, uuid)
    try:
      remote_document = sdk.api.get(path)
    except sdk.exceptions.ApiError as exception:
      if exception.status_code == 404:
        return None
      raise
    return cls(remote_document, sdk)


class GetLocationMixin (object):

  def _get_location_uuid (self):
    raise NotImplementedError

  def _get_zone_keys (self):
    raise NotImplementedError

  def get_location (self):
    uuid = self._get_location_uuid()
    if not uuid:
      return None
    return self._sdk.api.Location.get(uuid, self._sdk)

  def get_zones (self):
    location = self.get_location()
    if not location:
      return []
    keys = self._get_zone_keys()
    return [self._sdk.api.Zone(document, self, self._sdk) for document in location.document.get('zones', []) if document.get('key') in keys]


class GetExperienceMixin (object):

  def _get_experience_uuid (self):
    raise NotImplementedError

  def get_experience (self):
    uuid = self._get_experience_uuid()
    if not uuid:
      return None
    return self._sdk.api.Experience.get(uuid, self._sdk)


class GetDevicesMixin (object):

  def _get_device_query_params (self):
    raise NotImplementedError

  def get_devices (self):
    return self._sdk.api.Device.find(self._get_device_query_params(), self._sdk)


class GetThingsMixin (object):

  def _get_thing_query_params (self):
    raise NotImplementedError

  def get_things (self):
    return self._sdk.api.Thing.find(self._get_thing_query_params(), self._sdk)


class Device (CommonResource, GetLocationMixin, GetExperienceMixin):

  _collection_path = '/api/devices'

  def _get_experience_uuid (self):
    return self.document.get('experience', {}).get('uuid')

  def _get_location_uuid (self):
    return self.document.get('location', {}).get('uuid')

  def _get_zone_keys (self):
    return [document.get('key') for document in self.document.get('location', {}).get('zones', []) if document.get('key')]


class Thing (CommonResource, GetLocationMixin):

  _collection_path = '/api/things'

  def _get_location_uuid (self):
    return self.document.get('location', {}).get('uuid')

  def _get_zone_keys (self):
    return [document.get('key') for document in self.document.get('location', {}).get('zones', []) if document.get('key')]


class Experience (CommonResource, GetDevicesMixin):

  _collection_path = '/api/experiences'

  def _get_device_query_params (self):
    return { 'experience.uuid' : self.uuid }


class Location (CommonResource, GetDevicesMixin, GetThingsMixin):

  _collection_path = '/api/locations'

  def _get_device_query_params (self):
    return { 'location.uuid' : self.uuid }

  def _get_thing_query_params (self):
    return { 'location.uuid': self.uuid }

  def get_zones (self):
    return [self._sdk.api.Zone(document, self, self._sdk) for document in self.document.get('zones', [])]

  def get_layout_url (self):
    return self._get_resource_path() + '/layout?_rt=' + self._sdk.authenticator.get_auth()['restrictedToken']


class Feed (CommonResource):

  _collection_path = '/api/connectors/feeds'

  def get_data (self):
    return self._sdk.api.get(self._get_resource_path() + '/data')


class Zone (Resource, GetDevicesMixin, GetThingsMixin):

  def __init__ (self, document, location, sdk):
    super(Zone, self).__init__(document, sdk)
    self._location = location

  @property
  def key(self):
    return self.document.get('key')

  def _get_device_query_params (self):
    return { 'location.uuid': self._location.uuid, 'location.zones.key': self.key }

  def _get_thing_query_params (self):
    return { 'location.uuid': self._location.uuid, 'location.zones.key': self.key }

  def save (self):
    return self._location.save()

  def refresh (self):
    self._location.refresh()
    matches = [document for document in self._location.document.get('zones', []) if self.key == document['key']]
    if matches:
      self._document = matches[0]

  def get_location (self):
    return self._location

  def _get_channel_name(self):
    return self._location.uuid + ':zone:' + self.key




class Data (Resource):

  _collection_path = '/api/data'

  @property
  def group(self):
    return self.document.get('group')

  @property
  def key(self):
    return self.document.get('key')

  @property
  def value (self):
    return self.document.get('value')

  @value.setter
  def value(self, value):
    self.document['value'] = value

  def _get_resource_path(self):
    return '{}/{}/{}'.format(self._collection_path, self.group, self.key)

  @classmethod
  def get (cls, group, key, sdk):
    path = '{}/{}/{}'.format(cls._collection_path, group, key)
    try:
      document = sdk.api.get(path)
    except sdk.exceptions.ApiError as exception:
      if exception.status_code == 404:
        return None
      raise
    return cls(document, sdk)

  @classmethod
  def create (cls, group, key, value, sdk):
    path = '{}/{}/{}'.format(cls._collection_path, group, key)
    document = sdk.api.put(path, value)
    return cls(document, sdk)

  def save (self):
    a = self._sdk.api.put(self._get_resource_path(), self.value)
    print 'qweqewwqe'
    print a

  def _get_channel_name (self):
    return 'data:{}:{}'.format(self.group, self.key)




class Content (CommonResource):

  _collection_path = '/api/content'

  def get_children (self):
    if self._children is None:
      if self.document['children']:
        return [self.__class__(document, self._sdk) for document in self.document['children']]
      else:
        self.refresh()
        return self.get_children()
    return []

  def get_subtype (self):
    return self.document['subtype']

  def get_url (self):
    auth = self._sdk.authenticator.get_auth()
    delivery_url = auth['api']['host'] + '/api/delivery'
    rt_string = '?_rt=' + auth['restrictedToken']
    if self.get_subtype() == 'scala:content:file':
      return delivery_url + self._get_resource_path(self.document, self._sdk) + rt_string
    elif self.get_subtype() == 'scala:content:app':
      return delivery_url + self._get_resource_path(self.document, self._sdk) + rt_string
    elif self.get_subtype() == 'scala:content:url':
      return self.document['url']

  def get_variant_url (self, name):
    auth = self._sdk.authenticator.get_auth()
    delivery_url = auth['api']['host'] + '/api/delivery'
    rt_string = '?_rt=' + auth['restrictedToken']
    if self.get_subtype() == 'scala:content:file' and self.has_variant(name):
      return delivery_url + '?variant=' + urllib.quote(name) + rt_string

  def has_variant (self, name):
    return name in self.document.get('variants', [])



class Api (object):

  Device = Device
  Thing = Thing
  Experience = Experience
  Location = Location
  Zone = Zone
  Feed = Feed
  Data = Data
  Content = Content

  def __init__(self, sdk):
    self._sdk = sdk

  def _get_url (self, path):
    return '{0}{1}'.format(self._sdk.authenticator.get_auth()['api']['host'], urllib.quote(path))

  def _get_headers (self):
    return { 'Authorization': 'Bearer ' + self._sdk.authenticator.get_auth()['token'] }

  def _on_error(self, exception):
    if hasattr(exception, 'response'):
      try:
        payload = exception.response.json()
      except:
        self._sdk.logger.warn('API call encountered an unexpected error.')
        self._sdk.logger.debug('API call encountered an unexpected error: %s' % traceback.format_exc())
        raise self._sdk.exceptions.UnexpectedError('API call encountered an unexpected error.')
      else:
        raise self._sdk.exceptions.ApiError(code=payload.get('code'), message=payload.get('message'), status_code=exception.response.status_code)
    else:
      self._sdk.logger.warn('API call encountered an unexpected error.')
      self._sdk.logger.debug('API call encountered an unexpected error: %s' % traceback.format_exc())
      raise self._sdk.exceptions.UnexpectedError('API call encountered an unexpected error.')


  def get(self, path, params=None, timeout=10):
    try:
      response = requests.get(self._get_url(path), timeout=timeout, params=params, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def post(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.post(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def patch(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.patch(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def put(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.put(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

  def delete(self, path, payload=None, params=None, timeout=10):
    try:
      response = requests.delete(self._get_url(path), timeout=timeout, params=params, json=payload, headers=self._get_headers())
      response.raise_for_status()
      try:
        return response.json()
      except ValueError:
        return None
    except Exception as exception:
      return self._on_error(exception)

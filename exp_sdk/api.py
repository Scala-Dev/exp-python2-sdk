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
    return Collection(cls, sdk.api.get(cls._collection_path, params), sdk)

  def get_channel(self, **kwargs):
    return self._sdk.network.get_channel(self._get_channel_name(), **kwargs)


class Collection (list):

  def __init__(self, Resource, document, sdk):
    list.__init__(self, [Resource(doc, sdk) for doc in document['results']])
    for key, value in document.iteritems():
      self.__dict__[key] = value

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
    return '{0}/{1}'.format(self._collection_path, self.uuid)

  @classmethod
  def delete_ (cls, uuid, sdk):
    if not uuid or not isinstance(uuid, basestring):
      return None
    path = '{0}/{1}'.format(cls._collection_path, uuid)
    return sdk.api.delete(path)

  def delete (self):
    return self._sdk.api.delete(self._get_resource_path())

  @classmethod
  def get (cls, uuid, sdk):
    if not uuid or not isinstance(uuid, basestring):
      return None
    path = '{0}/{1}'.format(cls._collection_path, uuid)
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

  def get_devices (self, params=None):
    return self._sdk.api.Device.find(self._get_device_query_params(params), self._sdk)


class GetThingsMixin (object):

  def _get_thing_query_params (self):
    raise NotImplementedError

  def get_things (self, params=None):
    return self._sdk.api.Thing.find(self._get_thing_query_params(params), self._sdk)


class Device (CommonResource, GetLocationMixin, GetExperienceMixin):

  _collection_path = '/api/devices'

  def _get_experience_uuid (self):
    return self.document.get('experience', {}).get('uuid')

  def _get_location_uuid (self):
    return self.document.get('location', {}).get('uuid')

  def _get_zone_keys (self):
    return [document.get('key') for document in self.document.get('location', {}).get('zones', []) if document.get('key')]

  @classmethod
  def get_current (cls, sdk):
    auth = sdk.authenticator.get_auth()
    if not auth or not auth['identity']['type'] == 'device':
      return None
    return cls.get(auth['identity']['uuid'], sdk)


class Thing (CommonResource, GetLocationMixin):

  _collection_path = '/api/things'

  def _get_location_uuid (self):
    return self.document.get('location', {}).get('uuid')

  def _get_zone_keys (self):
    return [document.get('key') for document in self.document.get('location', {}).get('zones', []) if document.get('key')]


class Experience (CommonResource, GetDevicesMixin):

  _collection_path = '/api/experiences'

  def _get_device_query_params (self, params):
    params = params or {}
    params['experience.uuid'] = self.uuid

  @classmethod
  def get_current (cls, sdk):
    device = Device.get_current(sdk)
    return device.get_experience() if device else None


class Location (CommonResource, GetDevicesMixin, GetThingsMixin):

  _collection_path = '/api/locations'

  def _get_device_query_params (self, params=None):
    params = params or {}
    params['location.uuid'] = self.uuid

  def _get_thing_query_params (self, params=None):
    params = params or {}
    params['location.uuid'] = self.uuid

  def get_zones (self):
    return [self._sdk.api.Zone(document, self, self._sdk) for document in self.document.get('zones', [])]

  def get_layout_url (self):
    return self._get_resource_path() + '/layout?_rt=' + self._sdk.authenticator.get_auth()['restrictedToken']

  @classmethod
  def get_current(cls, sdk):
    device = Device.get_current(sdk)
    return device.get_location() if device else None


class Feed (CommonResource):

  _collection_path = '/api/connectors/feeds'

  def get_data (self, **params):
    return self._sdk.api.get(self._get_resource_path() + '/data', params=params)


class Zone (Resource, GetDevicesMixin, GetThingsMixin):

  def __init__ (self, document, location, sdk):
    super(Zone, self).__init__(document, sdk)
    self._location = location

  @property
  def key(self):
    return self.document['key']

  @property
  def name(self):
    return self.document['name']

  @name.setter
  def name (self, value):
    self.document['name'] = value

  def _get_device_query_params (self, params=None):
    params = params or {}
    params['location.uuid'] = self._location.uuid
    params['location.zones.key'] = self.key
    return params

  def _get_thing_query_params (self, params=None):
    params = params or {}
    params['location.uuid'] = self._location.uuid
    params['location.zones.key'] = self.key
    return params

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

  @classmethod
  def get_current(cls, sdk):
    device = Device.get_current(sdk)
    return device.get_zones() if device else []


class Data (Resource):

  _collection_path = '/api/data'

  @property
  def group(self):
    return self.document.get('group')

  @group.setter
  def group (self, value):
    self.document['group'] = value

  @property
  def key(self):
    return self.document.get('key')

  @key.setter
  def key (self, value):
    self.document['key'] = value

  @property
  def value (self):
    return self.document.get('value')

  @value.setter
  def value(self, value):
    self.document['value'] = value

  def _get_resource_path(self):
    return '{0}/{1}/{2}'.format(self._collection_path, self.group, self.key)

  @classmethod
  def get (cls, group, key, sdk):
    path = '{0}/{1}/{2}'.format(cls._collection_path, group, key)
    try:
      document = sdk.api.get(path)
    except sdk.exceptions.ApiError as exception:
      if exception.status_code == 404:
        return None
      raise
    return cls(document, sdk)

  @classmethod
  def create (cls, group, key, value, sdk):
    path = '{0}/{1}/{2}'.format(cls._collection_path, group, key)
    document = sdk.api.put(path, value)
    data = cls(document, sdk)
    return data

  def save (self):
    self._document = self._sdk.api.put(self._get_resource_path(), self.value)

  def _get_channel_name (self):
    return 'data:{0}:{1}'.format(self.group, self.key)

  @classmethod
  def delete_ (cls, group, key, sdk):
    path = '{0}/{1}/{2}'.format(cls._collection_path, group, key)
    sdk.api.delete(path)

  def delete (self):
    self._sdk.api.delete(self._get_resource_path())


class Content (CommonResource):

  _collection_path = '/api/content'

  def save (self):
    raise NotImplementedError

  @property
  def subtype(self):
      return self.document.get('subtype')

  def get_children (self, params=None):
    params = params or {}
    params['parent'] = self.uuid
    return Collection(self.__class__, self._sdk.api.get(self._collection_path, params), self._sdk)

  def _get_delivery_url (self):
    auth = self._sdk.authenticator.get_auth()
    base = '{0}/api/delivery'.format(auth['api']['host'])
    encoded_path = urllib.quote(self.document.get('path'))
    return '{0}/{1}?_rt={2}'.format(base, encoded_path, auth['restrictedToken'])

  def get_url (self):
    if self.subtype == 'scala:content:file':
      return self._get_delivery_url()
    elif self.subtype == 'scala:content:app':
      return self._get_delivery_url()
    elif self.subtype == 'scala:content:url':
      return self.document.get('url')

  def get_variant_url (self, name):
    return '{0}&variant='.format(self._get_delivery_url(), name)

  def has_variant (self, name):
    return name in [variant['name'] for variant in self.document.get('variants', [])]



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
        raise self._sdk.exceptions.ApiError(code=payload.get('code'), message=payload.get('message'), status_code=exception.response.status_code, payload=payload)
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

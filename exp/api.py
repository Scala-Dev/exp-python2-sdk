import urllib
import requests
import traceback

class Resource (object):

  _collection_path = None

  def __init__ (self, document, sdk):
    self.document = document
    self._sdk = sdk

  @classmethod
  def _get_resource_path_static (cls, uuid):
    return cls._collection_path + '/' + uuid

  def _get_resource_path (self):
    return self._get_resource_path_static(self.document['uuid'])

  def _get_channel_name (self):
    return self.document['uuid']

  @classmethod
  def get (cls, uuid, sdk):
    if not isinstance(uuid, basestring):
      return None
    try:
      document = sdk.api.get(cls._get_resource_path_static(uuid))
    except sdk.exceptions.ApiError as exception:
      if exception.status_code == 404:
        return None
      raise
    return cls(document, sdk)

  @classmethod
  def create (cls, document, sdk):
    return cls(sdk.api.post(cls._collection_path, document), sdk)

  @classmethod
  def find (cls, params, sdk):
    if params and not isinstance(params, dict):
      return []
    return [cls(document, sdk) for document in sdk.api.get(cls._collection_path, params)['results']]

  def save (self):
    self.document = self._sdk.api.patch(self._get_resource_path(), self.document)

  def refresh (self):
    self.document = self._sdk.api.get(self._get_resource_path())

  def get_channel(self, **kwargs):
    return self._sdk.network.get_channel(self._get_channel_name(), **kwargs)

class UuidMixin (object):

  @property
  def uuid (self):
    return self.document.get('uuid')

  @property
  def name (self):
    return self.document.get('name')

  @name.setter
  def name (self, value):
    self.document['name'] = value


class DeviceThingBase(Resource):

  def get_location (self):
    uuid = self.document.get('location', {}).get('uuid')
    if not uuid:
      return None
    return self._sdk.api.Location.get(uuid, self._sdk)

  def get_zones (self):
    location = self.get_location()
    if not location:
      return []
    keys = [document['key'] for document in self.document.get('location', {}).get('zones', [])]
    zones = [self._sdk.api.Zone(document, self, self._sdk) for document in location.document['zones'] if document.key in keys]


class Device (DeviceThingBase, UuidMixin):

  _collection_path = '/api/devices'

  def get_experience (self):
    uuid = self.document.get('experience', {}).get('uuid')
    if not uuid:
      return None
    return self._sdk.api.Experience.get(uuid, self._sdk)

  def identify (self):
    return self.get_channel().broadcast('identify')


class Thing (DeviceThingBase):

  _collection_path = '/api/things'


class Experience (Resource):

  _collection_path = '/api/experiences'

  def get_devices (self):
    return self._sdk.api.Device.find({ 'experience.uuid' : self.document.get('uuid') })


class Location (Resource):

  _collection_path = '/api/locations'

  def get_devices (self):
    return self._sdk.api.Device.find({ 'location.uuid': self.document.get('uuid') })

  def get_things (self):
    return self._sdk.api.Thing.find({ 'location.uuid': self.document.get('uuid') })

  def get_zones (self):
    return [self._sdk.api.Zone(document, self, self._sdk) for document in self.document.get('zones', [])]

  def get_layout_url (self):
    return self._get_resource_path(self.document, self._sdk) + '/layout?_rt=' + self._sdk.authenticator.get_auth()['restrictedToken']


class Zone (Resource):

  def __init__ (self, document, location, sdk):
    super(Zone, self).__init__(document, sdk)
    self._location = location

  def save (self):
    return self._location.save()

  def refresh (self):
    self._location = self._location.refresh()
    self._document = [document for document in self._location.document.get('zones') if document['key'] == self.document['key']]

  def get_location (self):
    return self._location

  def get_devices (self):
    return self._sdk.api.Device.find({ 'location.uuid': self._location.document['uuid'], 'location.zones.key': self.document['key'] })

  def get_things (self):
    return self._sdk.api.Thing.find({ 'location.uuid': self._location.document['uuid'], 'location.zones.key': self.document['key'] })

  @classmethod
  def get_channel_name(cls, document, sdk):
    return self._location.document['uuid'] + ':zone:' + self.document['key']


class Feed (Resource):

  _collection_path = '/api/connectors/feeds'

  def get_data (self):
    return self._sdk.api.get(self._get_resource_path(self.document, self._sdk) + '/data')


class Data (Resource):

  _collection_path = '/api/data'

  @classmethod
  def _get_resource_path(cls, document, sdk):
    return cls._collection_path + '/' + urllib.quote(document['group']) + '/' + urllib.quote(document['key'])

  @classmethod
  def get (cls, document, sdk):
    document['group'] = document.get('group', 'default')
    document_ = sdk.api.get(self._get_resource_path(document, sdk))
    if not document_:
      document_ = { 'key': document['key'], 'group': document['group'], 'value': None }
    return cls(document, sdk)

  @property
  def value (self):
    return self.document.get('value', None)

  @value.setter
  def value(self, value):
    self.document['value'] = value

  @classmethod
  def create (cls, document, sdk):
    data = cls(document, sdk)
    data.save()
    return data

  def save (self):
    self.document = self._sdk.api.put(self._get_resource_path(self.document, self._sdk), self.document)

  def _get_channel_name (self):
    return 'data' + ':' + self.document['key'] + ':' + self.document['group']


class Content (Resource):

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

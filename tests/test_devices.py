
import unittest

from . import utils


class TestDevicesGet(utils.Device, unittest.TestCase):

  def test_get (self):
    if not isinstance(self.exp.get_device(self.device_credentials['uuid']), self.exp._sdk.api.Device):
      raise Exception

  def test_get_with_invalid_uuid (self):
    if self.exp.get_device('not a device uuid') is not None:
      raise Exception

  def test_get_none (self):
    if self.exp.get_device(None) is not None:
      raise Exception

  def test_get_empty (self):
    if self.exp.get_device() is not None:
      raise Exception

  def test_get_wrong_type (self):
    if self.exp.get_device({}) is not None:
      raise Exception


class TestDevicesFind(utils.Device, unittest.TestCase):

  def test_find_without_params (self):
    devices = self.exp.find_devices()
    for device in devices:
      if not isinstance(device, self.exp._sdk.api.Device):
        raise Exception

  def test_find_with_params (self):
    devices = self.exp.find_devices({ 'uuid': self.device_credentials['uuid'] })
    if len(devices) != 1:
      raise Exception
    if not isinstance(devices[0], self.exp._sdk.api.Device):
      raise Exception

  def test_find_with_wrong_type (self):
    devices = self.exp.find_devices('test')
    if not isinstance(devices, list) or devices:
      raise Exception


class TestCreate(utils.Device, unittest.TestCase):

  def test_create_with_subtype (self):
    device = self.exp.create_device({ 'subtype' : 'scala:device:player' })
    if not isinstance(device, self.exp._sdk.api.Device):
      raise Exception
    if not self.exp.get_device(device.document['uuid']):
      raise Exception

  def test_create_empty (self):
    device = self.exp.create_device()
    if not isinstance(device, self.exp._sdk.api.Device):
      raise Exception
    if not self.exp.get_device(device.document['uuid']):
      raise Exception

  def test_create_none (self):
    device = self.exp.create_device(None)
    if not isinstance(device, self.exp._sdk.api.Device):
      raise Exception
    if not self.exp.get_device(device.document['uuid']):
      raise Exception


class TestSave(utils.Device, unittest.TestCase):

  def test_save (self):
    name = self.generate_name()
    device1 = self.exp.create_device()
    device1.name = name
    device1.save()
    device2 = self.exp.get_device(device1.uuid)
    if device2.name != name:
      raise Exception

class TestRefresh (utils.Device, unittest.TestCase):

  def test_refresh (self):
    name = self.generate_name()
    device1 = self.exp.create_device()
    device2 = self.exp.get_device(device1.uuid)
    device2.name = name
    device2.save()
    device1.refresh()
    if device1.name != name:
      raise Exception


class TestGettersAndSetters (utils.Device, unittest.TestCase):

  def test_uuid_getter (self):
    device = self.exp.create_device()
    if device.uuid is None:
      raise Exception

  def test_name_getter_setter (self):
    name = self.generate_name()
    device = self.exp.create_device()
    device.name = name
    if device.name != name:
      raise Exception
    if self.document['name'] != name:
      raise Exception



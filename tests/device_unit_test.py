
import unittest


from exp.api import Device, QueryResult
import exp.api_utils

class TestException (Exception): pass


class TestDeviceFind (unittest.TestCase):

  mock = {
    'total': 2,
    'results': [
      { 'name': 'device 1', 'uuid': 'fake uuid 1' },
      { 'name': 'device 2', 'uuid': 'fake uuid 2' }
    ]
  }

  def api_utils_get_mock (self, path, params=None):
    if path != '/api/devices':
      raise Exception()
    return self.mock

  def raise_exception (self):
    raise TestException()

  def tearDown (self):
    exp.api_utils.get = self.original_api_utils_get

  def setUp (self):
    self.original_api_utils_get = exp.api_utils.get

  def test_error_passthrough (self):
    exp.api_utils.get = lambda *args, **kwargs: self.raise_exception()
    try:
      exp.find_devices()
    except TestException:
      pass
    else:
      raise Exception()

  def test (self):
    exp.api_utils.get = lambda *args, **kwargs: self.api_utils_get_mock(*args, **kwargs)
    devices = exp.find_devices()
    for device in devices:
      if not isinstance(device, Device):
        raise Exception

  def test_results_length (self):
    devices = exp.find_devices()
    if len(devices) != 
    pass

  def test_results_type (self):
    pass

  def test_results_document (self):
    pass







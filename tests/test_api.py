import utils
import random
import string

class Test (utils.Device):

  def test_get (self):
    self.exp.get('/api/devices/' + self.device_credentials.get('uuid'))

  def test_post (self):
    self.exp.post('/api/experiences', {})

  def test_patch (self):
    document = self.exp.post('/api/experiences', {})
    self.exp.patch('/api/experiences/' + document['uuid'], {})

  def test_put (self):
    self.exp.put('/api/data/test1/test2', { 'a': 1 })

  def test_delete (self):
    document = self.exp.post('/api/experiences', {})
    self.exp.delete('/api/experiences/' + document['uuid'])

  def test_post_error (self):
    name = ''.join(random.choice(string.lowercase) for i in range(10))
    self.exp.post('/api/experiences', { 'name': name })
    try:
      self.exp.post('/api/experiences', { 'name': name })
    except self.exp_sdk.ApiError:
      pass
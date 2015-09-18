import unittest
import scala

class TestThatTestingWorks(unittest.TestCase):

  def test_something(self):
    self.assertEqual(0, 0)

  def test_something_else(self):
    self.assertEqual(0, 0)


if __name__ == '__main__':
  unittest.main()

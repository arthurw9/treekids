import unittest
import os

import config

class TestConfig(unittest.TestCase):

  def test_CreateIfNotExists(self):
    config.CreateIfNotExists()
    self.assertTrue(os.path.exists('config.json'))

  def test_GetConfig(self):
    c = config.GetConfig()
    self.assertTrue(isinstance(c, dict))
    self.assertTrue('SECRET_KEY' in c)

if __name__ == '__main__':
  unittest.main()

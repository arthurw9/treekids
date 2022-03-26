import flask_app
import unittest

class TestFlaskApp(unittest.TestCase):

  def test_Foo(self):
    client = flask_app.app.test_client()
    response = client.get("/")
    self.assertEqual("200 OK", response.status)
    self.assertEqual(3, len(response.data.split(b"TreeKids")),
                     "Expected TreeKids to appear twice in the response.")


if __name__ == '__main__':
  unittest.main()


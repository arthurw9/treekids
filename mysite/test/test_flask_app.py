import flask_app
import auth
import unittest

class TestFlaskApp(unittest.TestCase):

  def test_home_page_displays(self):
    client = flask_app.app.test_client()
    response = client.get("/")
    self.assertEqual("200 OK", response.status)
    self.assertIn(b"<title>TreeKids</title>", response.data)
    self.assertIn(b"""<a href="/login">login</a>""", response.data)
    self.assertIn(b"""<p>Home page!""", response.data)

  def test_login_page_displays(self):
    client = flask_app.app.test_client()
    response = client.get("/login")
    self.assertEqual("200 OK", response.status)
    self.assertIn(b"<title>TreeKids</title>", response.data)
    self.assertIn(b"""<input type="text" name="username" """, response.data)
    self.assertIn(b"""<input type="password" name="password" """, response.data)
    self.assertIn(b"""<input type="submit" value="Login">""", response.data)

  def test_can_login(self):
    client = flask_app.app.test_client()
    with client:
      response = client.post("/login", data={
         "username": "arthur",
         "password": "",
         "submit": "submit"})
      self.assertEqual("302 FOUND", response.status)
      self.assertIn(b"""redirected automatically to target URL: <a href="/">""",
         response.data)
      response = client.get("/")
      self.assertEqual("200 OK", response.status)
      self.assertIn(b"""Hello arthur<br><a href="/logout">logout</a>""",
         response.data)
      self.assertEqual(auth.Username(), "arthur")
      self.assertEqual(auth.LoggedIn(), True)
      self.assertEqual(auth.IsInternal(), True)

  def test_can_logout(self):
    client = flask_app.app.test_client()
    with client:
      response = client.post("/login", data={
         "username": "arthur",
         "password": "",
         "submit": "submit"})
      response = client.get("/")
      self.assertEqual("200 OK", response.status)
      self.assertIn(b"""Hello arthur<br><a href="/logout">logout</a>""",
         response.data)
      self.assertEqual(auth.Username(), "arthur")
      self.assertEqual(auth.LoggedIn(), True)
      self.assertEqual(auth.IsInternal(), True)
      response = client.get("/logout")
      self.assertEqual("302 FOUND", response.status)
      self.assertIn(b"""redirected automatically to target URL: <a href="/">""",
         response.data)
      response = client.get("/")
      self.assertEqual("200 OK", response.status)
      self.assertIn(b"""<a href="/login">login</a>""", response.data)
      self.assertIn(b"""<p>Home page!""", response.data)
      self.assertEqual(auth.LoggedIn(), False)
      self.assertEqual(auth.Username(), None)
      self.assertEqual(auth.IsInternal(), False)
      
if __name__ == '__main__':
  unittest.main()


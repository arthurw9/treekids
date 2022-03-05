import flask
import maintenance

def CheckLogin():
  # TODO: Check the password
  flask.session['username'] = flask.request.form['username'].lower()
  flask.session['logged_in'] = 'true'

def Logout():
  flask.session.pop('username', None)
  flask.session.pop('logged_in', None)

def IsInternal():
  if not 'username' in flask.session:
    return False
  user = flask.session['username']
  if user in ["arthur", "edmundo", "justo"]:
    return True
  rows = maintenance.query(user)
  for r in rows:
    if r[0] != user:
      continue
    if r[2] == "ics_user":
      return True
  return False

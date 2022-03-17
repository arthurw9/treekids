import flask
import maintenance

def Username():
  if LoggedIn():
    return flask.session['username']
  return None

def CheckLogin():
  # TODO: Check the password
  username = flask.request.form['username'].lower()
  if not username:
    return
  flask.session['username'] = username
  flask.session['logged_in'] = True
  if IsInternal():
    flask.session['is_internal'] = True

def Logout():
  flask.session.pop('username', None)
  flask.session.pop('logged_in', None)
  flask.session.pop('is_internal', None)

def IsInternal():
  if not LoggedIn():
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

def LoggedIn():
  return 'logged_in' in flask.session


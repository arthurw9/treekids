import sqlite3
import flask
import db_utils

app = flask.Flask(__name__)

def init_db():
  with app.app_context():
    db = db_utils.get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def query_users(user_query):
  with app.app_context():
    db = db_utils.get_db()
    if user_query:
      cur = db.execute("select username, relationship, other " +
                       "from role where username = ?", [user_query])
    else:
      cur = db.execute("select username, relationship, other from role")
    rv = cur.fetchall()
    cur.close()
  return rv

def new_user(form):
  username = form['username']
  relationship = ""
  other = "ics_user"
  with app.app_context():
    db = db_utils.get_db()
    db.cursor().execute("insert into role(username, relationship, other) " +
                        "values(?, ?, ?)", [username, relationship, other])
    db.commit()

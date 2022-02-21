import sqlite3
import flask

app = flask.Flask(__name__)
DATABASE = 'db.db'

def get_db():
  db = getattr(flask.g, '_database', None)
  if db is None:
    flask.g._database = sqlite3.connect(DATABASE)
    db = flask.g._database
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(flask.g, '_database', None)
  if db is not None:
    db.close()

def init_db():
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()


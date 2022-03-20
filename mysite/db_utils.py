import sqlite3
import flask

DATABASE = 'db.db'

def get_db():
  db = getattr(flask.g, '_database', None)
  if db is None:
    flask.g._database = sqlite3.connect(DATABASE)
    db = flask.g._database
  return db

def close_connection(exception):
  db = getattr(flask.g, '_database', None)
  if db:
    flask.g.pop('_database')
    db.close()


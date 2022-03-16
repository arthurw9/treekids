import sqlite3
import flask
import db_utils
import time

app = flask.Flask("TreeKids")

def record_question(question):
  ts = int(time.time())
  username = flask.session['username']
  app.logger.info("Question %s, %s" % (username, question))
  with app.app_context():
    db = db_utils.get_db()
    db.cursor().execute("insert into questions(username, question, ts) " +
                        "values(?, ?, ?)", [username, question, ts])
    db.commit()

def record_answer(question, answer):
  ts = int(time.time())
  username = flask.session['username']
  app.logger.info("Answer %s, %s, %s" % (username, question, answer))
  with app.app_context():
    db = db_utils.get_db()
    db.cursor().execute("insert into answers(username, question, answer, ts) " +
                        "values(?, ?, ?, ?)", [username, question, answer, ts])
    db.commit()



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

def query_answers(user_query):
  with app.app_context():
    db = db_utils.get_db()
    sql_query = """select q.username, a.ts - q.ts, q.question, a.answer
                   from questions q left join answers a 
                   on a.username = q.username and q.question = a.question """
    if user_query:
      cur = db.execute(sql_query + "where q.username = ? order by 3, 2", [user_query])
    else:
      cur = db.execute(sql_query + "order by 1, 3, 2")
    rv = cur.fetchall()
    cur.close()
    app.logger.info(str(rv))
  return rv


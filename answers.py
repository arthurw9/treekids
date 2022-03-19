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
    db.cursor().execute("insert into answers(username, ts, question, question_only) " +
                        "values(?, ?, ?, ?)", [username, ts, question, "Ques"])
    db.commit()

def record_answer(question, answer):
  ts = int(time.time())
  username = flask.session['username']
  app.logger.info("Answer %s, %s, %s" % (username, question, answer))
  with app.app_context():
    db = db_utils.get_db()
    db.cursor().execute("insert into answers(username, ts, question, question_only, answer) " +
                        "values(?, ?, ?, ?, ?)", [username, ts, question, "Ans", answer])
    db.commit()

def query_answers(user_query):
  with app.app_context():
    db = db_utils.get_db()
    sql_query = """select ts, username, question_only, question, answer
                   from answers a """
    if user_query:
      cur = db.execute(sql_query + "where username = ? order by 1", [user_query])
    else:
      cur = db.execute(sql_query + "order by 1, 2")
    rows = cur.fetchall()
    cur.close()
  rows.insert(0, ["timestamp", "username", "Q-vs-A", "question", "answer"])
  return rows


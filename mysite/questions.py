import sqlite3
import flask
import db_utils
import json
import flask

def save(form):
  # Decide if we are deleting, inserting or updating a question
  if 'save_problem_button' in form:
    if int(form['question_id']) > 0:
      update(form)
      return
    insert(form)
    return
  if 'delete_button' in form:
    delete(form)
    return
  raise Exception("huh?")

def edit(question_id):
  with flask.current_app.app_context():
    db = db_utils.get_db()
    sql_query = """
      select question_id, username, question, correct_answer, wrong_answers
      from questions q where question_id = ?
    """
    cur = db.execute(sql_query, [question_id])
    rows = cur.fetchall()
    cur.close()
  if not rows:
    return flask.render_template('build.html', question_id=-1)
  row = rows[0]
  if row[1] != flask.session['username']:
    # if the user doesn't match then silently copy the question to a new one.
    question_id = -1
  question = row[2]
  correct = row[3]
  wrong_options = json.loads(row[4])
  return flask.render_template('build.html', question_id=question_id,
    question=question, correct=correct, wrong_options=wrong_options)

def delete(form):
  username = flask.session['username']
  question_id = form['question_id']
  with flask.current_app.app_context():
    db = db_utils.get_db()
    db.cursor().execute("""
        delete from questions where question_id = ? and username = ?""",
      [question_id, username])
    db.commit()

def update(form):
  # todo prevent users from updating other's questions.
  username = flask.session['username']
  question_id = form['question_id']
  question = form['question']
  correct_answer = form['correct']
  num_choices = form['num_choices']
  wrong_answers = []
  for opt in form:
    if opt[:6] == "option":
      wrong_answers.append(form[opt])
  with flask.current_app.app_context():
    db = db_utils.get_db()
    db.cursor().execute("""
       replace into questions(
         question_id, username, question, correct_answer, wrong_answers)
       values(?, ?, ?, ?, ?)""",
       [question_id, username, question, correct_answer, json.dumps(wrong_answers)])
    db.commit()

def insert(form):
  username = flask.session['username']
  question_id = form['question_id']
  question = form['question']
  correct_answer = form['correct']
  num_choices = form['num_choices']
  wrong_answers = []
  for opt in form:
    if opt[:6] == "option":
      wrong_answers.append(form[opt])
  with flask.current_app.app_context():
    db = db_utils.get_db()
    db.cursor().execute("""
       insert into questions(
         username, question, correct_answer, wrong_answers)
       values(?, ?, ?, ?)""",
       [username, question, correct_answer, json.dumps(wrong_answers)])
    db.commit()

def query(query=""):
  with flask.current_app.app_context():
    db = db_utils.get_db()
    sql_query = """select question_id, username, question, correct_answer, wrong_answers
                   from questions q """
    if query:
      cur = db.execute(sql_query + "where username = ? order by 1", [query])
    else:
      cur = db.execute(sql_query + "order by 1, 2")
    rows = cur.fetchall()
    cur.close()
  rows.insert(0, ["question_id", "username", "question", "answer", "wrong_answers"])
  return rows


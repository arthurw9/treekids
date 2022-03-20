import flask
import json
import random
# from flask import Flask, escape, request, render_template

import auth
import maintenance
import config
import answers

app = flask.Flask(__name__)
config.LoadConfig(app)

@app.route('/ics', methods=['GET', 'POST'])
def ics_page():
  if not auth.IsInternal():
    return flask.redirect(flask.url_for("login_page"))
  rows = []
  if flask.request.method == 'POST':
    if "initdb_button" in flask.request.form:
      maintenance.init_db()
    if "new_ics_user_button" in flask.request.form:
      maintenance.new_user(flask.request.form)
    if "users_button" in flask.request.form:
      user_query = flask.request.form["user_query"]
      rows = maintenance.query_users(user_query)
    if "answers_time_button" in flask.request.form:
      user_query = flask.request.form["user_query"]
      rows = answers.query_answers(user_query)

  return flask.render_template('ics.html', rows=rows)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
  if flask.request.method == 'POST':
    auth.CheckLogin()
    return flask.redirect("/")
  return flask.render_template('login.html')

@app.route('/logout')
def logout():
  auth.Logout()
  return flask.redirect("/")

@app.route('/index.html')
@app.route('/')
def index():
  return flask.render_template('index.html')

@app.route('/api/record_answer')
def record_answer():
  ans = flask.request.args['ans']
  question = ans.split("=")[0] + "="
  answer = ans[len(question):]
  answers.record_answer(question, answer)
  return "ok"

@app.route('/homework.html')
@app.route('/homework')
def homework():
  app.logger.info("Starting homework method.")
  if not auth.LoggedIn():
    return flask.redirect(flask.url_for("login_page"))
  num_a = random.randint(0,9)
  num_b = random.randint(0,9)
  expected = num_a + num_b
  question = {'num_a': num_a, 'num_b': num_b, 'expected': expected}
  answers.record_question("%s+%s=" % (num_a, num_b))
  # TODO: make question a string?
  return flask.render_template('homework.html', question=question)

@app.route('/grades.html')
@app.route('/grades')
def grades():
  if not auth.LoggedIn():
    return flask.redirect(flask.url_for("login_page"))
  rows = answers.query_answers(auth.Username())
  return flask.render_template('grades.html', rows=rows)


if __name__ == '__main__':
  app.run(debug=True, host='localhost')
  # commented because it's not safe
  # app.run(debug=True,host='0.0.0.0')

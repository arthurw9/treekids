import flask
import json
# from flask import Flask, escape, request, render_template

import auth
import maintenance
import config

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
    if "query_button" in flask.request.form:
      query = flask.request.form["query"]
      rows = maintenance.query(query)
    if "new_ics_user_button" in flask.request.form:
      maintenance.new_user(flask.request.form)
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
  flask.g.internal = auth.IsInternal()
  return flask.render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True, host='localhost')
  # commented because it's not safe
  # app.run(debug=True,host='0.0.0.0')

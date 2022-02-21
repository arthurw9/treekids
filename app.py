import flask
# from flask import Flask, escape, request, render_template

import auth
import maintenance
import config

config.CreateIfNotExists()
app = flask.Flask(__name__)
app.config.from_json("config.json")

@app.route('/ics', methods=['GET', 'POST'])
def ics_page():
  if 'username' not in flask.session or flask.session['username'] != 'arthur':
    return flask.redirect(flask.url_for("login_page"))
  if flask.request.method == 'POST':
    maintenance.init_db()
  return flask.render_template('ics.html')

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


if __name__ == '__main__':
  app.run(debug=True, host='localhost')
  # commented because it's not safe
  # app.run(debug=True,host='0.0.0.0')

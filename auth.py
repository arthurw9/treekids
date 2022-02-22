import flask
# from flask import Flask, escape, request, render_template

_username = ""

def CheckLogin():
  # TODO: Check the password
  flask.session['username'] = flask.request.form['username'].lower()

def Logout():
  flask.session.pop('username', None)

def IsInternal():
  if not 'username' in flask.session:
    return False
  user = flask.session['username']
  if user in ["arthur", "edmundo", "justo"]:
    return True
  return False

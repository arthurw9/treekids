import flask
# from flask import Flask, escape, request, render_template

_username = ""

def CheckLogin():
  # TODO: Check the password
  flask.session['username'] = flask.request.form['username']

def Logout():
  flask.session.pop('username', None)


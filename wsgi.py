import sys

project_home = '/home/arthur/programming/treekids/mysite'
if project_home not in sys.path:
  sys.path = [project_home] + sys.path

from flask_app import app

if __name__ == "__main__":
  app.run()

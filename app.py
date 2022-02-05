from flask import Flask, escape, request

print(__name__)

app = Flask(__name__)

@app.route('/')
def hello_world():
  name = request.args.get("name", "World")
  s = "<center>Hello %s!</center>" % escape(name)
  s += "<p>let's go!</p>"
  return s
 

if __name__ == '__main__':
 app.run(debug=True,host='0.0.0.0')

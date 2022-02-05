from flask import Flask, escape, request, render_template

print(__name__)

app = Flask(__name__)

@app.route('/')
def hello_template():
  name = request.args.get("name", "World")
  return render_template('index.html')

@app.route('/v1')
def hello_world():
  name = request.args.get("name", "World")
  s = "<center>Hello %s!</center>" % escape(name)
  s += "<p>let's go!</p>"
  return s
 

if __name__ == '__main__':
 app.run(debug=True,host='0.0.0.0')

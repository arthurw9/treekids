import flask
import random
import auth
import maintenance
import config
import answers
import db_utils
import questions

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
    if "questions_button" in flask.request.form:
      user_query = flask.request.form["user_query"]
      rows = questions.query(user_query)
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
  if 'ans' in flask.request.args:
    ans = flask.request.args['ans']
    question = ans.split("=")[0] + "="
    answer = ans[len(question):]
  else:
    question = flask.request.args['question']
    answer = flask.request.args['answer']
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

@app.route('/build.html', methods=['GET', 'POST'])
@app.route('/build', methods=['GET', 'POST'])
def build():
  if not auth.LoggedIn():
    return flask.redirect(flask.url_for("login_page"))
  if flask.request.method == 'POST':
    questions.save(flask.request.form);
    rows = questions.query()
    return flask.render_template('questions.html', rows=rows)
  if 'question_id' in flask.request.args:
    question_id = flask.request.args['question_id']
    return questions.edit(question_id)
  if 'new_question_button' in flask.request.args:
    return flask.render_template('build.html', question_id=-1)
  rows = questions.query()
  return flask.render_template('questions.html', rows=rows)

@app.route('/view.html', methods=['GET', 'POST'])
@app.route('/view', methods=['GET', 'POST'])
def view():
  if not auth.LoggedIn():
    return flask.redirect(flask.url_for("login_page"))
  qid = 0
  if 'qid' in flask.request.args:
    qid = flask.request.args['qid']
  q = questions.GetNextQuestion(qid)
  answers.record_question("%s: %s" % (q["qid"], q["question"]))
  # return q
  return flask.render_template('view.html', q=q)


@app.teardown_appcontext
def tearDown(exception):
  db_utils.close_connection(exception)


if __name__ == '__main__':
  app.run(debug=True, host='localhost')
  # commented because it's not safe
  # app.run(debug=True,host='0.0.0.0')

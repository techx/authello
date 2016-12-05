from flask import render_template, redirect, request, session, url_for, jsonify
from functools import wraps

from authenticate import app, db, APP_ID
from authenticate.helpers import verify_token, is_valid_application_id, is_valid_return_url
from authenticate.models import Application

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'kerberos' not in session:
      return redirect(url_for('login', next=request.url))
    return f(*args, **kwargs)
  return decorated_function


@app.route('/manage/login')
def login():
  if 'next' in request.args:
    return redirect(url_for('handle_auth_request', application_id=APP_ID, next=request.args['next']))
  else:
    return redirect(url_for('handle_auth_request', application_id=APP_ID))


@app.route('/manage/login_return')
def login_return():
  secret = Application.find_by_id(APP_ID).secret
  success, err_msg = verify_token(request.args['kerberos'],
                                  request.args['time'],
                                  secret,
                                  request.args['token'])
  if not success:
    return "Login was unsuccessful: " + err_msg, 400
  session['kerberos'] = request.args['kerberos']
  session['acting_as'] = request.args['kerberos']
  return redirect(request.args['next'] if 'next' in request.args else url_for('index'))


@app.route('/manage/logout')
def logout():
  session.pop('kerberos', None)
  session.pop('acting_as', None)
  return redirect(url_for('index'))


@app.route('/')
def index():
  return render_template('homepage.html')


@app.route('/manage/')
@login_required
def manage_index():
  applications = Application.query.filter(Application.owner == session['acting_as']).all()
  return render_template('manage.html', applications=applications)


@app.route('/manage/create', methods=['POST'])
@login_required
def create_application():
  name = request.form['name']
  return_url = request.form['return_url']
  assert is_valid_return_url(return_url)
  application = Application(name, return_url, session['acting_as'])
  db.session.add(application)
  db.session.commit()
  return render_template('application_created.html', application=application)

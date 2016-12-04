from flask import render_template, redirect, request, session, url_for
from functools import wraps

from authenticate import app, APP_NAME
from authenticate.helpers import verify_token
from authenticate.models import Application

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'kerberos' not in session:
      return redirect(url_for('login_redirect', next=request.url))
    return f(*args, **kwargs)
  return decorated_function


@app.route('/manage/login')
def login_redirect():
  return redirect(url_for('handle_auth_request', application_name=APP_NAME, next=request.args['next']))


@app.route('/manage/login_return')
def login_return():
  secret = Application.query.filter(Application.name == APP_NAME).one().secret
  success, err_msg = verify_token(request.args['kerberos'],
                                  request.args['time'],
                                  secret,
                                  request.args['token'])
  if not success:
    return "Login was unsuccessful: " + err_msg, 400
  session['kerberos'] = request.args['kerberos']
  session['acting_as'] = request.args['kerberos']
  return redirect(request.args['next'])


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
  return "You are logged in " + session['kerberos']

import sys
import time
from flask import Flask, session, redirect, url_for, abort, Config, request
from functools import wraps
from hashlib import sha256

####### IGNORE THIS STUFF
APPLICATION_ID = sys.argv[1]
APPLICATION_SECRET = sys.argv[2]
AUTHELLO_URL = 'https://authello.mit.edu/auth/'

class DevConfig(Config):
  DEBUG = True
  SECRET_KEY = 'this-is-a-super-secret-key'

app = Flask(__name__)
app.config.from_object(DevConfig)
####### END IGNORE


####################
# Helpers
####################

# Returns the kerberos of the person who is logged in, otherwise None
def get_user():
    return session.get('kerberos')


# A decorator to make that function's route require login.
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'kerberos' not in session:
      abort(404)
    return f(*args, **kwargs)
  return decorated_function


# Calculates a token given a kerberos, time, and secret
def calculate_token(kerberos, cur_time, secret):
  h = sha256()
  h.update(kerberos + '\x00' + str(cur_time) + '\x00' + secret)
  return h.hexdigest()


# Checks if a token returned from authello.mit.edu is valid
def verify_token(kerberos, req_time, token):
  if abs(int(req_time) - time.time()) > 300: # tokens are valid for 5 minutes.
    return False, 'Token is too old'
  ctoken = calculate_token(kerberos, req_time, APPLICATION_SECRET)
  if ctoken != token:
    return False, 'Calculated token does not match'
  return True, None


####################
# Routes
####################

# The index page
@app.route('/', methods=["GET"])
def index():
  if get_user():
    return "Welcome {}! Visit /secret to see a page that requires login, and visit /logout to log out.".format(get_user())
  else:
    return "Hello stranger! Please visit /login to log in."


# A route only visible if logged in
@app.route('/secret', methods=["GET"])
@login_required
def secret():
  return "Congrats, {}, you found the secret page.".format(get_user())


# The route to initiate login
@app.route('/login', methods=["GET"])
def start_login():
  return redirect(AUTHELLO_URL + APPLICATION_ID)


# The route to finish login
@app.route('/login_return', methods=["GET"])
def finish_login():
  success, err = verify_token(request.args['kerberos'], request.args['time'], request.args['token'])
  if success:
    session['kerberos'] = request.args['kerberos']
    return redirect(url_for('index'))
  else:
    return err


# The route to log out
@app.route('/logout', methods=["GET"])
def logout():
  session.pop('kerberos', None)
  return redirect(url_for('index'))


if __name__ == "__main__":
  app.run(port=5005)

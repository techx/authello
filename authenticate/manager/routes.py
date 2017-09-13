import re
from flask import render_template, request, g, redirect, url_for, Response

from authenticate import app, db
from authenticate.helpers import verify_token
from authenticate.models import Application, Owner, AccessLog
from authenticate.helpers import parse_certificate_dn

def is_valid_return_url(url):
  return bool(re.match(r'^https?://[^\s]+$', url.lower()))

@app.route('/')
def index():
  return render_template('homepage.html')


@app.route('/manage/')
def manage_index():
  applications = Application.query.filter(Application.owner == g.current_owner).all()
  return render_template('manage.html', applications=applications)


@app.route('/manage/create', methods=['POST'])
def create_application():
  name = request.form['name']
  return_url = request.form['return_url']
  assert is_valid_return_url(return_url)
  application = Application(name, return_url, g.current_owner)
  db.session.add(application)
  db.session.commit()
  return render_template('application_created.html', application=application)

@app.route('/manage/<application_id>/delete', methods=['POST'])
def delete_application(application_id):
  application = Application.find_by_id(application_id)
  db.session.delete(application)
  db.session.commit()
  return redirect(url_for('manage_index'))

@app.route('/manage/<application_id>/logs', methods=['GET'])
def application_log(application_id):
  limit = int(request.args.get('limit', 100))
  application = Application.find_by_id(application_id)
  logs = AccessLog.query.filter(AccessLog.application == application).order_by(AccessLog.time.desc()).limit(limit).all()
  result = ""
  for log in logs:
    result += "{},{}\n".format(log.time, parse_certificate_dn(log.certificate_info)['kerberos'])
  if result == "":
    result = "No information to display!"
  return Response(result, mimetype='text/plain')

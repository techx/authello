from urlparse import parse_qsl, urlparse, urlunparse
import time
from flask import request, redirect
from urllib import urlencode

from authenticate import app, db
from authenticate.models import Application, AccessLog
from authenticate.helpers import calculate_token, is_valid_application_name, parse_certificate_dn

def construct_redirect_url(url_base, params):
  url_parts = list(urlparse(application.return_url))
  query = dict(urlparse.parse_qsl(url_parts[4]))
  query.update(params)
  url_parts[4] = urlencode(query)
  return urlunparse(url_parts)

@app.route('/auth/<application_name>')
def handle_auth_request(application_name):
  application = Application.find_by_name(application_name)
  if not application:
    return "Could not find the given application :(", 404
  certificate_info_str = request.headers.get('x-certificate-info')
  if app.debug and not certificate_info_str:
    # TODO: Make this an actual dummy string
    certificate_info_str = ''

  certificate_info = parse_certificate_dn(certificate_info_str)

  log_entry = AccessLog(application, certificate_info_str)
  db.session.add(log_entry)
  db.session.commit()

  kerberos = certificate_info['kerberos']
  time = int(time.time())
  token = calculate_token(kerberos, time, application.secret)
  params = {'token': token, 'user': kerberos, 'time': time}
  return redirect(construct_redirect_url(application.return_url, params))

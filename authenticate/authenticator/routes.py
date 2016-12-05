from urlparse import parse_qsl, urlparse, urlunparse
import time
from flask import request, redirect
from urllib import urlencode

from authenticate import app, db
from authenticate.models import Application, AccessLog
from authenticate.helpers import calculate_token, parse_certificate_dn

def construct_redirect_url(url_base, request_args, new_params):
  url_parts = list(urlparse(url_base))
  query = dict(parse_qsl(url_parts[4]))
  query.update(request_args)
  query.update(new_params)
  # Necessary to fix some parameter parsing issues
  query = {key: value[0] if isinstance(value, list) and len(value) == 1 else value
           for key, value in query.iteritems()}
  url_parts[4] = urlencode(query)
  return urlunparse(url_parts)

@app.route('/auth/<application_id>')
def handle_auth_request(application_id):
  application = Application.find_by_id(application_id)
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
  cur_time = int(time.time())
  token = calculate_token(kerberos, cur_time, application.secret)
  new_params = {'token': token, 'kerberos': kerberos, 'time': cur_time}
  return redirect(construct_redirect_url(application.return_url, dict(request.args), new_params))

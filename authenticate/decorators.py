import re

from flask import abort, session, g, request
from authenticate import app, db

from authenticate.models import Owner
from authenticate.helpers import parse_certificate_dn

ADMINS = set(['jserrino'])

TEST_CERT = '/C=US/ST=Massachusetts/O=Massachusetts Institute of Technology/OU=Client CA v1/CN=Jack S Serrino/emailAddress=jserrino@MIT.EDU'

def is_admin(kerberos):
  return kerberos in ADMINS

@app.before_request
def set_up_g():
  cert = TEST_CERT if app.debug else request.headers['x-certificate-info']
  g.raw_certificate_info = cert
  g.parsed_certificate_info = parse_certificate_dn(cert)
  g.is_admin = is_admin(g.parsed_certificate_info['kerberos'])

  if 'current_kerberos' not in session:
    session['current_kerberos'] = g.parsed_certificate_info['kerberos']

  g.current_owner = Owner.get_or_create(session['current_kerberos'])

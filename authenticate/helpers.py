import re
from hashlib import sha256

def calculate_token(kerberos, time, secret):
  h = sha256()
  h.update(kerberos + '\x00' + str(time) + '\x00' + secret)
  return h.hexdigest()

def is_valid_application_name(name):
  return bool(re.match(r'^[a-z0-9_-]+$', name.lower()))

def parse_certificate_dn(cert_info_string):
  return {
    'kerberos': 'jserrino'
  }

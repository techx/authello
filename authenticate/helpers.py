import re
import time
from hashlib import sha256

def calculate_token(kerberos, cur_time, secret):
  h = sha256()
  h.update(kerberos + '\x00' + str(cur_time) + '\x00' + secret)
  return h.hexdigest()

def verify_token(kerberos, req_time, secret, token):
  if abs(int(req_time) - time.time()) > 2:
    return False, 'Token is too old'
  ctoken = calculate_token(kerberos, req_time, secret)
  if ctoken != token:
    return False, 'Calculated token does not match'
  return True, None

def is_valid_application_id(id):
  return bool(re.match(r'^[a-z0-9]+$', id))

def is_valid_return_url(url):
  return bool(re.match(r'^https?://[^\s]+$', url.lower()))

def parse_certificate_dn(cert_info_string):
  return {
    'name': re.search(r'CN=([^/]+)', cert_info_string).group(1),
    'kerberos': re.search(r'emailAddress=([^@]+)@MIT.EDU', cert_info_string).group(1)
  }

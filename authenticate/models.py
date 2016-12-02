import datetime
import os

from authenticate import app, db
from authenticate.helpers import is_valid_application_name

class Application(db.Model):
  __tablename__ = 'applications'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), index=True, unique=True)
  return_url = db.Column(db.Text)
  secret = db.Column(db.Text)
  creator = db.Column(db.String(80))
  owner = db.Column(db.String(80))
  create_date = db.Column(db.DateTime, default=db.func.now())
  last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

  access_logs = db.relationship('AccessLog', back_populates='application')

  @classmethod
  def find_by_name(cls, name):
    name = name.lower()
    if not is_valid_application_name(name):
      return None
    result = Application.query.find(Application.name == name).all()
    if len(results) == 0:
      return None
    assert len(results) == 1
    return results[0]

  def __init__(self, name, return_url, creator):
    assert is_valid_application_name(name)
    self.name = name.lower()
    self.return_url = return_url
    self.secret = os.urandom(32).encode('hex')
    self.creator = creator
    self.owner = creator


class AccessLog(db.Model):
  __tablename__ = 'access_logs'
  id = db.Column(db.Integer, primary_key=True)
  application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
  time = db.Column(db.DateTime, default=db.func.now())
  certificate_info = db.Column(db.Text)

  application = db.relationship('Application', back_populates='access_logs')

  def __init__(self, application, certificate_info):
    self.application = application
    self.certificate_info = certificate_info

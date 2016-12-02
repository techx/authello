from authenticate import app, db

import datetime

class Application(db.Model):
  __tablename__ = 'applications'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True)
  creator = db.Column(db.String(80))
  owner = db.Column(db.String(80))
  create_date = db.Column(db.DateTime, default=db.func.now())
  last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

  access_logs = db.relationship('AccessLog', back_populates='application')


class AccessLog(db.Model):
  __tablename__ = 'access_logs'
  id = db.Column(db.Integer, primary_key=True)
  application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
  time = db.Column(db.DateTime, default=db.func.now())
  certificate_info = db.Column(db.Text, nullable=True)

  application = db.relationship('Application', back_populates='access_logs')


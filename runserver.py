import os
from authenticate import app, db, APP_NAME
from authenticate.models import Application

app.config.from_object('authenticate.config.DevConfig')

if not os.path.exists('dev.db'):
  print "Regenerating db..."
  db.create_all()
  db.session.add(Application(APP_NAME, '/manage/login_return', '__DEV__'))
  db.session.commit()

app.run()

import os
from authenticate import app, db, APP_ID
from authenticate.models import Application

app.config.from_object('authenticate.config.DevConfig')

if not os.path.exists('dev.db'):
  print "Regenerating db..."
  db.create_all()
  application = Application('techx-authenticate', '/manage/login_return', '__DEV__')
  application.id = APP_ID
  db.session.add(application)
  db.session.commit()

app.run()

import os
from authenticate import app, db

app.config.from_object('authenticate.config.DevConfig')

if not os.path.exists('dev.db'):
  print "Regenerating db..."
  db.create_all()

app.run()

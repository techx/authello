from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('authenticate.config.ProductionConfig')
db = SQLAlchemy(app)

APP_NAME = 'techx-authenticate'

import authenticate.authenticator
import authenticate.manager
import authenticate.models

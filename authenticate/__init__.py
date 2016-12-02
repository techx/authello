from flask import Flask
app = Flask(__name__)
app.config.from_object('authenticate.config.ProductionConfig')

import authenticate.authenticator
import authenticate.manager

from flask import render_template

from authenticate import app

@app.route('/')
def index():
  return render_template('homepage.html')

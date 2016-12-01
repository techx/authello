from flask import Flask, request
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World! I'm a flask example."

if __name__ == '__main__':
    app.run(debug=True)

# python-flask

This folder shows a simple example application that uses flask and authello.mit.edu to log users in.

To run this example, first install the dependencies by running:

`pip install -r requirements.txt`

Then, go to authello.mit.edu, and create a new application with return URL `http://localhost:5005/login_return`

Finally, run this example:

`python app.py <application id> <application secret>`

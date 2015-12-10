#! /usr/bin/env python3
from flask import Flask
from flask.ext.script import Manager


app = Flask(__name__) # The Flask application
app.debug = True
manager = Manager(app)

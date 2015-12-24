#! /usr/bin/env python3
from flask import Flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__) # The Flask application
app.debug = True
manager = Manager(app)

# Bootstrap
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)

# database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
import os.path
def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))
from flask.ext.sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../app.db'))
db=SQLAlchemy(app)

app.config['SECRET_KEY'] = "ca4fea79-f05e-4f0c-af86-261fd3b830c5"

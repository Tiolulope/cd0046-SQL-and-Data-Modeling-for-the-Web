import os

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
#from .templates.models import Venue
from datetime import datetime
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *
import sys

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Adedapo22@localhost:5432/fyyurproject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = '<Put your local database url>'
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

"""Flask app for Cupcakes"""
import os

from flask import Flask, render_template, redirect, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Cupcake, DEFAULT_IMAGE

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

connect_db(app)

toolbar = DebugToolbarExtension(app)
from flask import flask, render_template, request, redirect, flash, session
from models import *
from app import app
from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')
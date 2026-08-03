from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'person'
    pid = db.Column(db.Integer, primary_key=True)
    identity_handle = db.Column(db.String(80), unique=True, nullable=False)
    sec_key = db.Column(db.String(256), nullable=False)
    profile_type = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    assigned_treks = db.relationship('Trek', backref='guide', lazy=True)

    def set_sec_key(self, pwd):
        self.sec_key = generate_password_hash(pwd, method='scrypt')

    def verify_sec_key(self, pwd):
        return check_password_hash(self.sec_key, pwd)

class Trek(db.Model):
    __tablename__ = 'trek'
    tid = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    challenge_level = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    open_slots = db.Column(db.Integer, nullable=False)
    commencement_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    trek_status = db.Column(db.String(50), default='Pending Approval')
    coordinator_id = db.Column(db.Integer, db.ForeignKey('person.pid'), nullable=True)

class Reservation(db.Model):
    __tablename__ = 'reservation'
    rid = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('person.pid', ondelete='CASCADE'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.tid', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(50), default='Booked')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    client = db.relationship('Person', backref='reservations')
    trek = db.relationship('Trek', backref='reservations')

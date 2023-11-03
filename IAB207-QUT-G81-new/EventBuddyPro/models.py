from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from . import db

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Open, Inactive, Sold Out, Cancelled
    image = db.Column(db.String(60), nullable=False, default='default.jpg')
    price = db.Column(db.Float, nullable=False)  # Assuming each event has a fixed price
    category = db.Column(db.String(50), nullable=False)  # Category of the event

    # Relationships
    comments = db.relationship('Comment', backref='event', lazy=True)
    bookings = db.relationship('Booking', backref='event', lazy=True)

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # You should hash and salt the password
    contact_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # Relationships
    comments = db.relationship('Comment', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comment' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False)

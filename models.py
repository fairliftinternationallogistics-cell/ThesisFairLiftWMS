from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# -------------------- USER --------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='admin')

    # Relationships
    driver = db.relationship('Driver', backref='user', uselist=False)
    events = db.relationship('Event', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


# -------------------- DRIVER --------------------
class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    vehicle_plate = db.Column(db.String(50))
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)
    status = db.Column(db.String(50), default="available")

    # Relationships
    parcels = db.relationship('Parcel', backref='driver', lazy=True)

    def __repr__(self):
        return f"<Driver {self.name} ({self.status})>"


# -------------------- PARCEL --------------------
class Parcel(db.Model):
    __tablename__ = 'parcels'

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(64), unique=True, nullable=False)
    size = db.Column(db.String(10))
    weight = db.Column(db.Float)
    arrival_date = db.Column(db.DateTime, default=datetime.utcnow)
    destination = db.Column(db.String(200))
    status = db.Column(db.String(50), default="stored")  # stored, assigned, in-transit, delivered
    location_rack = db.Column(db.String(64))
    extra_data = db.Column(db.JSON)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))

    tickets = db.relationship('Ticket', backref='parcel', lazy=True)

    def __repr__(self):
        return f"<Parcel {self.tracking_number} - {self.status}>"


# -------------------- TICKET --------------------
class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcels.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    department = db.Column(db.String(120))
    status = db.Column(db.String(50), default="open")
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Ticket {self.id} - {self.status}>"


# -------------------- EVENT (Calendar) --------------------
class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
            "description": self.description,
            "created_by": self.created_by
        }

    def __repr__(self):
        return f"<Event {self.title}>"

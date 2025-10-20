from flask import Flask, request, jsonify, session, redirect
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, User, Driver, Parcel, Ticket, Event
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import requests
import random
import time

app = Flask(__name__, static_folder="static")
CORS(app, supports_credentials=True)

# -------------------- CONFIG --------------------
app.config['SECRET_KEY'] = 'fairlift_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/fairlift_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- AUTH --------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        login_user(user)
        return jsonify({"message": "Login successful", "role": user.role})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

# -------------------- ADMIN: PARCELS --------------------
@app.route('/api/parcels', methods=['GET'])
@login_required
def get_parcels():
    parcels = Parcel.query.all()
    return jsonify([
        {
            "tracking_number": p.tracking_number,
            "destination": p.destination,
            "status": p.status,
            "driver_id": p.driver_id
        } for p in parcels
    ])

@app.route('/api/parcels', methods=['POST'])
@login_required
def add_parcel():
    data = request.json
    parcel = Parcel(
        tracking_number=data.get('tracking_number'),
        destination=data.get('destination'),
        status=data.get('status', 'stored'),
        size=data.get('size'),
        weight=data.get('weight'),
        arrival_date=datetime.utcnow()
    )
    db.session.add(parcel)
    db.session.commit()
    return jsonify({"message": "Parcel added"})

# -------------------- DRIVER API --------------------
@app.route('/api/driver/parcels', methods=['GET'])
@login_required
def driver_parcels():
    if current_user.role != 'driver':
        return jsonify({"error": "Unauthorized"}), 403
    driver = Driver.query.filter_by(user_id=current_user.id).first()
    parcels = Parcel.query.filter_by(driver_id=driver.id).all()
    return jsonify([
        {
            "tracking_number": p.tracking_number,
            "destination": p.destination,
            "status": p.status
        } for p in parcels
    ])

@app.route('/api/driver/update_status', methods=['POST'])
@login_required
def driver_update_status():
    if current_user.role != 'driver':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    parcel = Parcel.query.filter_by(tracking_number=data.get('tracking_number')).first()
    if parcel:
        parcel.status = data.get('status')
        db.session.commit()
        return jsonify({"message": "Status updated"})
    return jsonify({"error": "Parcel not found"}), 404

@app.route('/api/driver/live_location', methods=['POST'])
@login_required
def driver_live_location():
    if current_user.role != 'driver':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    driver = Driver.query.filter_by(user_id=current_user.id).first()
    driver.current_lat = data.get('lat')
    driver.current_lng = data.get('lng')
    db.session.commit()
    return jsonify({"message": "Location updated"})

# -------------------- CALENDAR --------------------
@app.route('/api/events', methods=['GET'])
@login_required
def get_events():
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events])

@app.route('/api/events', methods=['POST'])
@login_required
def add_event():
    data = request.json
    event = Event(
        title=data.get('title'),
        start=data.get('start'),
        end=data.get('end'),
        description=data.get('description'),
        created_by=current_user.id
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Event added"})

# -------------------- TRACKING SIMULATION --------------------
@app.route('/api/parcels/<tracking_number>/live')
def simulate_live_tracking(tracking_number):
    # Simulate random movement for demo
    parcel = Parcel.query.filter_by(tracking_number=tracking_number).first()
    if not parcel:
        return jsonify({"error": "Parcel not found"}), 404

    base_lat, base_lng = 14.6042, 120.9822
    delta_lat = random.uniform(-0.01, 0.01)
    delta_lng = random.uniform(-0.01, 0.01)
    new_lat = base_lat + delta_lat
    new_lng = base_lng + delta_lng

    return jsonify({
        "tracking_number": tracking_number,
        "status": parcel.status,
        "position": {"lat": new_lat, "lng": new_lng}
    })

# -------------------- AUTO-SEED --------------------
@app.before_first_request
def auto_seed_demo():
    try:
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('password123')
            db.session.add(admin)
            db.session.commit()

        driver_user = User.query.filter_by(username='driver1').first()
        if not driver_user:
            driver_user = User(username='driver1', role='driver')
            driver_user.set_password('password123')
            db.session.add(driver_user)
            db.session.commit()

        driver = Driver.query.filter_by(user_id=driver_user.id).first()
        if not driver:
            driver = Driver(
                user_id=driver_user.id,
                name='Juan Dela Cruz',
                phone='+639171234567',
                vehicle_plate='ABC-123',
                current_lat=14.6042,
                current_lng=120.9822,
                status='available'
            )
            db.session.add(driver)
            db.session.commit()

        parcel = Parcel.query.filter_by(tracking_number='FL-DRIVER-001').first()
        if not parcel:
            parcel = Parcel(
                tracking_number='FL-DRIVER-001',
                destination='Bonifacio Global City, Taguig, Philippines',
                status='assigned',
                driver_id=driver.id
            )
            db.session.add(parcel)
            db.session.commit()

        print("✅ Demo data seeded successfully.")
    except Exception as e:
        print("⚠️ Auto-seed failed:", e)

# -------------------- RUN APP --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

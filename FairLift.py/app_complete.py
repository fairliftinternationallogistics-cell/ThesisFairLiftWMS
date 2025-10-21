from flask import Flask, request, jsonify, send_from_directory, session
from config import Config
from models import db, User, Parcel, Ticket, Driver
from flask_migrate import Migrate
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_cors import CORS
from datetime import datetime, date

# --- Flask app setup ---
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)

# --- Ensure session & CORS settings ---
app.config.update(
    SECRET_KEY="supersecretkey",  # Change before production
    SESSION_COOKIE_SAMESITE=None,
    SESSION_COOKIE_SECURE=False
)
CORS(app, supports_credentials=True)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Serve pages ---
@app.route('/')
def index():
    return send_from_directory('static', 'Login.html')


@app.route('/page/<path:filename>')
def page(filename):
    return send_from_directory('static', filename)


# --- AUTH API ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        session.permanent = True
        return jsonify({"message": "Logged in", "username": user.username, "role": user.role})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out"})
@app.route('/api/user/info', methods=['GET'])
@login_required
def user_info():
    return jsonify({
        "username": current_user.username,
        "role": current_user.role
    })

# --- PARCELS API ---
@app.route('/api/parcels', methods=['GET'])
@login_required
def list_parcels():
    q = Parcel.query
    dest = request.args.get('destination')
    status = request.args.get('status')
    size = request.args.get('size')

    if dest:
        q = q.filter(Parcel.destination.ilike(f"%{dest}%"))
    if status:
        q = q.filter_by(status=status)
    if size:
        q = q.filter_by(size=size)

    parcels = q.order_by(Parcel.arrival_date.desc()).all()
    out = [{
        "id": p.id,
        "tracking_number": p.tracking_number,
        "size": p.size,
        "weight": p.weight,
        "arrival_date": p.arrival_date.isoformat() if p.arrival_date else None,
        "destination": p.destination,
        "status": p.status,
        "location_rack": p.location_rack,
       "metadata": dict(p.metadata) if isinstance(p.metadata, dict) else {}
    } for p in parcels]

    return jsonify(out)


@app.route('/api/parcels', methods=['POST'])
@login_required
def create_parcel():
    data = request.json
    if not data or not data.get('tracking_number'):
        return jsonify({"error": "tracking_number required"}), 400

    if Parcel.query.filter_by(tracking_number=data['tracking_number']).first():
        return jsonify({"error": "tracking_number already exists"}), 400

    p = Parcel(
        tracking_number=data['tracking_number'],
        size=data.get('size'),
        weight=data.get('weight'),
        arrival_date=(date.fromisoformat(data['arrival_date'])
                      if data.get('arrival_date') else None),
        destination=data.get('destination'),
        status=data.get('status', 'stored'),
        location_rack=data.get('location_rack'),
        metadata=data.get('metadata')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "created", "id": p.id}), 201


@app.route('/api/parcels/<int:parcel_id>', methods=['GET'])
@login_required
def get_parcel(parcel_id):
    p = Parcel.query.get_or_404(parcel_id)
    return jsonify({
        "id": p.id,
        "tracking_number": p.tracking_number,
        "size": p.size,
        "weight": p.weight,
        "arrival_date": p.arrival_date.isoformat() if p.arrival_date else None,
        "destination": p.destination,
        "status": p.status,
        "location_rack": p.location_rack,
        "metadata": p.metadata if isinstance(p.metadata, dict) else {}
    })
@app.route('/api/parcels/<int:parcel_id>', methods=['PUT', 'PATCH'])
@login_required
def update_parcel(parcel_id):
    """Update existing parcel details"""
    p = Parcel.query.get_or_404(parcel_id)
    data = request.get_json() or {}

    # Update only the fields provided
    if 'tracking_number' in data:
        # prevent duplicates
        existing = Parcel.query.filter_by(tracking_number=data['tracking_number']).first()
        if existing and existing.id != p.id:
            return jsonify({"error": "Tracking number already exists"}), 400
        p.tracking_number = data['tracking_number']

    if 'size' in data:
        p.size = data['size']
    if 'weight' in data:
        try:
            p.weight = float(data['weight'])
        except (TypeError, ValueError):
            return jsonify({"error": "Weight must be numeric"}), 400
    if 'arrival_date' in data:
        try:
            p.arrival_date = date.fromisoformat(data['arrival_date'])
        except ValueError:
            return jsonify({"error": "Invalid date format (use YYYY-MM-DD)"}), 400
    if 'destination' in data:
        p.destination = data['destination']
    if 'status' in data:
        p.status = data['status']
    if 'location_rack' in data:
        p.location_rack = data['location_rack']
    if 'metadata' in data and isinstance(data['metadata'], dict):
        p.metadata = data['metadata']

    db.session.commit()
    return jsonify({"message": "Parcel updated successfully", "id": p.id})


@app.route('/api/parcels/<int:parcel_id>', methods=['DELETE'])
@login_required
def delete_parcel(parcel_id):
    p = Parcel.query.get_or_404(parcel_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"})
# --- Get parcel by tracking number (unique endpoint name) ---
# Fetch parcel by numeric ID
@app.route('/api/parcels/id/<int:parcel_id>', methods=['GET'])
@login_required
def get_parcel_by_id(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    return jsonify({
        "id": parcel.id,
        "tracking_number": parcel.tracking_number,
        "destination": parcel.destination,
        "status": parcel.status,
        "size": parcel.size,
        "weight": parcel.weight,
        "arrival_date": parcel.arrival_date.isoformat() if parcel.arrival_date else None,
        "location_rack": parcel.location_rack,
        "metadata": parcel.metadata if isinstance(parcel.metadata, dict) else {}
    })
# Fetch parcel by tracking number (string)
@app.route('/api/parcels/<tracking_number>', methods=['GET'])
@login_required
def get_parcel_by_tracking(tracking_number):
    parcel = Parcel.query.filter_by(tracking_number=tracking_number).first()
    if not parcel:
        return jsonify({"error": "Parcel not found"}), 404

    return jsonify({
        "id": parcel.id,
        "tracking_number": parcel.tracking_number,
        "destination": parcel.destination,
        "status": parcel.status,
        "size": parcel.size,
        "weight": parcel.weight,
        "arrival_date": parcel.arrival_date.isoformat() if parcel.arrival_date else None,
        "location_rack": parcel.location_rack,
        "metadata": parcel.metadata if isinstance(parcel.metadata, dict) else {}
    })
# --- Health route ---
@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})


# --- Unauthorized handler ---
@login_manager.unauthorized_handler
def unauthorized_callback():
    return jsonify({"error": "Unauthorized"}), 401


# --- Start app ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

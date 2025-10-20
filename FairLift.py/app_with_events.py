from flask import Flask, request, jsonify, send_from_directory
from config import Config
from models import db, User, Parcel, Ticket, Driver
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)
CORS(app, supports_credentials=True)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Event model (simple addition here) ---
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.String(50), nullable=False)
    end = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# --- Serve static pages ---
@app.route('/')
def index():
    return send_from_directory('static', 'Login.html')

@app.route('/page/<path:filename>')
def page(filename):
    return send_from_directory('static', filename)

# --- Auth endpoints ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json or request.form
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in", "username": user.username, "role": user.role})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out"})

# --- Parcels API (keep as in original app) ---
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
    out = []
    for p in parcels:
        out.append({
            "id": p.id,
            "tracking_number": p.tracking_number,
            "size": p.size,
            "weight": p.weight,
            "arrival_date": p.arrival_date.isoformat() if p.arrival_date else None,
            "destination": p.destination,
            "status": p.status,
            "location_rack": p.location_rack,
            "metadata": p.metadata or {}
        })
    return jsonify(out)

@app.route('/api/parcels', methods=['POST'])
@login_required
def create_parcel():
    data = request.json
    if not data or not data.get('tracking_number'):
        return jsonify({"error":"tracking_number required"}), 400
    if Parcel.query.filter_by(tracking_number=data['tracking_number']).first():
        return jsonify({"error":"tracking_number already exists"}), 400
    p = Parcel(
        tracking_number=data['tracking_number'],
        size=data.get('size'),
        weight=data.get('weight'),
        arrival_date=(datetime.fromisoformat(data['arrival_date']).date() if data.get('arrival_date') else None),
        destination=data.get('destination'),
        status=data.get('status','stored'),
        location_rack=data.get('location_rack'),
        metadata=data.get('metadata')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"message":"created", "id": p.id}), 201

# --- Events API ---
@app.route('/api/events', methods=['GET'])
@login_required
def list_events():
    events = Event.query.order_by(Event.start).all()
    return jsonify([e.to_dict() for e in events])

@app.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.json
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')
    description = data.get('description')
    if not title or not start:
        return jsonify({"error":"title and start required"}), 400
    ev = Event(title=title, start=start, end=end, description=description, created_by=current_user.id if current_user else None)
    db.session.add(ev)
    db.session.commit()
    return jsonify({"message":"created", "id": ev.id}), 201

@app.route('/api/events/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    ev = Event.query.get_or_404(event_id)
    data = request.json
    if 'title' in data: ev.title = data['title']
    if 'start' in data: ev.start = data['start']
    if 'end' in data: ev.end = data.get('end')
    if 'description' in data: ev.description = data.get('description')
    db.session.commit()
    return jsonify({"message":"updated"})

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    ev = Event.query.get_or_404(event_id)
    db.session.delete(ev)
    db.session.commit()
    return jsonify({"message":"deleted"})

# --- Health ---
@app.route('/api/health')
def health():
    return jsonify({"status":"ok"})

if __name__ == '__main__':
    # create tables if not exist (helpful for testing without migrations)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

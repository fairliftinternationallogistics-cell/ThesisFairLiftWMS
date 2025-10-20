from app import app
from models import db, User
with app.app_context():
    db.create_all()  # ensure tables exist
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin', role='admin')
        u.set_password('password123')   # change this before production
        db.session.add(u)
        db.session.commit()
        print("Admin user created")
    else:
        print("Admin exists")

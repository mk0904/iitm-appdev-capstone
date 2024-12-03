from app import create_app
from database import db
from models import User, Service

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
        if not Service.query.first():
            services = [
                Service(
                    name='Plumbing Service',
                    base_price=75.00,
                    time_required='1-2 hours',
                    description='Professional plumbing services including repairs and installations'
                ),
                Service(
                    name='Electrical Work',
                    base_price=90.00,
                    time_required='2-3 hours',
                    description='Electrical repairs, installations, and maintenance'
                ),
                Service(
                    name='House Cleaning',
                    base_price=60.00,
                    time_required='3-4 hours',
                    description='Complete house cleaning and sanitization services'
                )
            ]
            for service in services:
                db.session.add(service)
                
        db.session.commit()

if __name__ == '__main__':
    init_db()
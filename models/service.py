from database import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(50))
    description = db.Column(db.Text)
    requests = db.relationship('ServiceRequest', back_populates='service', cascade='all, delete-orphan')
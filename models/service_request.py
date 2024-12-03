from datetime import datetime
from database import db

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='requested')
    remarks = db.Column(db.Text)

    service = db.relationship('Service', back_populates='requests')
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_requests')
    professional = db.relationship('User', foreign_keys=[professional_id], backref='professional_requests')
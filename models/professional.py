from database import db

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer)
    description = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('professional', uselist=False))
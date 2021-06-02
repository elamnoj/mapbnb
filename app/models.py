from datetime import datetime as dt
from app import db

class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    regarding = db.Column(db.String)
    explain = db.Column(db.Text)
    created = db.Column(db.DateTime, default=dt.utcnow)

    def from_dict(self, data):
        for field in ['email', 'regarding', 'explain']:
            if field in data:
                if field == 'email':
                    setattr(self, field, data[field].lower())
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        return {
            '_id': self.id,
            'email': self.email,
            'regarding': self.regarding,
            'explain': self.explain,
            'created': dt.strftime(self.created, '%m/%d/%Y')
        }

    def __repr__(self):
        return f'<Submit: [{self.email}]: {self.explain[:20]}...>'


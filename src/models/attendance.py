from models import db
from datetime import datetime
#no se está usando este archivo
class Attendance(db.Model):
    __tablename__='attendance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "check_in_time": self.check_in_time,
            "check_out_time": self.check_out_time,
            "user_id": self.user_id
        }
from models import db
#no se está usando este archivo
class Attendance(db.Model):
    __tablename__='attendance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Datetime, nullable=False)
    check_in_time = db.Column(db.Datetime, nullable=False)
    check_out_time = db.Column(db.Datetime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "check_in_time": self.check_in_time,
            "check_out_time": self.check_out_time,
            "user_id": self.user_id
        }
from models import db
#no se está usando este archivo
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    trainer = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    is_active = db.Column(db.Boolean, nullable=False)
    subscription_date = db.Column(db.Datetime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "trainer": self.trainer,
            "is_active": self.is_active,
            "subscription_date": self.subscription_date
        }
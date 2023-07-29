from models import db
#no se está usando este archivo
class Exercise(db.Model):
    __tablename__='exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    repetitions = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer)
    is_completed = db.Column(db.Boolean, nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)
    equipment_issue = db.Column(db.Enum)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "sets": self.sets,
            "repetitions": self.repetitions,
            "weight": self.weight,
            "is_completed": self.is_completed,
            "equipment_id": self.equipment_id,
            "equipment_issue": self.equipment_issue
        }
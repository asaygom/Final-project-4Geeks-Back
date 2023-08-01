from models import db
#no se está usando este archivo
class Routine(db.Model):
    __tablename__='routine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    weekday = db.Column(db.Enum("monday","tuesday","wednesday","thursday","friday","saturday","sunday",name="weekday"), nullable=False)
    completed_percentage = db.Column(db.Float, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    training_plan = db.relationship("Training_plan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "exercise_id": self.exercise_id,
            "weekday": self.weekday,
            "completed_percentage": self.completed_percentage,
            "is_completed": self.is_completed,
            "is_active": self.is_active
        }
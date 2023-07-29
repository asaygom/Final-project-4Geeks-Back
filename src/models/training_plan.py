from models import db
#no se está usando este archivo
class Training_plan(db.Model):
    __tablename__='training_plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=True)
    start_time = db.Column(db.Datetime, nullable=False)
    finish_time = db.Column(db.Datetime, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False)
    goal_name = db.Column(db.String(200), nullable=False)
    goal_description = db.Column(db.String(200))
    completed_percentage = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "routine_id": self.routine_id,
            "user_id": self.user_id,
            "trainer_id": self.trainer_id,
            "start_time": self.start_time,
            "finish_time": self.finish_time,
            "is_completed": self.is_completed,
            "goal_name": self.goal_name,
            "goal_description": self.goal_description,
            "completed_percentage": self.completed_percentage,
            "is_active": self.is_active
        }
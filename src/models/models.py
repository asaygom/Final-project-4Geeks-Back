from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False)
    subscription_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "trainer_id": self.trainer_id,
            "is_active": self.is_active,
            "subscription_date": self.subscription_date
        }

class Trainer(db.Model):
    __tablename__='trainer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    attendance = db.Column(db.Boolean, nullable=False)
    users = db.relationship("User", backref="trainer", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "attendance": self.attendance
        }
    
class Training_plan(db.Model):
    __tablename__='training_plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finish_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, nullable=False)
    goal_name = db.Column(db.String(200), nullable=False)
    goal_description = db.Column(db.String(200))
    completed_percentage = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    trainer = db.relationship("Trainer")
    user = db.relationship("User")

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
    equipment_issue = db.Column(db.Enum("minor_issue","mid_issue","mayor_issue",name="equipment_issue"))
    routine = db.relationship("Routine")
    equipment = db.relationship("Equipment")

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

class Equipment(db.Model):
    __tablename__='equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum("malfunction","not_working","working",name="status"), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "is_active": self.is_active
        }

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
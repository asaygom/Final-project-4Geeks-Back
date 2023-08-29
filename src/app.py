import re
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.models import db, User, Trainer, Training_plan, Routine, Exercise, Equipment, Attendance
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:admin@localhost/postgres_gym"
app.config["JWT_SECRET_KEY"] = "super-secret" #debemos cambiar esto al archivo .env y pensar un key
app.config['SECRET_KEY'] = "pass-key" #debemos cambiar esto al archivo .env y pensar un key
db.init_app(app)
migrate = Migrate(app,db)
CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# para cambiar el alcance de las expresiones regulares
#Regular expression that checks a valid email
ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
#Regular expression that checks a valid password
preg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'

#empezamos a declarar nuestras rutas y metodos
@app.route('/user', methods=['GET', "POST"])
def handle_user():
    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.to_dict(), users))

        return jsonify({
            "data": users
        }), 200
    elif request.method == 'POST':
        user = User()
        data = request.get_json()
         #Checking email 
        if (re.search(ereg,data["email"])):
            user.email = data["email"]
        else:
            return jsonify({
            "error": "Invalid email format"
        }), 400
        #Checking password
        if (re.search(preg,data["password"])):
            password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            user.password = password_hash
        else:
            return jsonify({
            "error": "Invalid password format"
        }), 400
        #Ask for everything else
        user.name = data["name"]
        user.last_name = data["last_name"]
        user.role = data["role"]

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "msg": "User created"
        }), 200

@app.route('/member', methods=['GET'])
def handle_member():
        members = User.query.filter_by(role="member").all()
        members = list(map(lambda user: user.to_dict(), members))

        return jsonify({
            "data": members
        }), 200

@app.route('/active_member', methods=['GET'])
def handle_activeMember():
        actives_members = User.query.filter_by(role="member",is_active=True).all()
        actives_members = list(map(lambda user: user.to_dict(), actives_members))

        return jsonify({
            "data": actives_members
        }), 200

@app.route('/active_trainer', methods=['GET'])
def handle_activeTrainer():
        actives_trainers = Trainer.query.filter_by(is_active=True).all()
        actives_trainers = list(map(lambda trainer: trainer.to_dict(), actives_trainers))

        return jsonify({
            "data": actives_trainers
        }), 200

@app.route('/userinfo', methods=['GET','PUT', 'DELETE'])
@jwt_required()
def update_user():
    email = get_jwt_identity()
    
    if request.method == 'GET':
        user = User.query.filter_by(email=email).first()
        data = user.to_dict()

        return data, 200

@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    if not email:
        return jsonify({"error": "Missing email parameter"}), 400
    if not password:
        return jsonify({"error": "Missing password parameter"}), 400
    user = User.query.filter_by(email=email).first()
    if email is not None:
        current_password = user.password
        is_valid = bcrypt.check_password_hash(current_password, password)
        if is_valid:
            access_token = create_access_token(identity=email)
            return jsonify({
                "access_token": access_token,
                "user":user.to_dict()
            }), 200
        else:
            return jsonify({
                "error": "Invalid credentials"
            }), 400
    else:
        return jsonify({
            "error": "Invalid credentials"
        }), 400

@app.route("/trainer_login", methods=["POST"])
def trainer_login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    if not email:
        return jsonify({"error": "Missing email parameter"}), 400
    if not password:
        return jsonify({"error": "Missing password parameter"}), 400
    trainer = Trainer.query.filter_by(email=email).first()
    if email is not None:
        current_password = trainer.password
        is_valid = bcrypt.check_password_hash(current_password, password)
        if is_valid:
            access_token = create_access_token(identity=email)
            return jsonify({
                "access_token": access_token,
                "user":trainer.to_dict()
            }), 200
        else:
            return jsonify({
                "error": "Invalid credentials"
            }), 400
    else:
        return jsonify({
            "error": "Invalid credentials"
        }), 400

@app.route('/equipment', methods=['GET', "POST"])
def handle_equipment():
    if request.method == 'GET':
        equipments = Equipment.query.all()
        equipments = list(map(lambda equipment: equipment.to_dict(), equipments))

        return jsonify({
            "data": equipments
        }), 200
    elif request.method == 'POST':
        equipment = Equipment()
        data = request.get_json()
        equipment.name = data["name"]
        equipment.description = data["description"]
        equipment.status = data["status"]
        equipment.is_active = data["is_active"]
        equipment.photo_link = data["photo_link"]

        if not equipment.status:
            equipment.status = None

        db.session.add(equipment)
        db.session.commit()

        return jsonify({
            "msg": "Equipment added"
        }), 200

@app.route('/status_equipment_summary', methods=['GET'])
def handle_statusEquipmentSummary():
        working_equipment = Equipment.query.filter_by(status="working").all()
        working_equipment = list(map(lambda equipment: equipment.to_dict(), working_equipment))
        malfunction_equipment = Equipment.query.filter_by(status="malfunction").all()
        malfunction_equipment = list(map(lambda equipment: equipment.to_dict(), malfunction_equipment))
        not_working_equipment = Equipment.query.filter_by(status="not_working").all()
        not_working_equipment = list(map(lambda equipment: equipment.to_dict(), not_working_equipment))

        return jsonify({
            "data": {"working_equipment": working_equipment, "not_working_equipment": not_working_equipment, "malfunction_equipment": malfunction_equipment}
        }), 200

@app.route('/equipment/<int:id>', methods=['GET','PUT', 'DELETE'])
def update_equipment(id):
    if request.method == 'GET':
        equipment = Equipment.query.get(id)
        data = equipment.to_dict()

        return data, 200
    elif request.method == 'DELETE':
        equipment = Equipment.query.get(id)
        if equipment is not None:
            db.session.delete(equipment)
            db.session.commit()

            return jsonify({
                "msg": "Equipment deleted"
            }), 202
        else:
            return jsonify({
                "error": "Equipment not found"
            }), 404
    elif request.method == 'PUT':
        equipment = Equipment.query.get(id)
        if equipment is not None:
            data = request.get_json()
            equipment.name = data["name"]
            equipment.description = data["description"]
            equipment.status = data["status"]
            equipment.is_active = data["is_active"]
            equipment.photo_link = data["photo_link"]


            db.session.commit()

            return jsonify({
                "error": "Equipment updated"
            }), 200
        else:
            return jsonify({
                "error": "Equipment not found"
            }), 404
        
@app.route('/trainer', methods=['GET', "POST"])
def handle_trainer():
    if request.method == 'GET':
        trainers = Trainer.query.all()
        trainers = list(map(lambda trainer: trainer.to_dict(), trainers))

        return jsonify({
            "data": trainers
        }), 200
    elif request.method == 'POST':
        # Instancing the a new user
        trainer = Trainer()
        data = request.get_json()
         #Checking email 
        if (re.search(ereg,data["email"])):
            trainer.email = data["email"]
        else:
            return jsonify({
            "error": "Invalid email format"
        }), 400
        #Checking password
        if (re.search(preg,data["password"])):
            password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            trainer.password = password_hash
        else:
            return jsonify({
            "error": "Invalid password format"
        }), 400
        #Ask for everything else
        trainer.name = data["name"]
        trainer.last_name = data["last_name"]
        # trainer.role = data["role"]
        trainer.attendance = data["attendance"]

        db.session.add(trainer)
        db.session.commit()

        return jsonify({
            "msg": "Trainer created"
        }), 200
    
@app.route('/routines', methods = ["POST","GET", "DELETE", "PUT"])
def routine():
    if request.method == "GET":
        routine = Routine.query.all()
        data = routine.to_dict()
        return data, 200
    
    if request.method == "POST":
        routine = Routine()
        data = request.get_json()
        print(data)
        routine.name = data["name"]
        routine.weekday = data["weekday"]
        routine.is_completed = data["is_completed"]
        routine.completed_percentage = data["completed_percentage"]
        routine.is_active = data["is_active"]
        routine.training_plan_id = data["training_plan_id"]
        routine.photo_link = data["photo_link"]
        db.session.add(routine)
        db.session.commit()

        return jsonify ({
            "msg": "New routine created"
        }), 200
    else:
        return jsonify ({
            "error": "Not valid"
        }), 400
    

#ejercicios

@app.route('/exercise', methods=['GET', "POST"])
@jwt_required()
def handle_exercise():
    if request.method == 'GET':
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if not user:
            return jsonify(message="User not found"), 404

       # Obtener todos los IDs de los planes de entrenamiento del usuario
        training_plan_ids = [plan.id for plan in Training_plan.query.filter_by(user_id=user.id).all()]

        # Obtener todos los IDs de las rutinas asociadas a esos planes de entrenamiento
        routine_ids = [routine.id for routine in Routine.query.filter(Routine.training_plan_id.in_(training_plan_ids)).all()]

        # Filtrar los ejercicios basados en esas rutinas
        exercises = Exercise.query.filter(Exercise.routine_id.in_(routine_ids)).all()
        exercises = list(map(lambda exercise: exercise.to_dict(), exercises))


        return jsonify({
            "data": exercises
        }), 200
    elif request.method == 'POST':
        exercise = Exercise()
        data = request.get_json()
        exercise.name = data["name"]
        exercise.description = data["description"]
        exercise.sets = data["sets"]
        exercise.repetitions = data["repetitions"]
        exercise.weight = data["weight"]
        exercise.is_completed = data["is_completed"]
        exercise.equipment_id = data.get("equipment_id")  # Usar get para evitar errores si la clave no existe
        exercise.equipment_issue = data["equipment_issue"]
        exercise.routine_id = data.get("routine_id")  # Usar get para evitar errores si la clave no existe
        exercise.photo_link = data["photo_link"]

        if not exercise.equipment_id:
            exercise.equipment_id = None
        if not exercise.routine_id:
            exercise.routine_id = None
        if not exercise.equipment_issue:
            exercise.equipment_issue = None

        db.session.add(exercise)
        db.session.commit()

        return jsonify({
            "msg": "Exercise added"
        }), 200



@app.route('/exercise/<int:id>', methods=['GET','PUT', 'DELETE'])
def update_exercise(id):
    if request.method == 'GET':
        exercise = Exercise.query.get(id)
        equipment = Equipment.query.get(exercise.equipment_id)          # Usamos el equipment_id para obtener el equipo asociado
        equipment_name = equipment.name if equipment else None

        routine = Routine.query.get(exercise.routine_id)
        routine_name = routine.name if routine else None

        data = exercise.to_dict()
        data["equipment_name"] = equipment_name
        data["routine_name"] = routine_name

        return data, 200
    elif request.method == 'DELETE':
        exercise = Exercise.query.get(id)
        if exercise is not None:
            db.session.delete(exercise)
            db.session.commit()

            return jsonify({
                "msg": "Exercise deleted"
            }), 202
        else:
            return jsonify({
                "error": "Exercise not found"
            }), 404
    elif request.method == 'PUT':
        exercise = Exercise.query.get(id)
        if exercise is not None:
            data = request.get_json()
            exercise.name = data["name"]
            exercise.description = data["description"]
            exercise.sets = data["sets"]
            exercise.repetitions = data["repetitions"]
            exercise.weight = data["weight"]
            exercise.is_completed = data["is_completed"]
            exercise.equipment_id = data["equipment_id"]
            exercise.equipment_issue = data["equipment_issue"]
            exercise.routine_id = data["routine_id"]
            exercise.photo_link = data["photo_link"]

            if not exercise.equipment_id:
                exercise.equipment_id = None
            if not exercise.routine_id:
                exercise.routine_id = None
            if not exercise.equipment_issue:
                exercise.equipment_issue = None

            db.session.commit()

            return jsonify({
                "msg": "Exercise updated"
            }), 200
        else:
            return jsonify({
                "error": "Exercise not found"
            }), 404




#rutina

@app.route('/routine', methods=['GET', "POST"])
def handle_routine():
    if request.method == 'GET':
        routines = Routine.query.all()
        routines = list(map(lambda routine: routine.to_dict(), routines))

        return jsonify({
            "data": routines
        }), 200
    elif request.method == 'POST':
        routine = Routine()
        data = request.get_json()
        routine.name = data["name"]
        routine.weekday = data["weekday"]
        routine.completed_percentage = data["completed_percentage"]
        routine.is_completed = data["is_completed"]
        routine.is_active = data["is_active"]
        routine.training_plan_id = data["training_plan_id"]
        routine.photo_link = data["photo_link"]


        db.session.add(routine)
        db.session.commit()

        return jsonify({
            "msg": "Routine added"
        }), 200

@app.route('/routine/<int:id>', methods=['GET','PUT', 'DELETE'])
def update_routine(id):
    if request.method == 'GET':
        routine = Routine.query.get(id)
        data = routine.to_dict()

        return data, 200
    elif request.method == 'DELETE':
        routine = Routine.query.get(id)
        if routine is not None:
            db.session.delete(routine)
            db.session.commit()

            return jsonify({
                "msg": "Routine deleted"
            }), 202
        else:
            return jsonify({
                "error": "Routine not found"
            }), 404
    elif request.method == 'PUT':
        routine = Routine.query.get(id)
        if routine is not None:
            data = request.get_json()
            routine.name = data["name"]
            routine.weekday = data["weekday"]
            routine.completed_percentage = data["completed_percentage"]
            routine.is_completed = data["is_completed"]
            routine.is_active = data["is_active"]
            routine.training_plan_id = data["training_plan_id"]
            routine.photo_link = data["photo_link"]


            db.session.commit()

            return jsonify({
                "msg": "Routine updated"
            }), 200
        else:
            return jsonify({
                "error": "Routine not found"
            }), 404
        

#plan de entrenamiento

@app.route('/trainingplan', methods=['GET', "POST"])
@jwt_required()                                         #@@@
def handle_training_plan():
    if request.method == 'GET':
        # Obtener el email del usuario logueado @@@
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify(message="User not found"), 404
        
        # Solo obtener los planes de entrenamiento del usuario logueado @@@
        training_plans = Training_plan.query.filter_by(user_id=user.id).all()
        training_plans = list(map(lambda training_plan: training_plan.to_dict(), training_plans))


        return jsonify({
            "data": training_plans
        }), 200
    elif request.method == 'POST':
        training_plan = Training_plan()
        data = request.get_json()
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        if user:
            user_id = user.id
        else:
            return jsonify(message="User not found"), 404

        training_plan.name = data["name"]
        training_plan.user_id = user_id                 #@@@
        training_plan.trainer_id = data["trainer_id"]
        training_plan.start_time = data["start_time"]
        training_plan.finish_time = data["finish_time"]
        training_plan.is_completed = data["is_completed"]
        training_plan.goal_name = data["goal_name"]
        training_plan.goal_description = data["goal_description"]
        training_plan.completed_percentage = data["completed_percentage"]
        training_plan.is_active = data["is_active"]
        training_plan.photo_link = data["photo_link"]


        if not training_plan.trainer_id:
            training_plan.trainer_id = None

        db.session.add(training_plan)
        db.session.commit()

        return jsonify({
            "msg": "Training plan added"
        }), 200

@app.route('/trainingplan/<int:id>', methods=['GET','PUT', 'DELETE'])
@jwt_required()                                         #@@@
def update_training_plan(id):
    if request.method == 'GET':
        training_plan = Training_plan.query.get(id)

        trainer = Trainer.query.get(training_plan.trainer_id)          # @@@
        trainer_name = trainer.name if trainer else None
        trainer_lastname = trainer.last_name if trainer else None

        user = User.query.get(training_plan.user_id)          # @@@
        user_name = user.name if user else None
        user_lastname = user.last_name if user else None


        data = training_plan.to_dict()
        data["trainer_name"] = trainer_name
        data["trainer_lastname"] = trainer_lastname
        data["user_name"] = user_name
        data["user_lastname"] = user_lastname


        return data, 200
    elif request.method == 'DELETE':
        training_plan = Training_plan.query.get(id)
        if training_plan is not None:
            db.session.delete(training_plan)
            db.session.commit()

            return jsonify({
                "msg": "Training plan deleted"
            }), 202
        else:
            return jsonify({
                "error": "Training plan not found"
            }), 404
    elif request.method == 'PUT':
        training_plan = Training_plan.query.get(id)
        if training_plan is not None:
            data = request.get_json()

            user_email = get_jwt_identity()
            user = User.query.filter_by(email=user_email).first()
            if user:
                user_id = user.id
            else:
                return jsonify(message="User not found"), 404
            
            training_plan.name = data["name"]
            training_plan.user_id = user_id
            training_plan.trainer_id = data["trainer_id"]
            training_plan.start_time = data["start_time"]
            training_plan.finish_time = data["finish_time"]
            training_plan.is_completed = data["is_completed"]
            training_plan.goal_name = data["goal_name"]
            training_plan.goal_description = data["goal_description"]
            training_plan.completed_percentage = data["completed_percentage"]
            training_plan.is_active = data["is_active"]
            training_plan.photo_link = data["photo_link"]


            db.session.commit()

            return jsonify({
                "msg": "Training plan updated"
            }), 200
        else:
            return jsonify({
                "error": "Training plan not found"
            }), 404





#no modificar desde este punto hacia abajo

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
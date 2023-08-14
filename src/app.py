import re
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.models import db, User, Trainer, Training_plan, Routine, Exercise, Equipment, Attendance
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
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
        #Regular expression that checks a valid email
        ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        #Regular expression that checks a valid password
        preg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        # Instancing the a new user
        user = User()
        data = request.get_json()
         #Checking email 
        if (re.search(ereg,data["email"])):
            user.email = data["email"]
        else:
            return "Invalid email format", 400
        #Checking password
        if (re.search(preg,data["password"])):
            password_hash = bcrypt.generate_password_hash(data["password"])
            user.password = password_hash
        else:
            return "Invalid password format", 400
        #Ask for everything else
        user.name = data["name"]
        user.last_name = data["last_name"]
        user.role = data["role"]
        user.trainer_id = data["trainer_id"]
        user.is_active = data["is_active"]
        user.subscription_date = data["subscription_date"]

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "msg": "user created"
        }), 200

@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = User.query.filter_by(email=email).first()
    if email is not None:
        current_password = user.password
        is_valid = bcrypt.check_password_hash(current_password, password)
        if is_valid:
            access_token = create_access_token(email)
            return jsonify({
                "access_token": access_token
            }), 200
        else:
            return jsonify({
                "msg": "invalid credentials"
            }), 400
    else:
        return jsonify({
            "msg": "invalid credentials"
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

        db.session.add(equipment)
        db.session.commit()

        return jsonify({
            "msg": "equipment added"
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
                "msg": "equipment deleted"
            }), 202
        else:
            return jsonify({
                "msg": "equipment not found"
            }), 404
    elif request.method == 'PUT':
        equipment = Equipment.query.get(id)
        if equipment is not None:
            data = request.get_json()
            equipment.name = data["name"]
            equipment.description = data["description"]
            equipment.status = data["status"]
            equipment.is_active = data["is_active"]

            db.session.commit()

            return jsonify({
                "msg": "equipment updated"
            }), 200
        else:
            return jsonify({
                "msg": "equipment not found"
            }), 404


#no modificar desde este punto hacia abajo

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
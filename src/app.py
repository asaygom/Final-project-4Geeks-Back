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
        user = User()
        data = request.get_json()
        user.name = data["name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.password = data["password"]
        user.role = data["role"]
        user.trainer_id = data["trainer_id"]
        user.is_active = data["is_active"]
        user.subscription_date = data["subscription_date"]

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "msg": "user created"
        }), 200

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
        
@app.route('/register', methods=["POST"])
def register():
    user = User()
    data = request.get_json()
    user.name = data["name"]
    user.last_name = data["last_name"]
    user.email = data["email"]
    password = data["password"]
    password_hash = bcrypt.generate_password_hash(password)
    user.password = password_hash
    user.role = data["role"]
    user.is_active = data["is_active"]
    user.subscription_date = data["subscription_date"]
    user.photo_link = data["photo_link"]

    db.session.add(user)
    db.session.commit()

    return jsonify({
       "msg": "user created"
        }), 200



#no modificar desde este punto hacia abajo

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
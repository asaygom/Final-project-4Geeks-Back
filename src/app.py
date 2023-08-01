from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.models import db, User, Trainer, Training_plan, Routine, Exercise, Equipment, Attendance
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:admin@localhost/postgres"
app.config["JWT_SECRET_KEY"] = "super-secret" #debemos cambiar esto al archivo .env y pensar un key
app.config['SECRET_KEY'] = "pass-key" #debemos cambiar esto al archivo .env y pensar un key
db.init_app(app)
migrate = Migrate(app,db)
CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

#empezamos a declarar nuestras rutas y metodos



#no modificar desde este punto hacia abajo

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
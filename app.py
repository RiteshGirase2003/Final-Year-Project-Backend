from flask import Flask
from worker_api.Routes.worker_routes import worker_bp
from multimeter_api.Routes.multimeter_routes import multimeter_bp
from db_connect import DB
from exception_handler import handle_validation_error, handle_generic_error
from pydantic import ValidationError
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()
access_token_expires = int(os.getenv("ACCESS_TOKEN_EXPIRES_IN"))
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=access_token_expires)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"

jwt = JWTManager(app)

app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(Exception, handle_generic_error)

app.register_blueprint(worker_bp)
app.register_blueprint(multimeter_bp)


@app.route("/")
def home():
    return "Welcome to the Flask API with MongoDB!"


if __name__ == "__main__":
    app.run(debug=True)

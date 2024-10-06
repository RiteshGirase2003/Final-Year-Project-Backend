from flask import Flask
from worker_api.Routes.worker_routes import worker_bp
from multimeter_api.Routes.multimeter_routes import multimeter_bp
from db_connect import DB
from exception_handler import handle_validation_error, handle_generic_error
from pydantic import ValidationError

app = Flask(__name__)

app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(Exception, handle_generic_error)

app.register_blueprint(worker_bp)
app.register_blueprint(multimeter_bp)


@app.route("/")
def home():
    return "Welcome to the Flask API with MongoDB!"


if __name__ == "__main__":
    app.run(debug=True)

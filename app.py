from flask import Flask
from worker_api.Routes.worker_routes import worker_bp
from multimeter_api.Routes.multimeter_routes import multimeter_bp
from db_connect import DB

app = Flask(__name__)

app.register_blueprint(worker_bp)
app.register_blueprint(multimeter_bp)

@app.route('/')
def home():
    return "Welcome to the Flask API with MongoDB!"

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from pymongo import MongoClient
from worker_api.get_worker import getWorker, getWorkerById, getWorkerByName
from worker_api.create_worker import createWorker
from worker_api.update_worker import updateWorker
from worker_api.delete_worker import deleteWorker
from multimeter_api.get_multimeter import getAllMultimeters, getMultimeterByModel
from multimeter_api.create_multimeter import createMultimeter
from multimeter_api.update_multimeter import updateMultimeter
from multimeter_api.delete_multimeter import deleteMultimeter


app = Flask(__name__)

# db_username = "cloudaids2022"
# db_password = "dAWvHdCbApKbNab7"
# connection_string = f"mongodb+srv://{db_username}:{db_password}@cluster0.v9pnh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(connection_string)
# DB = client['my_database']  


client = MongoClient('mongodb://localhost:27017/')
DB = client['Project']  


@app.route('/')
def home():
    return "Welcome to the Flask API with MongoDB!"

# Get all workers
@app.route('/workers', methods=['GET'])
def get_workers():
    data = getWorker(DB['Worker'])
    return data

# Get worker by name
@app.route('/workers/name/<string:name>', methods=['GET'])
def get_worker_by_name(name):
    data = getWorkerByName(DB['Worker'],name)
    return data

# Get worker by registration number
@app.route('/workers/regno/<string:reg_no>', methods=['GET'])
def get_worker_by_reg_no(reg_no):
    data = getWorkerById(DB['Worker'],reg_no)
    return data

# Add a new worker
@app.route('/worker', methods=['POST'])
def add_worker():
    new_worker = request.json
    data = createWorker(DB['Worker'],new_worker)
    return data

# Update worker by ID
@app.route('/worker/<string:reg_no>', methods=['PUT'])
def update_worker(reg_no):
    updated_data = request.json
    data = updateWorker(DB['Worker'], updated_data,reg_no)
    return data

# Delete worker by ID
@app.route('/workers/<string:reg_no>', methods=['DELETE'])
def delete_worker(reg_no):
    data = deleteWorker(DB['Worker'],reg_no)
    return data


# Get all multimeters
@app.route('/multimeters', methods=['GET'])
def get_multimeters():
    data = getAllMultimeters(DB['Multimeter'])
    return data

# Get multimeter by model
@app.route('/multimeters/model/<string:model>', methods=['GET'])
def get_multimeter_by_model(model):
    data = getMultimeterByModel(DB['Multimeter'], model)
    return data

# Add a new multimeter
@app.route('/multimeter', methods=['POST'])
def add_multimeter():
    new_multimeter = request.json
    data = createMultimeter(DB['Multimeter'], new_multimeter)
    return data

# Update multimeter by model
@app.route('/multimeter/<string:model>', methods=['PUT'])
def update_multimeter(model):
    updated_data = request.json
    data = updateMultimeter(DB['Multimeter'], updated_data, model)
    return data

# Delete multimeter by model
@app.route('/multimeter/<string:model>', methods=['DELETE'])
def delete_multimeter(model):
    data = deleteMultimeter(DB['Multimeter'], model)
    return data

if __name__ == '__main__':
    app.run(debug=True)

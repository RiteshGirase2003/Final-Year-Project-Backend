from flask import Blueprint, request
from db_connect import DB
from multimeter_api.services.get_multimeter import getAllMultimeters, getMultimeterByModel
from multimeter_api.services.create_multimeter import createMultimeter
from multimeter_api.services.update_multimeter import updateMultimeter
from multimeter_api.services.delete_multimeter import deleteMultimeter

multimeter_bp = Blueprint('multimeter_bp', __name__)

@multimeter_bp.route('/multimeters', methods=['GET'])
def get_multimeters():
    data = getAllMultimeters(DB['Multimeter'])
    return data

@multimeter_bp.route('/multimeters/model/<string:model>', methods=['GET'])
def get_multimeter_by_model(model):
    data = getMultimeterByModel(DB['Multimeter'], model)
    return data

@multimeter_bp.route('/multimeter', methods=['POST'])
def add_multimeter():
    new_multimeter = request.json
    data = createMultimeter(DB['Multimeter'], new_multimeter)
    return data

@multimeter_bp.route('/multimeter/<string:model>', methods=['PUT'])
def update_multimeter(model):
    updated_data = request.json
    data = updateMultimeter(DB['Multimeter'], updated_data, model)
    return data

@multimeter_bp.route('/multimeter/<string:model>', methods=['DELETE'])
def delete_multimeter(model):
    data = deleteMultimeter(DB['Multimeter'], model)
    return data
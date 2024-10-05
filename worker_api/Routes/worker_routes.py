from flask import Blueprint, request
from db_connect import DB
from worker_api.services.get_worker import getWorker, getWorkerById, getWorkerByName
from worker_api.services.create_worker import createWorker
from worker_api.services.update_worker import updateWorker
from worker_api.services.delete_worker import deleteWorker

worker_bp = Blueprint('worker_bp', __name__)

@worker_bp.route('/workers', methods=['GET'])
def get_workers():
    data = getWorker(DB['Worker'])
    return data

@worker_bp.route('/workers/name/<string:name>', methods=['GET'])
def get_worker_by_name(name):
    data = getWorkerByName(DB['Worker'], name)
    return data

@worker_bp.route('/workers/reg_no/<string:reg_no>', methods=['GET'])
def get_worker_by_reg_no(reg_no):
    data = getWorkerById(DB['Worker'], reg_no)
    return data

@worker_bp.route('/worker', methods=['POST'])
def add_worker():
    new_worker = request.json
    data = createWorker(DB['Worker'], new_worker)
    return data

@worker_bp.route('/worker/<string:reg_no>', methods=['PUT'])
def update_worker(reg_no):
    updated_data = request.json
    data = updateWorker(DB['Worker'], updated_data, reg_no)
    return data

@worker_bp.route('/workers/<string:reg_no>', methods=['DELETE'])
def delete_worker(reg_no):
    data = deleteWorker(DB['Worker'], reg_no)
    return data
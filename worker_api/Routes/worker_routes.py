from flask import Blueprint, request
from db_connect import DB as db
from worker_api.services.worker_service import (
    getWorkers,
    createWorker,
    updateWorker,
    deleteWorker,
)

worker_bp = Blueprint("worker_bp", __name__)


@worker_bp.route("/workers", methods=["GET"])
def get_workers():
    return getWorkers(db["Worker"])


@worker_bp.route("/worker", methods=["POST"])
def add_worker():
    new_worker = request.json
    return createWorker(db["Worker"], new_worker)


@worker_bp.route("/worker/<string:id>", methods=["PUT"])
def update_worker(id):
    return updateWorker(db["Worker"], id)


@worker_bp.route("/worker/<string:id>", methods=["DELETE"])
def delete_worker(id):
    return deleteWorker(db["Worker"], id)

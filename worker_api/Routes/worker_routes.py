from flask import Blueprint, request
from db_connect import DB as db
from worker_api.services.worker_service import (
    getWorkers,
    createWorker,
    updateWorker,
    deleteWorker,
    loginUser,
    refreshAccessToken,
    logoutUser,
)
from middleware.auth import jwt_required
from worker_api.dto.req.create_worker_dto import UserRole

worker_bp = Blueprint("worker_bp", __name__)


@worker_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user_role = request.args.get("user_role")
    if user_role not in UserRole:
        raise Exception("Invalid user role!")
    return loginUser(db["Worker"], data, user_role)


@worker_bp.route("/refresh", methods=["POST"])
def refresh():
    return refreshAccessToken(db["Worker"])


@worker_bp.route("/workers", methods=["GET"])
@jwt_required
def get_workers():
    return getWorkers(db["Worker"])


@worker_bp.route("/worker", methods=["POST"])
def add_worker():
    new_worker = request.json
    return createWorker(db["Worker"], new_worker)


@worker_bp.route("/worker/<string:id>", methods=["PUT"])
@jwt_required
def update_worker(id):
    return updateWorker(db["Worker"], id)


@worker_bp.route("/worker/<string:id>", methods=["DELETE"])
@jwt_required
def delete_worker(id):
    return deleteWorker(db["Worker"], id)

@worker_bp.route("/logout", methods=["GET"])
@jwt_required
def logout():
    return logoutUser(db["Worker"])

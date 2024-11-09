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
    loggedInWorker,
)
from middleware.auth import jwt_required, check_role
from worker_api.dto.req.create_worker_dto import UserRole

worker_bp = Blueprint("worker_bp", __name__)


@worker_bp.route("/me", methods=["GET"])
@jwt_required
def get_me():
    return loggedInWorker(db["Worker"])


@worker_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    return loginUser(db["Worker"], data)


@worker_bp.route("/refresh", methods=["GET"])
def refresh():
    return refreshAccessToken(db["Worker"])


@worker_bp.route("/workers", methods=["GET"])
@jwt_required
@check_role("admin")
def get_workers():
    return getWorkers(db["Worker"])


@worker_bp.route("/worker", methods=["POST"])
@jwt_required
@check_role("admin")
def add_worker():
    new_worker = request.form.to_dict()
    return createWorker(db["Worker"], new_worker)


@worker_bp.route("/worker/<string:id>", methods=["PUT"])
@jwt_required
@check_role("admin")
def update_worker(id):
    return updateWorker(db["Worker"], id)


@worker_bp.route("/worker/<string:id>", methods=["DELETE"])
@jwt_required
@check_role("admin")
def delete_worker(id):
    return deleteWorker(db["Worker"], id)


@worker_bp.route("/logout", methods=["GET"])
@jwt_required
def logout():
    return logoutUser(db["Worker"])

from flask import Blueprint, request
from db_connect import DB as db
from middleware.auth import jwt_required, check_role
from flask_jwt_extended import get_jwt_identity
from results_api.services.results_service import (
    create_inspection,
    get_inspections,
    delete_inspection,
)

results_bp = Blueprint("results_bp", __name__)


@results_bp.route("/getInspections", methods=["GET"])
@jwt_required
def inspections():
    return get_inspections(db)


@results_bp.route("/inspect", methods=["POST"])
@jwt_required
def inspect():
    worker_id = get_jwt_identity()["worker_id"]
    data = request.json
    data["worker_id"] = worker_id
    return create_inspection(db, data)


@results_bp.route("/remove_inspection/<string:inspection_id>", methods=["DELETE"])
@jwt_required
@check_role('admin')
def remove_inspection(inspection_id):
    return delete_inspection(db, inspection_id)


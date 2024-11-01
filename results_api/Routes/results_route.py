from flask import Blueprint, request
from db_connect import DB as db
from middleware.auth import jwt_required
from results_api.services.results_service import create_inspection, get_inspections

results_bp = Blueprint("results_bp", __name__)


@results_bp.route("/getInspections", methods=["GET"])
@jwt_required
def inspections():
    return get_inspections(db)


@results_bp.route("/inspect", methods=["POST"])
@jwt_required
def inspect():
    return create_inspection(db, request.json)

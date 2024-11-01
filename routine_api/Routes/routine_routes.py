from flask import Blueprint, request
from db_connect import DB as db
from middleware.auth import jwt_required
from routine_api.services.routine_service import getRoutines

routine_bp = Blueprint("routine_bp", __name__)


@routine_bp.route("/getRoutines", methods=["GET"])
@jwt_required
def get_routines():
    return getRoutines(db)

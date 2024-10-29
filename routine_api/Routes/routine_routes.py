from flask import Blueprint, request
from db_connect import DB as db
from middleware.auth import jwt_required
from routine_api.services.routine_service import sendMessage

routine_bp = Blueprint("routine_bp", __name__)


@routine_bp.route("/hello", methods=["GET"])
def hello_world():
    return sendMessage()

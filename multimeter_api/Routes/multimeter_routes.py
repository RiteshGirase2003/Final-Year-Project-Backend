from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from db_connect import DB
from multimeter_api.services.multimeter_service import (
    createMultimeter,
    getMultimeters,
    updateMultimeter,
    deleteMultimeter,
)
from middleware.auth import jwt_required

multimeter_bp = Blueprint("multimeter_bp", __name__)


@multimeter_bp.route("/multimeters", methods=["GET"])
def get_multimeters():
    data = getMultimeters(DB["Multimeter"])
    return data


@multimeter_bp.route("/multimeter", methods=["POST"])
@jwt_required
def add_multimeter():
    new_multimeter = request.json
    worker_id = get_jwt_identity()["worker_id"]
    new_multimeter["created_by"] = worker_id
    data = createMultimeter(DB["Multimeter"], new_multimeter)
    return data


@multimeter_bp.route("/multimeter/<string:id>", methods=["PUT"])
@jwt_required
def update_multimeter(id):
    updated_data = request.json
    data = updateMultimeter(DB["Multimeter"], updated_data, id)
    return data


@multimeter_bp.route("/multimeter/<string:id>", methods=["DELETE"])
@jwt_required
def delete_multimeter(id):
    data = deleteMultimeter(DB["Multimeter"], id)
    return data

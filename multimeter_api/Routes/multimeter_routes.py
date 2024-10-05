from flask import Blueprint, request
from db_connect import DB
from multimeter_api.services.multimeter_service import (
    createMultimeter,
    getMultimeters,
    updateMultimeter,
    deleteMultimeter,
)

multimeter_bp = Blueprint("multimeter_bp", __name__)


@multimeter_bp.route("/multimeters", methods=["GET"])
def get_multimeters():
    print("Request")
    data = getMultimeters(DB["Multimeter"])
    return data


@multimeter_bp.route("/multimeter", methods=["POST"])
def add_multimeter():
    new_multimeter = request.json
    data = createMultimeter(DB["Multimeter"], new_multimeter)
    return data


@multimeter_bp.route("/multimeter/<string:id>", methods=["PUT"])
def update_multimeter(id):
    updated_data = request.json
    data = updateMultimeter(DB["Multimeter"], updated_data, id)
    return data


@multimeter_bp.route("/multimeter/<string:id>", methods=["DELETE"])
def delete_multimeter(id):
    data = deleteMultimeter(DB["Multimeter"], id)
    return data

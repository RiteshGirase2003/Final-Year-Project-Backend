from flask import Blueprint, request
from db_connect import DB as db
from middleware.auth import jwt_required, check_role
from flask_jwt_extended import get_jwt_identity
from os import getenv
from results_api.services.results_service import (
    create_inspection,
    get_inspections,
    delete_inspection,
    getNumbers,
    checkMeter,
    export_today_results,
    send_email,
)

results_bp = Blueprint("results_bp", __name__)


@results_bp.route("/getInspections", methods=["GET"])
@jwt_required
def inspections():
    worker_id = get_jwt_identity()["worker_id"]
    return get_inspections(db, worker_id)


@results_bp.route("/inspect", methods=["POST"])
@jwt_required
def inspect():
    worker_id = get_jwt_identity()["worker_id"]
    data = request.json
    data["worker_id"] = worker_id
    return create_inspection(db, data)


@results_bp.route("/remove_inspection/<string:inspection_id>", methods=["DELETE"])
@jwt_required
@check_role("admin")
def remove_inspection(inspection_id):
    return delete_inspection(db, inspection_id)


@results_bp.route("/analytics/numbers", methods=["GET"])
@jwt_required
def getAnalytics():
    worker_id = get_jwt_identity()["worker_id"]
    return getNumbers(db, worker_id)


@results_bp.route("/check", methods=["POST"])
@jwt_required
def check():
    return checkMeter(db)


@results_bp.route("/excel", methods=["GET"])
@jwt_required
def download_excel():
    return export_today_results(db)


@results_bp.route("/send_email", methods=["POST"])
@jwt_required
def emailSender():
    email_service_url = getenv("SMTP_HOST")
    port = getenv("SMTP_PORT")
    sender_email = getenv("SMTP_USER")
    sender_pass = getenv("SMTP_PASS")
    receipant_emails = request.args.get("email")
    print(receipant_emails)
    return send_email(
        email_service_url, port, sender_email, sender_pass, receipant_emails
    )

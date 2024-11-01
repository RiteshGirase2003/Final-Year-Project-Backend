from flask import jsonify
from results_api.dto.request.results_request_dto import ResultsRequestDTO
from bson import ObjectId
from datetime import datetime

""" Create and update inspection """


def create_inspection(DB, data):
    data = ResultsRequestDTO(**data)
    meter = DB["Multimeter"].find_one(
        {"_id": ObjectId(data.meter_id), "is_active": True}
    )
    if not meter:
        return jsonify({"message": "Meter not found"}), 404
    worker = DB["Worker"].find_one({"_id": ObjectId(data.worker_id), "is_active": True})
    if not worker:
        return jsonify({"message": "Worker not found"}), 404
    existing_result = DB["Result"].find_one(
        {"meter_id": data.meter_id, "worker_id": data.worker_id}
    )
    if existing_result:
        DB["Result"].update_one(
            {"meter_id": data.meter_id, "worker_id": data.worker_id},
            {"$set": {"status": data.status, "date": datetime.now()}},
        )
        return jsonify({"message": "Inspection updated successfully"}), 200
    inspection = {
        "meter_id": data.meter_id,
        "worker_id": data.worker_id,
        "status": data.status,
        "date": datetime.now(),
        "time": datetime.now(),
    }
    DB["Result"].insert_one(inspection)
    print("Inspection Created")
    return jsonify({"message": "Inspection created successfully"}), 201


def get_inspections(DB):
    inspections = DB["Result"].find()
    formatted = []
    for inspection in inspections:
        inspection["_id"] = str(inspection["_id"])
        inspection["meter_id"] = str(inspection["meter_id"])
        inspection["worker_id"] = str(inspection["worker_id"])
        formatted.append(inspection)
    return jsonify({"inspections": list(formatted)}), 200


def delete_inspection(DB, inspection_id):
    inspection = DB["Result"].find_one({"_id": ObjectId(inspection_id)})
    if not inspection:
        raise Exception("Inspection Not Found!")

    DB["Result"].delete_one({"_id": ObjectId(inspection_id)})
    return jsonify({"message": "Inspection deleted successfully!"}), 200

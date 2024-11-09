from flask import jsonify, request
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
    }
    DB["Result"].insert_one(inspection)
    return jsonify({"message": "Inspection created successfully"}), 201


def get_inspections(DB):
    worker_id = request.args.get("worker_id")
    query = {}
    if worker_id:
        query["worker_id"] = worker_id
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    inspections = DB["Result"].find(query).skip((page - 1) * limit).limit(limit)
    formatted = []
    for inspection in inspections:
        inspection["_id"] = str(inspection["_id"])
        inspection["meter_id"] = str(inspection["meter_id"])
        inspection["worker_id"] = str(inspection["worker_id"])
        formatted.append(inspection)
    return (
        jsonify(
            {
                "data": formatted,
                "total": DB["Result"].count_documents({}),
                "page": page,
                "limit": limit,
            }
        ),
        200,
    )


def delete_inspection(DB, inspection_id):
    inspection = DB["Result"].find_one({"_id": ObjectId(inspection_id)})
    if not inspection:
        raise Exception("Inspection Not Found!")

    DB["Result"].delete_one({"_id": ObjectId(inspection_id)})
    return jsonify({"message": "Inspection deleted successfully!"}), 200

from flask import jsonify, request
from results_api.dto.request.results_request_dto import ResultsRequestDTO
from bson import ObjectId
from datetime import datetime
import dateutil.parser
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


def get_inspections(DB, worker_id):
    query = {}
    if worker_id:
        query["worker_id"] = worker_id
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    pipeline = [
        {"$match": query},
        {"$addFields": {"meter_id": {"$toObjectId": "$meter_id"}}},
        {
            "$lookup": {
                "from": "Multimeter",
                "localField": "meter_id",
                "foreignField": "_id",
                "as": "meter_details",
            }
        },
        {"$unwind": "$meter_details"},
        {"$skip": (page - 1) * limit},
        {"$limit": limit},
    ]

    inspections = list(DB["Result"].aggregate(pipeline))
    formatted = []
    for inspection in inspections:
        inspection["_id"] = str(inspection["_id"])
        inspection["meter_id"] = str(inspection["meter_id"])
        inspection["worker_id"] = str(inspection["worker_id"])
        inspection["meter_details"]["_id"] = str(inspection["meter_details"]["_id"])
        formatted.append(inspection)

    total = DB["Result"].count_documents(query)

    return (
        jsonify({"data": formatted, "total": total, "page": page, "limit": limit}),
        200,
    )


def delete_inspection(DB, inspection_id):
    inspection = DB["Result"].find_one({"_id": ObjectId(inspection_id)})
    if not inspection:
        raise Exception("Inspection Not Found!")

    DB["Result"].delete_one({"_id": ObjectId(inspection_id)})
    return jsonify({"message": "Inspection deleted successfully!"}), 200


def getNumbers(DB, worker_id):
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    meter_type = request.args.get("meter_type")
    query = {}
    query["worker_id"] = worker_id
    if start_date:
        start_date = dateutil.parser.parse(start_date)
        query["date"] = {"$gte": start_date}
    if end_date:
        end_date = dateutil.parser.parse(end_date)
        if "date" in query:
            query["date"]["$lte"] = end_date
        else:
            query["date"] = {"$lte": end_date}

    if meter_type:
        query["meter_type"] = meter_type
    total_meters = DB["Result"].count_documents(query)
    correct_meters = DB["Result"].count_documents({**query, "status": "pass"})
    incorrect_meters = DB["Result"].count_documents({**query, "status": "fail"})
    return (
        jsonify(
            {
                "total": total_meters,
                "correct": correct_meters,
                "incorrect": incorrect_meters,
            }
        ),
        200,
    )

from flask import jsonify, request
import re
from worker_api.schema.worker_schema import Worker
from bson.objectid import ObjectId
from datetime import datetime

""" Create Worker """


def createWorker(DB, worker):
    try:
        existing_worker = DB.find_one({"reg_no": worker["reg_no"]})
        if existing_worker:
            return jsonify({"error": "Worker already exists with this Reg. No."}), 400
        DB.insert_one(
            {
                "name": worker["name"],
                "reg_no": worker["reg_no"],
                "password": worker["password"],
                "photo": worker["photo"],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )

        return jsonify({"message": "Worker created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


""" Get Worker """


def getWorkers(DB):
    reg_no = request.args.get("reg_no")
    name = request.args.get("name")

    query = {}
    if reg_no:
        query["reg_no"] = int(reg_no)
    if name:
        name = name.strip('"')
        query["name"] = {"$regex": name, "$options": "i"}
    workers = DB.find(query)
    workers_list = list(workers)

    if workers_list:
        results = []
        for worker in workers_list:
            worker_data = Worker(
                id=str(worker["_id"]),
                name=worker["name"],
                reg_no=worker["reg_no"],
                password=worker["password"],
                photo=worker["photo"],
            )
            results.append(worker_data.dict())
        return jsonify(results)
    else:
        return jsonify({"error": "Worker not found"}), 404


""" Update Worker """


def updateWorker(DB, id):
    try:
        updated_data = request.json
        if not updated_data:
            return (
                jsonify({"error": "Data is required in the request body"}),
                400,
            )
        id = ObjectId(id)
        existing_worker = DB.find_one({"_id": id})
        if not existing_worker:
            return jsonify({"error": "Worker not found"}), 404
        updated_data["updated_at"] = datetime.now()
        DB.find_one_and_update({"_id": id}, {"$set": updated_data})
        return jsonify({"message": "Worker updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


""" Delete Worker """


def deleteWorker(DB, id):
    try:
        DB.find_one_and_delete({"_id": ObjectId(id)})
        return jsonify({"message": "Worker deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

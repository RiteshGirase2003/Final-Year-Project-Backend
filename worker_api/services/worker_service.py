from flask import jsonify, request
import re
from worker_api.schema.worker_schema import Worker
from bson.objectid import ObjectId
from datetime import datetime
from worker_api.dto.req.create_worker_dto import CreateWorkerDTO
from worker_api.dto.res.worker_res_dto import WorkerResDTO
from worker_api.dto.req.update_worker_dto import UpdateWorkerDTO
from pydantic import ValidationError

""" Create Worker """


def createWorker(DB, worker: CreateWorkerDTO):
    worker = CreateWorkerDTO(**worker)
    existing_worker = DB.find_one({"reg_no": worker.reg_no})
    if existing_worker:
        raise (Exception("Worker with this registration number already exists!"))
    worker.created_at = datetime.now()
    worker.updated_at = datetime.now()
    DB.insert_one(worker.dict())
    return jsonify({"message": "Worker created successfully"}), 201


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
    results = []
    if workers_list:
        for worker in workers_list:
            worker_data = WorkerResDTO(
                id=str(worker["_id"]),
                name=worker["name"],
                reg_no=worker["reg_no"],
                password=worker["password"],
                photo=worker["photo"],
                created_at=worker["created_at"],
                updated_at=worker["updated_at"],
            )
            results.append(worker_data.dict())
    if len(results) == 0:
        raise (Exception("No worker found!"))
    return jsonify(results), 200


""" Update Worker """


def updateWorker(DB, id):

    updated_data = request.json
    if not updated_data:
        raise (Exception("No data found to update"))
    id = ObjectId(id)
    existing_worker = DB.find_one({"_id": id})
    if not existing_worker:
        raise (Exception("Worker not found!"))
    updated_worker_data = UpdateWorkerDTO(**updated_data)
    updated_data_dict = updated_worker_data.dict(exclude_unset=True)
    updated_data_dict["updated_at"] = datetime.now()
    DB.find_one_and_update({"_id": id}, {"$set": updated_data})
    return jsonify({"message": "Worker updated successfully"}), 200


""" Delete Worker """


def deleteWorker(DB, id):
    id = ObjectId(id)
    existing_worker = DB.find_one({"_id": id})
    if not existing_worker:
        raise (Exception("Worker not found!"))
    DB.find_one_and_delete({"_id": id})
    return jsonify({"message": "Worker deleted successfully"}), 200

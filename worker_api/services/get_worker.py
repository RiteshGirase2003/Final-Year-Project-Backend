from flask import jsonify
import re
from worker_api.schema.worker_schema import Worker

def getWorker(DB):
    workers = []
    for worker in DB.find():
        worker_data = Worker(
            id=str(worker["_id"]),
            name=worker["name"],
            reg_no=worker["reg_no"],
            password=worker["password"],
            photo=worker["photo"],
        )
        workers.append(worker_data.dict())
    return jsonify(workers)


def getWorkerById(DB, reg_no):
    workers = DB.find({"Reg_No": {"$regex": re.compile(reg_no, re.IGNORECASE)}})
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


def getWorkerByName(DB, name):
    workers = DB.find({"name": {"$regex": re.compile(name, re.IGNORECASE)}})
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

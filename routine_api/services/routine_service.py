from bson import ObjectId
from flask import jsonify
from datetime import datetime, date, time
from routine_api.schema.routine_schema import Routine


def updateRoutine(DB, worker_id):
    current_datetime = datetime.now()
    current_date = current_datetime.date()

    start_of_day = datetime.combine(current_date, time.min)
    end_of_day = datetime.combine(current_date, time.max)

    existing_routine = DB["Routine"].find_one(
        {"worker_id": worker_id, "date": {"$gte": start_of_day, "$lt": end_of_day}}
    )
    if existing_routine:
        DB["Routine"].update_one(
            {"_id": existing_routine["_id"]},
            {"$set": {"end_time": current_datetime}},
        )
        return

    worker = DB["Worker"].find_one({"_id": ObjectId(worker_id)})
    if not worker:
        raise Exception("Worker not found!")

    routine = {
        "worker_id": worker_id,
        "date": start_of_day,
        "start_time": current_datetime,
        "end_time": None,
    }

    DB["Routine"].insert_one(routine)
    return


def getRoutines(DB):
    """query_filter = {}
    worker_id = request.args.get("worker_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if worker_id:
        query_filter["worker_id"] = worker_id
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        if start_date > end_date:
            return jsonify({"msg": "Invalid date range"}), 400
        query_filter["date"] = {"$gte": start_date, "$lte": end_date}
    if start_date and not end_date:
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        query_filter["date"] = {"$gte": start_date}
    if end_date and not start_date:
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        query_filter["date"] = {"$lte": end_date}
    """
    routines = list(DB["Routine"].find())

    formatted_routines = []

    for routine in routines:
        routine["_id"] = str(routine["_id"])
        routine["worker_id"] = str(routine["worker_id"])
        routine = Routine(**routine)
        routine_dict = routine.dict(by_alias=True)
        routine_dict["date"] = routine_dict["date"].strftime("%d-%m-%Y")
        routine_dict["start_time"] = routine_dict["start_time"].strftime("%H:%M:%S")
        if routine_dict["end_time"]:
            routine_dict["end_time"] = routine_dict["end_time"].strftime("%H:%M:%S")
        formatted_routines.append(routine_dict)

    return jsonify(formatted_routines), 200

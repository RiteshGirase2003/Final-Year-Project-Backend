from bson import ObjectId
from flask import jsonify
from datetime import datetime, date, time
from routine_api.schema.routine_schema import Routine


def updateRoutine(DB, worker_id):
    print("*********Update Routine*********")
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
    print("Routine Updated")


def getRoutines(DB, query):
    query_filter = {
        
    }
    if query.get("date"):
        query_filter["date"] = query.get("date")
    if query.get("worker_id"):
        query_filter["worker_id"] = query.get("worker_id")
    if query.get("start_date") and query.get("end_date"):
        start_date = datetime.strptime(query.get("start_date"), "%d-%m-%Y").date()
        end_date = datetime.strptime(query.get("end_date"), "%d-%m-%Y").date()
        query_filter["date"] = {"$gte": start_date, "$lte": end_date}
    if query.get("start_date") and not query.get("end_date"):
        start_date = datetime.strptime(query.get("start_date"), "%d-%m-%Y").date()
        query_filter["date"] = {"$gte": start_date}
    if query.get("end_date") and not query.get("start_date"):
        end_date = datetime.strptime(query.get("end_date"), "%d-%m-%Y").date()
        query_filter["date"] = {"$lte": end_date}

    routines = list(
        DB["Routine"].find(
            query_filter,
        )
    )
    formatted_routines = []
    for routine in routines:
        routine = Routine(**routine)
        routine_dict = routine.dict()
        routine["date"] = routine["date"].strftime("%d-%m-%Y")
        routine_dict["start_time"] = routine_dict["start_time"].strftime("%H:%M:%S")
        if routine_dict["end_time"]:
            routine_dict["end_time"] = routine_dict["end_time"].strftime("%H:%M:%S")
        formatted_routines.append(routine_dict)
    return jsonify(formatted_routines), 200

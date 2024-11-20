from bson import ObjectId
from flask import jsonify, request
from datetime import datetime, date, time
from routine_api.schema.routine_schema import Routine
import dateutil.parser
import random


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
    query_filter = {}
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    worker_id = request.args.get("worker_id")
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")

    if worker_id:
        query_filter["worker_id"] = worker_id
    if start_date and end_date:
        start_date = dateutil.parser.parse(start_date)
        end_date = dateutil.parser.parse(end_date)
        if start_date > end_date:
            raise Exception("Invalid date range")
        query_filter["date"] = {"$gte": start_date, "$lte": end_date}
    if start_date and not end_date:
        raise Exception("End date is required")
    if end_date and not start_date:
        raise Exception("Start date is required")

    pipeline = [
        {"$match": query_filter},
        {
            "$addFields": {
                "worker_id": {"$toObjectId": "$worker_id"},
                "total_hours": {
                    "$divide": [{"$subtract": ["$end_time", "$start_time"]}, 3600000]
                },  # Convert milliseconds to hours
            }
        },
        {
            "$lookup": {
                "from": "Worker",
                "localField": "worker_id",
                "foreignField": "_id",
                "as": "worker",
            }
        },
        {"$unwind": "$worker"},
        {"$sort": {"date": 1}},
        {"$skip": (page - 1) * limit},
        {"$limit": limit},
        {
            "$project": {
                "_id": 1,
                "worker_id": 1,
                "total_hours": 1,
                "start_time": 1,
                "end_time": 1,
                "date": 1,
                "worker.name": 1,
                "worker.reg_no": 1,
            }
        },
    ]

    routines = list(DB["Routine"].aggregate(pipeline))
    formatted_routines = []

    for routine in routines:
        routine["_id"] = str(routine["_id"])
        routine["worker_id"] = str(routine["worker_id"])
        routine["worker_name"] = routine["worker"]["name"]
        routine["worker_reg_no"] = routine["worker"]["reg_no"]
        routine = Routine(**routine)
        routine_dict = routine.dict(by_alias=True)
        routine_dict["date"] = routine_dict["date"].strftime("%d-%m-%Y")
        routine_dict["start_time"] = routine_dict["start_time"].strftime("%I:%M:%S %p")
        if routine_dict["end_time"]:
            routine_dict["end_time"] = routine_dict["end_time"].strftime("%I:%M:%S %p")
        formatted_routines.append(routine_dict)

    total = DB["Routine"].count_documents(query_filter)

    return (
        jsonify(
            {
                "data": formatted_routines,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                },
            }
        ),
        200,
    )

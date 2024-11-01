from flask import jsonify, request, make_response
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from worker_api.dto.req.create_worker_dto import CreateWorkerDTO
from worker_api.dto.res.worker_res_dto import WorkerResDTO
from worker_api.dto.req.update_worker_dto import UpdateWorkerDTO
import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
import jwt
import os

refresh_token_expires = int(os.getenv("REFRESH_TOKEN_EXPIRES_IN"))

""" Login Admin and Login Worker"""


def loginUser(DB, data):
    user = DB.find_one({"reg_no": data["reg_no"], "is_active": True})
    if not user:
        raise Exception("Registration number does not exist!")
    if not bcrypt.checkpw(
        data["password"].encode("utf-8"), user["password"].encode("utf-8")
    ):
        raise Exception("Password is incorrect!")
    user_id = str(user["_id"])
    access_token = create_access_token(
        identity={
            "worker_id": user_id,
            "reg_no": user["reg_no"],
            "role": user["user_role"],
        }
    )
    refresh_token = create_refresh_token(
        identity={
            "worker_id": user_id,
            "reg_no": user["reg_no"],
            "role": user["user_role"],
        }
    )
    DB.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "refresh_token.token": refresh_token,
                "refresh_token.expires_at": datetime.now()
                + timedelta(minutes=refresh_token_expires),
            }
        },
    )
    response = make_response(
        jsonify({"message": f"{user["user_role"]} logged in successfully"}), 200
    )
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return response


""" Create Worker """


def createWorker(DB, worker: CreateWorkerDTO):
    worker = CreateWorkerDTO(**worker)
    existing_worker = DB.find_one({"reg_no": worker.reg_no, "is_active": True})
    if existing_worker:
        raise Exception("Worker with this registration number already exists!")
    hashed_password = bcrypt.hashpw(worker.password.encode("utf-8"), bcrypt.gensalt())
    worker.password = hashed_password.decode("utf-8")
    result = DB.insert_one(worker.dict())
    user = DB.find_one({"_id": result.inserted_id})
    user_id = str(user["_id"])
    access_token = create_access_token(
        identity={
            "worker_id": user_id,
            "reg_no": user["reg_no"],
            "role": user["user_role"],
        }
    )
    refresh_token = create_refresh_token(
        identity={
            "worker_id": user_id,
            "reg_no": user["reg_no"],
            "role": user["user_role"],
        }
    )
    DB.update_one(
        {"_id": result.inserted_id},
        {
            "$set": {
                "refresh_token": {
                    "token": refresh_token,
                    "expires_at": datetime.now()
                    + timedelta(minutes=refresh_token_expires),
                }
            }
        },
    )
    response = make_response(jsonify({"message": "Worker created successfully"}), 201)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return response


""" Get Worker """


def getWorkers(DB):

    reg_no = request.args.get("reg_no")
    name = request.args.get("name")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", "asc")

    match_stage = {"is_active": True}
    if reg_no:
        match_stage["reg_no"] = int(reg_no)
    if name:
        name = name.strip('"')
        match_stage["name"] = {"$regex": name, "$options": "i"}

    sort_stage = {}
    if sort_by in ["name", "reg_no"]:
        sort_stage[sort_by] = 1 if sort_order == "asc" else -1

    pipeline = [{"$match": match_stage}]
    if sort_stage:
        pipeline.append({"$sort": sort_stage})

    workers = list(DB.aggregate(pipeline))
    results = []

    if workers:
        for worker in workers:
            worker_data = WorkerResDTO(
                id=str(worker["_id"]), **{k: v for k, v in worker.items() if k != "_id"}
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
    existing_worker = DB.find_one({"_id": id, "is_active": True})
    if not existing_worker:
        raise (Exception("Worker not found!"))
    updated_worker_data = UpdateWorkerDTO(**updated_data)
    updated_data_dict = updated_worker_data.dict()
    DB.find_one_and_update({"_id": id}, {"$set": updated_data_dict})
    return jsonify({"message": "Worker updated successfully"}), 200


""" Delete Worker """


def deleteWorker(DB, id):
    id = ObjectId(id)
    existing_worker = DB.find_one({"_id": id, "is_active": True})
    if not existing_worker:
        raise (Exception("Worker not found!"))
    DB.find_one_and_update(
        {"_id": id}, {"$set": {"is_active": False, "updated_at": datetime.now()}}
    )
    return jsonify({"message": "Worker deleted successfully"}), 200


""" Refresh Access Token """


def refreshAccessToken(DB):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise Exception("No refresh token found!")

    try:
        decoded_token = jwt.decode(
            refresh_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token has expired!")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refresh token!")

    if (
        "sub" not in decoded_token
        or "worker_id" not in decoded_token["sub"]
        or "role" not in decoded_token["sub"]
    ):
        raise Exception("Invalid refresh token payload!")

    worker_id = ObjectId(decoded_token["sub"]["worker_id"])
    user_role = decoded_token["sub"]["role"]
    worker = DB.find_one(
        {"_id": worker_id, "is_active": True, "user_role": str(user_role)}
    )
    if not worker:
        raise Exception("Worker not found!")

    if "refresh_token" not in worker or "expires_at" not in worker["refresh_token"]:
        raise Exception("Invalid worker data: missing refresh token expiration")

    if datetime.now() > worker["refresh_token"]["expires_at"]:
        raise Exception("Refresh token has expired!")

    access_token = create_access_token(
        identity={
            "worker_id": str(worker_id),
            "reg_no": worker["reg_no"],
            "role": str(user_role),
        }
    )
    DB.update_one(
        {"_id": worker_id},
        {
            "$set": {
                "refresh_token.token": refresh_token,
                "refresh_token.expires_at": datetime.now()
                + timedelta(minutes=refresh_token_expires),
            }
        },
    )
    response = make_response(jsonify({"message": "Access token refreshed"}), 200)
    response.set_cookie("access_token", access_token, httponly=True)
    return response


""" Logout Worker and Logout Admin """


def logoutUser(DB):
    access_token = request.cookies.get("access_token")
    try:
        decoded_token = jwt.decode(
            access_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise Exception("Access token has expired!")
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token!")

    if (
        "sub" not in decoded_token
        or "worker_id" not in decoded_token["sub"]
        or "role" not in decoded_token["sub"]
    ):
        raise Exception("Invalid refresh token payload!")

    worker_id = ObjectId(decoded_token["sub"]["worker_id"])
    worker_role = decoded_token["sub"]["role"]
    worker = DB.find_one(
        {
            "_id": worker_id,
            "is_active": True,
            "user_role": worker_role,
        }
    )
    if not worker:
        raise Exception("Worker not found!")
    DB.update_one(
        {"_id": worker_id},
        {"$set": {"refresh_token.token": None, "refresh_token.expires_at": None}},
    )
    response = make_response(
        jsonify({"message": f"{worker["user_role"]} logged out"}), 200
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

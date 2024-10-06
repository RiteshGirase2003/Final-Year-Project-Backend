from flask import jsonify, request
from bson.objectid import ObjectId
from multimeter_api.dto.req.create_multimeter_dto import CreateMultimeterDTO
from multimeter_api.dto.req.update_multimeter_dto import UpdateMultimeterDTO
from multimeter_api.dto.res.multimeter_res_dto import MultimeterResDTO
from datetime import datetime

""" Create Multimeter """


def createMultimeter(DB, multimeter):

    existing_multimeter = DB.find_one({"serial_no": multimeter["serial_no"]})
    if existing_multimeter:
        raise (Exception("Multimeter with this serial number already exists!"))
    multimeter = CreateMultimeterDTO(**multimeter)
    DB.insert_one(multimeter.dict())
    return jsonify({"message": "Multimeter created successfully"}), 201


""" Get Multimeter """


def getMultimeters(DB):
    query = {
        "is_active": True,
    }
    serial_no = request.args.get("serial_no")
    model = request.args.get("model")
    sort_order = request.args.get("sort_order", "asc")
    if serial_no:
        query["serial_no"] = {"$regex": serial_no.strip('"'), "$options": "i"}
    if model:
        query["model"] = model.strip('"')

    sort_criteria = [("created_at", 1 if sort_order == "asc" else -1)]

    multimeters = DB.find(query).sort(sort_criteria)
    multimeter_list = list(multimeters)
    results = []
    if multimeter_list:
        for multimeter in multimeter_list:
            multimeter_data = MultimeterResDTO(
                id=str(multimeter["_id"]),
                **{k: v for k, v in multimeter.items() if k != "_id"}
            )
            results.append(multimeter_data.dict())
    if len(results) == 0:
        raise (Exception("No multimeter found!"))
    return jsonify(results), 200


""" Update Multimeter """


def updateMultimeter(DB, updated_data, id):

    id = ObjectId(id)
    existing_multimeter = DB.find_one({"_id": id, "is_active": True})
    if not existing_multimeter:
        raise (Exception("Multimeter not found!"))
    updated_data = UpdateMultimeterDTO(**updated_data)
    updated_data.updated_at = datetime.now()
    DB.find_one_and_update({"_id": id}, {"$set": updated_data.dict()})
    return jsonify({"message": "Multimeter updated successfully"}), 200


""" Delete Multimeter """


def deleteMultimeter(DB, id):
    id = ObjectId(id)
    existing_multimeter = DB.find_one({"_id": id, "is_active": True})
    if not existing_multimeter:
        raise (Exception("Multimeter not found!"))
    DB.find_one_and_update(
        {"_id": id}, {"$set": {"is_active": False, "updated_at": datetime.now()}}
    )
    return jsonify({"message": "Multimeter deleted successfully"}), 200

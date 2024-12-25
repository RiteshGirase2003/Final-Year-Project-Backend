from flask import jsonify, request
from bson.objectid import ObjectId
from multimeter_api.dto.req.create_multimeter_dto import CreateMultimeterDTO
from multimeter_api.dto.req.update_multimeter_dto import UpdateMultimeterDTO
from multimeter_api.dto.res.multimeter_res_dto import MultimeterResDTO
from datetime import datetime
from middleware.upload_photos import upload_image

""" Handle Pagination """


def handlePagination(DB):
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    total = DB.count_documents({})
    total_pages = (total + limit - 1) // limit
    if total_pages == 0:
        return [], 0, 0, 0
    if page > total_pages:
        page = total_pages
    data = DB.find({}).skip((page - 1) * limit).limit(limit)
    res = []
    for meter in data:
        entry = MultimeterResDTO(
            id=str(meter["_id"]), **{k: v for k, v in meter.items() if k != "_id"}
        ).dict()
        res.append(entry)
    return res, total, page, limit


""" Create Multimeter """


def createMultimeter(DB, multimeter):
    cover_image = request.files.get("photo")
    if not cover_image:
        raise (Exception("Please provide cover image and screen photos!"))
    cover_image = upload_image(cover_image)
    multimeter["photo"] = cover_image
    multimeter = CreateMultimeterDTO(**multimeter)
    DB.insert_one(multimeter.dict())
    data, total, page, limit = handlePagination(DB)
    return (
        jsonify(
            {
                "data": data,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                },
            }
        ),
        201,
    )


""" Get Multimeter """


def getMultimeters(DB):
    query = {}
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    model = request.args.get("model")
    sort_order = request.args.get("sort_order", "asc")
    if model:
        query["model"] = {"$regex": model, "$options": "i"}

    sort_criteria = [("created_at", 1 if sort_order == "asc" else -1)]

    multimeters = (
        DB.find(query).sort(sort_criteria).skip((page - 1) * limit).limit(limit)
    )
    multimeter_list = list(multimeters)

    results = []
    if multimeter_list:
        for multimeter in multimeter_list:
            multimeter_data = MultimeterResDTO(
                id=str(multimeter["_id"]),
                **{k: v for k, v in multimeter.items() if k != "_id"}
            )
            results.append(multimeter_data.dict())
    total = DB.count_documents(query)
    return (
        jsonify(
            {
                "data": results,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                },
            }
        ),
        200,
    )


""" Update Multimeter """


def updateMultimeter(DB, updated_data, id):
    id = ObjectId(id)
    existing_multimeter = DB.find_one({"_id": id})
    if not existing_multimeter:
        raise (Exception("Multimeter not found!"))
    photo = request.files.get("photo")
    if photo:
        updated_data["photo"] = upload_image(photo)
    updated_data = UpdateMultimeterDTO(**updated_data)
    updated_data_dict = updated_data.dict(exclude_unset=True)
    updated_data_dict["updated_at"] = datetime.now()
    DB.find_one_and_update({"_id": id}, {"$set": updated_data_dict})
    data, total, page, limit = handlePagination(DB)
    return (
        jsonify(
            {
                "data": data,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                },
            }
        ),
        200,
    )


""" Delete Multimeter """


def deleteMultimeter(DB, id):
    id = ObjectId(id)
    existing_multimeter = DB.find_one({"_id": id})
    if not existing_multimeter:
        raise (Exception("Multimeter not found!"))
    DB.delete_one({"_id": id})
    data, total, page, limit = handlePagination(DB)
    return (
        jsonify(
            {
                "data": data,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                },
            }
        ),
        200,
    )


""" Get List of Unique Models """


def getList(DB):
    unique_models = DB.find({}).distinct("model")
    if not unique_models:
        raise Exception("No models found!")
    models_with_ids = []
    for model in DB.find({}, {"model": 1, "photo": 1}):
        models_with_ids.append(
            {"id": str(model["_id"]), "model": model["model"], "image": model["photo"]}
        )
    return jsonify(models_with_ids), 200

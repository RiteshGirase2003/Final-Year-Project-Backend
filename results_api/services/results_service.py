from flask import jsonify, request
from results_api.dto.request.results_request_dto import ResultsRequestDTO
from bson import ObjectId
from datetime import datetime
import dateutil.parser
import random

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
    for inspection in data:
        inspection["_id"] = str(inspection["_id"])
        res.append(inspection)
    return res, total, page, limit


""" Create and update inspection """


def create_inspection(DB, data):
    data = ResultsRequestDTO(**data)
    meter = DB["Multimeter"].find_one(
        {"_id": ObjectId(data.meter_id), "is_active": True}
    )
    if not meter:
        return jsonify({"message": "Meter not found"}), 404
    if data.serial_no and data.client:
        exists = DB["Result"].find_one(
            {"serial_no": data.serial_no, "client": data.client}
        )
        if exists:
            DB["Result"].update_one(
                {"_id": ObjectId(exists["_id"])},
                {
                    "$set": {
                        "meter_id": data.meter_id,
                        "worker_id": data.worker_id,
                        "status": data.status,
                        "date": datetime.now(),
                    }
                },
            )
            data, total, page, limit = handlePagination(DB["Result"])
            return (
                jsonify(
                    {
                        "data": data,
                        "meta": {"total": total, "page": page, "limit": limit},
                    }
                ),
                201,
            )
    inspection = {
        "serial_no": data.serial_no,
        "client": data.client,
        "meter_id": data.meter_id,
        "worker_id": data.worker_id,
        "status": data.status,
        "date": datetime.now(),
    }
    DB["Result"].insert_one(inspection)
    data, total, page, limit = handlePagination(DB["Result"])
    return (
        jsonify({"data": data, "meta": {"total": total, "page": page, "limit": limit}}),
        201,
    )


def get_inspections(DB, worker_id):
    query = {}
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    my = request.args.get("my")
    if my:
        query["worker_id"] = worker_id
    for key in ["serial_no", "client"]:
        if request.args.get(key):
            query[key] = {"$regex": request.args.get(key), "$options": "i"}
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    if start_date and end_date:
        start_date = dateutil.parser.parse(start_date)
        end_date = dateutil.parser.parse(end_date)
        if start_date > end_date:
            raise Exception("Invalid date range")
        query["date"] = {"$gte": start_date, "$lte": end_date}
    if request.args.get("result"):
        query["status"] = str(request.args.get("result"))

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
        inspection["model"] = inspection["meter_details"]["model"]
        formatted.append(inspection)

    total = DB["Result"].count_documents(query)

    return (
        jsonify(
            {"data": formatted, "meta": {"total": total, "page": page, "limit": limit}}
        ),
        200,
    )


def delete_inspection(DB, inspection_id):
    inspection = DB["Result"].find_one({"_id": ObjectId(inspection_id)})
    if not inspection:
        raise Exception("Inspection Not Found!")

    DB["Result"].delete_one({"_id": ObjectId(inspection_id)})
    data, total, page, limit = handlePagination(DB["Result"])
    return (
        jsonify({"data": data, "meta": {"total": total, "page": page, "limit": limit}}),
        200,
    )


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


def checkMeter(DB):
    """model = tf.keras.models.load_model("path_to_saved_model_weights.h5")

    image_file = request.files.get("image")
    if not image_file:
        raise Exception("Image is required")

    image = Image.open(io.BytesIO(image_file.read()))

    preprocess = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    image_tensor = preprocess(image).unsqueeze(0)

    # Convert the image tensor to a numpy array
    image_np = image_tensor.numpy()

    # Make prediction
    predictions = model.predict(image_np)
    predicted_class = tf.argmax(predictions, axis=1).numpy()[0]

    # Send the result back"""
    image = request.files.get("image")
    master = request.files.get("master")
    if not image or not master:
        raise Exception("Image is required")
    predicted_class = random.randint(0, 1)
    if predicted_class == 0:
        return jsonify("Pass"), 200
    return jsonify("Fail"), 200

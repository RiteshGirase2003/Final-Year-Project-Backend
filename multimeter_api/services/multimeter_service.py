from flask import jsonify, request
from bson.objectid import ObjectId

""" Create Multimeter """


def createMultimeter(DB, multimeter):
    try:
        existing_multimeter = DB.find_one({"serial_no": multimeter["serial_no"]})
        if existing_multimeter:
            return (
                jsonify({"error": "Multimeter already exists with this serial_no."}),
                400,
            )

        DB.insert_one(
            {
                "serial_no": multimeter["serial_no"],
                "model": multimeter["model"],
                "description": multimeter["description"],
                "photo": multimeter["photo"],
                "screen_photos": multimeter["screen_photos"],
            }
        )

        return jsonify({"message": "Multimeter created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


""" Get Multimeter """


def getMultimeters(DB):
    query = {}

    serial_no = request.args.get("serial_no")
    model = request.args.get("model")

    if serial_no:
        query["serial_no"] = {"$regex": serial_no.strip('"'), "$options": "i"}
    if model:
        query["model"] = {"$regex": model.strip('"'), "$options": "i"}

    multimeters = DB.find(query)
    multimeter_list = list(multimeters)

    if multimeter_list:
        results = []
        for multimeter in multimeter_list:
            results.append(
                {
                    "id": str(multimeter["_id"]),
                    "serial_no": multimeter["serial_no"],
                    "model": multimeter["model"],
                    "description": multimeter["description"],
                    "photo": multimeter["photo"],
                    "screen_photos": multimeter["screen_photos"],
                }
            )
        return jsonify(results)
    else:
        return jsonify({"error": "Multimeter not found"}), 404


""" Update Multimeter """


def updateMultimeter(DB, updated_data, id):
    try:
        id = ObjectId(id)
        existing_multimeter = DB.find_one({"_id": id})
        if not existing_multimeter:
            return jsonify({"error": "Multimeter not found"}), 404

        DB.find_one_and_update({"_id": id}, {"$set": updated_data})

        return jsonify({"message": "Multimeter updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


""" Delete Multimeter """


def deleteMultimeter(DB, id):
    try:
        id = ObjectId(id)
        DB.find_one_and_delete({"_id": id})
        return jsonify({"message": "Multimeter deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

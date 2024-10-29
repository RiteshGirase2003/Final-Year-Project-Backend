from flask import jsonify


def sendMessage():
    return jsonify({"message": "Hello World!"})

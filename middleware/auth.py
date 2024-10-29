from flask import Flask, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            print(e)
            return jsonify({"msg": "Missing or invalid token"}), 401
        return fn(*args, **kwargs)
    return wrapper
from flask import Flask, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from routine_api.services.routine_service import updateRoutine
from db_connect import DB
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            worker_id = get_jwt_identity()["worker_id"]
            future = executor.submit(updateRoutine, DB, worker_id)
            future.add_done_callback(lambda f: print("Routine Updated"))
        except Exception as e:
            print(e)
            return jsonify({"msg": "Missing or invalid token"}), 401
        return fn(*args, **kwargs)

    return wrapper


def check_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                if role != get_jwt_identity()["role"]:
                    return jsonify({"msg": "Unauthorized access"}), 403
            except Exception as e:
                print(e)
                return jsonify({"msg": "Missing or invalid token"}), 401
            return fn(*args, **kwargs)

        return wrapper

    return decorator

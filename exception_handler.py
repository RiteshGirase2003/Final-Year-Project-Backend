from flask import jsonify
from pydantic import ValidationError


def handle_validation_error(e: ValidationError):
    errors = e.errors()
    readable_errors = []
    for error in errors:
        field = error["loc"][0]
        message = error["msg"]
        readable_errors.append(f"{field}: {message}")
    error_string = "; ".join(readable_errors)

    response = jsonify({"error": error_string})
    response.status_code = 400
    return response


def handle_generic_error(e):
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response

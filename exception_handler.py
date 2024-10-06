from flask import jsonify
from pydantic import ValidationError

def handle_validation_error(e):
    response = jsonify({"Validation Error": e.errors()})
    response.status_code = 400
    return response

def handle_generic_error(e):
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response
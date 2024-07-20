from flask import jsonify

def handle_error(e):
    error_response = {
        "error": {
            "message": str(e),
            "type": "challenge error"
        }
    }
    return jsonify(error_response), 501
"""
VAPI Transfer Call Integration Service
------------------------------------

This Flask application provides a webhook endpoint (/webhook) for a Voice API integration.

Author: Development Team
Date: February 2025
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configure logging system
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Load secrets from environment variables
API_KEY = os.getenv('FLASK_API_KEY')
VAPI_SECRET_TOKEN = os.getenv('VAPI_WEBHOOK_SECRET')

if not API_KEY or not VAPI_SECRET_TOKEN:
    logging.warning("No API keys set. Using development defaults - DO NOT USE IN LIVE ENVIRONMENT!")
    API_KEY = 'development-api-key-do-not-use-in-live'
    VAPI_SECRET_TOKEN = 'development-webhook-secret-do-not-use-in-live'

# Decorator to enforce API key authentication
def require_api_key(f):
    """Require API key authentication for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or provided_key != API_KEY:
            logging.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Load company directory data from JSON file
try:
    with open('company_directory.json') as f:
        directory_data = json.load(f)
        directory = directory_data.get('employees', [])
        logging.info(f"Loaded {len(directory)} employees from directory")
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"Company directory error: {str(e)}")
    directory = []

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming VAPI webhooks and route calls to appropriate representatives.
    """
    # Verify the secret token
    secret = request.headers.get('x-vapi-secret')
    if not secret or secret != VAPI_SECRET_TOKEN:
        logging.warning(f"Unauthorized VAPI webhook request from {request.remote_addr}")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)
    if not data:
        logging.error("No JSON body received or failed to parse JSON.")
        return jsonify({"error": "Invalid request, JSON required"}), 400

    logging.info(f"Incoming call webhook data: {json.dumps(data, indent=2)}")

    tool_call_id = data.get('toolCallId')
    requested_party = data.get('requestedParty')
    if not tool_call_id:
        logging.error("toolCallId missing in request data.")
        return jsonify({"error": "Missing toolCallId"}), 400
    if not requested_party:
        logging.error("requestedParty not provided in request data.")
        return jsonify({
            "results": [{
                "toolCallId": tool_call_id,
                "result": "ERROR: requestedParty not provided"
            }]
        }), 400

    # Attempt to find the requested employee
    target_employee = next(
        (emp for emp in directory if emp.get("name", "").lower() == requested_party.lower()),
        None
    )

    if not target_employee or not target_employee.get("phone"):
        logging.warning(f"No available employee found for: {requested_party}")
        return jsonify({
            "results": [{
                "toolCallId": tool_call_id,
                "result": f"No such contact: {requested_party}"
            }]
        }), 404

    target_number = target_employee["phone"]
    target_name = target_employee["name"]
    logging.info(f"Routing call to: {target_name} ({target_number})")

    result_payload = {
        "results": [{
            "toolCallId": tool_call_id,
            "result": target_number
        }]
    }
    return jsonify(result_payload)

@app.route('/transfer', methods=['POST'])
@require_api_key
def transfer_call():
    """
    Handle call transfer requests from external sources.
    """
    data = request.get_json()
    if not data or "target_number" not in data:
        return jsonify({"error": "Missing required field: target_number"}), 400

    target_number = data["target_number"]
    logging.info(f"Processing transfer request to: {target_number}")

    return jsonify({
        "message": "Transfer request received",
        "target_number": target_number
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint."""
    return "VAPI Call Transfer Service is running."

# Entry point for development
if __name__ == "__main__":
    logging.info("Starting VAPI Service")
    if API_KEY.startswith('development-'):
        logging.warning("Using development API key. Set FLASK_API_KEY environment variable for live deployment.")
    port = int(os.environ.get("PORT", 8080))
    print(f"\n🚀 VAPI Transfer Call Service is running!")
    print(f"🌐 Server: http://0.0.0.0:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)

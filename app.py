"""
VAPI Transfer Call Integration Service
------------------------------------

This Flask application provides a webhook endpoint for handling incoming voice calls
through a Voice API integration. It routes calls to company representatives based
on the company directory configuration.

Key Components:
    - Webhook endpoint (/webhook) for handling incoming call events
    - Company directory integration for employee contact information
    - Logging system for tracking all webhook interactions
    - Voice API response formatting for call routing
    - API key authentication for security

Author: Development Team
Date: February 2025
"""

from flask import Flask, request, jsonify
import json
import logging
import os
from functools import wraps

# Initialize Flask application
app = Flask(__name__)

# Configure logging system
# Logs will be written to app.log with timestamp, level, and message
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Get API key from environment variable or use a default for development
API_KEY = os.getenv('FLASK_API_KEY', 'your-development-api-key-change-this')

def require_api_key(f):
    """Decorator to require API key for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or provided_key != API_KEY:
            logging.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Load company directory data from JSON file
# The directory contains employee contact information for call routing
try:
    with open('company_directory.json') as f:
        directory_data = json.load(f)
        # Extract employees list from the directory data
        directory = directory_data.get('employees', [])
        logging.info(f"Loaded {len(directory)} employees from directory")
except FileNotFoundError:
    logging.error("Company directory file not found")
    directory = []
except json.JSONDecodeError:
    logging.error("Invalid JSON in company directory file")
    directory = []

@app.route('/webhook', methods=['POST'])
@require_api_key
def webhook():
    """
    Handle incoming VAPI webhooks and route calls to appropriate representatives.

    This endpoint processes incoming webhook data from the Voice API and determines
    how to route the call based on the company directory configuration.

    Required Headers:
        X-API-Key: Your API key for authentication

    Returns:
        JSON response containing Voice API actions:
        - For successful routing: Talk action followed by Connect action
        - For failures: Talk action with error message
        - For unauthorized access: 401 Unauthorized

    Example Response:
        [
            {
                "action": "talk",
                "text": "Connecting you to our representative."
            },
            {
                "action": "connect",
                "endpoint": [
                    {
                        "type": "phone",
                        "number": "+15551234567"
                    }
                ]
            }
        ]
    """
    # Extract and log the incoming webhook data
    data = request.get_json()
    logging.info(f"Incoming call webhook data: {data}")

    # Find target phone number from directory
    # Currently routes to the first employee as an example
    # TODO: Implement more sophisticated routing logic based on:
    #   - Time of day
    #   - Department
    #   - Employee availability
    #   - Call purpose or customer input
    target_number = None
    target_name = None
    if len(directory) > 0:
        target_employee = directory[0]
        target_number = target_employee.get("phone")
        target_name = target_employee.get("name")
        logging.info(f"Routing call to: {target_name} ({target_number})")
    else:
        logging.warning("No available employees found in directory")

    # Build response actions for the Voice API
    if target_number:
        actions = [
            {
                "action": "talk",
                "text": f"Connecting you to our representative, {target_name}."
            },
            {
                "action": "connect",
                "endpoint": [
                    {
                        "type": "phone",
                        "number": target_number
                    }
                ]
            }
        ]
    else:
        actions = [
            {
                "action": "talk",
                "text": "No employees are available to take your call at this time."
            }
        ]

    # Log and return the response
    logging.info(f"Responding with actions: {actions}")
    return jsonify(actions)

if __name__ == "__main__":
    # Start development server
    # Note: For production, use a proper WSGI server like Gunicorn
    logging.info("Starting VAPI Transfer Call Integration Service")
    if API_KEY == 'your-development-api-key-change-this':
        logging.warning("Using default API key. Set FLASK_API_KEY environment variable in production.")
    app.run(host="0.0.0.0", port=5000)
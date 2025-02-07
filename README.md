# VAPI Transfer Call Integration

A Flask-based Voice API integration service for handling call transfers. This service handles incoming call webhooks and routes them to appropriate company representatives based on the company directory.

## Features

- Webhook endpoint for handling incoming voice calls
- Integration with company employee directory
- Automatic call routing to available representatives
- Comprehensive logging system
- Simple JSON-based configuration

## Project Structure

```
vapi-transfer-call-integration/
├── app.py                    # Main Flask application with VAPI webhook handling
├── company_directory.json    # Employee directory with contact information
├── requirements.txt         # Python dependencies
└── .gitignore              # Git ignore configuration
```

## Prerequisites

- Python 3.6 or higher
- Flask
- Gunicorn (for production deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/samurai-no-shogun/vapi-transfer-call-integration.git
cd vapi-transfer-call-integration
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Company Directory

The `company_directory.json` file contains the employee directory information. Each entry includes:
- `id`: Unique identifier for the employee
- `name`: Employee's full name
- `department`: Department they work in
- `phone`: Contact phone number
- `email`: Email address

Example:
```json
{
  "employees": [
    {
      "id": 1,
      "name": "Alice Smith",
      "department": "Sales",
      "phone": "+15551234567",
      "email": "alice.smith@example.com"
    }
  ]
}
```

## Usage

1. Start the development server:
```bash
python app.py
```

2. The server will start on `http://0.0.0.0:5000`

3. The webhook endpoint will be available at:
```
POST /webhook
```

### Webhook Response Format

The webhook endpoint returns a JSON response with Voice API actions:
```json
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
```

## Logging

The application logs all incoming webhook data and responses to `app.log`. The logging format includes:
- Timestamp
- Log level
- Message content

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Production Deployment

For production deployment, it's recommended to:

1. Use Gunicorn as the WSGI server:
```bash
gunicorn app:app
```

2. Set up proper security measures:
   - Use HTTPS
   - Implement authentication for the webhook endpoint
   - Configure proper firewall rules

## License

[Add appropriate license information]
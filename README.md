# VAPI Transfer Call Integration

A Flask-based Voice API integration service for handling call transfers. This service handles incoming call webhooks and routes them to appropriate company representatives based on the company directory.

## Features

- Webhook endpoint for handling incoming voice calls
- API key authentication for security
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
├── Procfile                # Railway deployment configuration
├── .env.example           # Example environment variables
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

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env`:
     ```
     FLASK_API_KEY=your-secure-api-key-here
     PORT=8080
     ```

## Configuration

### API Key Authentication

The webhook endpoint is protected by API key authentication. You must include the API key in the request headers:

```http
X-API-Key: your-api-key-here
```

For development, if no API key is set in the environment, a default key is used:
```
your-development-api-key-change-this
```

Make sure to set a secure API key in production using the `FLASK_API_KEY` environment variable.

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

### Local Development

1. Start the development server:
```bash
python app.py
```

2. The server will start on `http://0.0.0.0:8080`

3. The webhook endpoint will be available at:
```
POST /webhook
```

Remember to include the API key in your requests:
```bash
curl -X POST http://localhost:8080/webhook \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"your": "webhook data"}'
```

### Railway Deployment

This project is configured for deployment on Railway. The included `Procfile` specifies the command to run the application using Gunicorn.

To deploy on Railway:

1. Create a new project on [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Set up environment variables in Railway:
   - Add `FLASK_API_KEY` with a secure value
4. Railway will automatically:
   - Detect the Python environment
   - Install dependencies from requirements.txt
   - Use the Procfile to start the application
5. Your application will be available at the URL provided by Railway

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
- Authentication attempts and failures

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Production Deployment

For production deployment, we use:

1. Gunicorn as the WSGI server (configured in Procfile):
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

2. Security measures:
   - API key authentication (required)
   - HTTPS (handled by Railway)
   - Proper firewall rules

## License

[Add appropriate license information]
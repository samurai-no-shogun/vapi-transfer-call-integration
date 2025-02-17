#!/bin/bash
# Super Prompt: Set up Dockerization for your VAPI Transfer Call Integration project

echo "Creating Dockerfile..."

cat > Dockerfile << 'EOF'
# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code, including company_directory.json
COPY . .

# Expose the port that Railway will map externally (e.g., 8080)
EXPOSE 8080

# Run the app using Gunicorn, binding to the port from environment or defaulting to 8080
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
EOF

echo "Dockerfile created successfully."

# Optional: Create a minimal railway.toml if you want config-as-code (uncomment the following block if desired)
# echo "Creating railway.toml..."
# cat > railway.toml << 'EOF'
# [build]
#   command = "pip install -r requirements.txt"
#
# [deploy]
#   command = "gunicorn app:app --bind 0.0.0.0:$PORT"
# EOF
# echo "railway.toml created successfully."

echo "Ensure that your sensitive files (like company_directory.json) are not excluded in production if needed."
echo "If they are in .gitignore and you want to include them in your Docker image, update your .gitignore accordingly."

echo "Next steps:"
echo "1. Verify your Dockerfile and any changes."
echo "2. Commit these changes to your Git repository:"
echo "   git add Dockerfile [railway.toml if created] && git commit -m 'Add Dockerfile for Dockerization' && git push origin main"
echo "3. In Railway, set your environment variables (e.g., FLASK_API_KEY, VAPI_WEBHOOK_SECRET) as usual."
echo "4. Railway will build your Docker image automatically if you link your GitHub repo."
echo "5. Test your deployment at: https://vapi-transfer-call-integration-production.up.railway.app"

echo "Dockerization setup complete!"
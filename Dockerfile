# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and company directory
COPY app.py .
COPY company_directory.json .

# Expose the port that Railway will map externally (e.g., 8080)
EXPOSE 8080

# Run the app using Gunicorn, binding to the port from environment
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
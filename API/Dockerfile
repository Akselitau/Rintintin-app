# Dockerfile for backend
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV CHALICE_APP_NAME your_chalice_app_name
ENV CHALICE_STAGE dev

# Expose the port Chalice will run on
EXPOSE 8000

# Run Chalice local server
CMD ["chalice", "local", "--host", "0.0.0.0", "--port", "8000"]

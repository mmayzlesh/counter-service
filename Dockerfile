# Use the Python 3.11-slim base image from Docker Hub
FROM python:3.11-slim

# Set the working directory within the container to /app
WORKDIR /app

# Copy the local requirements.txt file to the /app directory in the container
COPY requirements.txt requirements.txt

# Install the Python dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the contents of the local application code into the /app directory in the container
COPY . .

# Run Gunicorn to serve the "counter_service:app" application on 0.0.0.0:8080
# to make it accessible outside the container, e.g. for Nginx.
CMD ["gunicorn", "-b", "0.0.0.0:8080", "counter_service:app"]

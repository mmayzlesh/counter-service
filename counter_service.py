# Import necessary modules from Flask, Redis, and the OS
from flask import Flask, request
import redis
import os

# Create a Flask web application instance
app = Flask(__name__)

# Connect to the Redis server using the 'redis' hostname and default port (6379)
# Set decode_responses=True to ensure that Redis responses are decoded to strings
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Define a route for the root URL ('/') that handles both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def counter():
    if request.method == 'POST':
        # If it's a POST request, increment the 'count' key in Redis
        r.incr('count')
    
    # Retrieve the current value of the 'count' key from Redis
    count = r.get('count')

    # If 'count' is None (not set in Redis), initialize it to 0
    if count is None:
        count = 0
        r.set('count', count)

    # Return a JSON response with the current count as an integer
    return {'count': int(count)}

# Run the Flask app if this script is the main entry point, e.g. using app.run()
# but if app is being served by other means, e.g. by Gunicorn etc., let them set the binding
if __name__ == "__main__":
    # Set the host to '0.0.0.0' to make the app accessible outside the container (e.g. by Nginx)
    # Use the port specified by the 'PORT' environment variable, defaulting to 8080
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

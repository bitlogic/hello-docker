"""
Flask application with Redis counter.

This application demonstrates a simple Flask web server that maintains
a visitor counter using Redis as a backend store.
"""
import logging
import os
import socket

from flask import Flask, render_template
from redis import Redis, RedisError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_TIMEOUT = int(os.getenv("REDIS_TIMEOUT", "2"))
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "80"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# Connect to Redis with proper error handling
try:
    redis = Redis(
        host=REDIS_HOST,
        db=REDIS_DB,
        socket_connect_timeout=REDIS_TIMEOUT,
        socket_timeout=REDIS_TIMEOUT
    )
    # Test connection
    redis.ping()
    logger.info("Successfully connected to Redis at %s", REDIS_HOST)
except (RedisError, ConnectionError) as e:
    logger.warning("Failed to connect to Redis: %s. Counter will be disabled.", str(e))
    redis = None

app = Flask(__name__)


@app.route("/")
def hello():
    """
    Main route handler that displays a greeting page with visit counter.

    Returns:
        str: Rendered HTML template with greeting message, hostname, and visit count
    """
    visits = None
    
    if redis is not None:
        try:
            visits = redis.incr("counter")
            logger.debug("Visit counter incremented to: %s", visits)
        except RedisError as e:
            logger.error("Redis error while incrementing counter: %s", str(e))
            visits = "cannot connect to Redis, counter disabled"
    else:
        visits = "cannot connect to Redis, counter disabled"

    name = os.getenv("NAME", "world")
    hostname = socket.gethostname()
    
    return render_template(
        'hello.html',
        name=name,
        hostname=hostname,
        visits=visits
    )


if __name__ == "__main__":
    logger.info(
        "Starting Flask application on %s:%d (debug=%s)",
        FLASK_HOST,
        FLASK_PORT,
        FLASK_DEBUG
    )
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
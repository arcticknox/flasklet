import redis
import time
import os

from flask import Flask, jsonify
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
APP_PORT = os.environ.get("APP_PORT")
# Flask app
app = Flask(__name__)
# Connect redis
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/")
def healthcheck():
    count = get_hit_count()
    return jsonify(
        timestamp=datetime.utcnow(),
        hits=count
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT, debug=True)

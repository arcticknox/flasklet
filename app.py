from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def healthcheck():
    return jsonify(
        timestamp= datetime.utcnow()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
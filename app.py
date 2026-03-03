import os

import redis
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

r = None


def get_redis():
    global r
    if r is None:
        r = redis.Redis.from_url(
            os.environ.get("REDIS_URL", "redis://localhost:6379"), decode_responses=True
        )
    return r


@app.route("/")
def root():
    return jsonify(
        {
            "routes": [
                {"method": "GET", "path": "/kv/{key}", "description": "Get a value by key"},
                {"method": "PUT", "path": "/kv/{key}", "description": "Set a value by key"},
                {
                    "method": "DELETE",
                    "path": "/kv/{key}",
                    "description": "Delete a value by key",
                },
            ]
        }
    )


@app.route("/kv/<key>", methods=["PUT"])
def put_key(key):
    body = request.get_json()
    if not body or "value" not in body:
        abort(400, description="Missing 'value' in request body")
    get_redis().set(key, body["value"])
    return jsonify({"key": key, "value": body["value"]})


@app.route("/kv/<key>", methods=["GET"])
def get_key(key):
    value = get_redis().get(key)
    if value is None:
        abort(404, description="Key not found")
    return jsonify({"key": key, "value": value})


@app.route("/kv/<key>", methods=["DELETE"])
def delete_key(key):
    if not get_redis().delete(key):
        abort(404, description="Key not found")
    return jsonify({"deleted": True})

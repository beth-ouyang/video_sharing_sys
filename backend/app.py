import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

QUEUE = []
PORT = 8000


# Helper function to find item by ID
def find_by_id(video_id):
    return next((item for item in QUEUE if item["id"] == video_id), None)


@app.route("/submit", methods=["POST"])
def submit_video():
    data = request.get_json()
    video_id = str(uuid.uuid4())
    item = {"id": video_id, "url": data["url"], "domain": data["domain"]}
    QUEUE.append(item)
    return jsonify({"message": "Video added", "id": video_id})


@app.route("/queue", methods=["GET"])
def get_queue():
    return jsonify(QUEUE)


@app.route("/queue/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    global QUEUE
    QUEUE = [item for item in QUEUE if item["id"] != video_id]
    return jsonify({"message": "Video removed"})


@app.route("/next", methods=["GET"])
def get_next_video():
    if QUEUE:
        return jsonify(QUEUE[0])
    return jsonify(None)


@app.route("/consume_next", methods=["POST"])
def consume_next_video():
    if QUEUE:
        item = QUEUE.pop(0)
        return jsonify({"url": item["url"], "domain": item["domain"]})
    return jsonify({"url": None})


if __name__ == "__main__":
    app.run(debug=True, port=PORT)

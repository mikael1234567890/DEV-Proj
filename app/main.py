from flask import Flask, jsonify, request
import logging
import uuid
from datetime import datetime, timezone


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

TASKS = {}


@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/metrics")
def metrics():
    return jsonify(
        task_count=len(TASKS),
        uptime="running"
    ), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not data or "title" not in data:
        return jsonify(error="title required"), 400
    
    
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": data["title"],
        "created": datetime.now(timezone.utc).isoformat(),
        "status": "pending"

    }

    TASKS[task_id] = task
    app.logger.info(f"task created: {task_id}")

    return jsonify(task), 201

@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(list(TASKS.values())), 200

@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = TASKS.get(task_id)
    if not task:
        return jsonify(error="not found"), 404
    return jsonify(task), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


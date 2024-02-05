import json
import os

from flask import Flask, request, jsonify
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)

model = YOLO('yolov8m-oiv7.pt')  # pretrained YOLOv8n model


def get_predictions(filepath):
    results = model(filepath)
    return json.loads(results[0].tojson())


def check_for_item(predictions, item):
    for classification in predictions:
        name = classification["name"]
        confidence = float(classification["confidence"])

        if name == item and confidence > 0.8:
            return True

    return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


@app.route('/brew', methods=['POST', 'BREW'])
def teapot_or_not():
    files = list(request.files.values())
    if len(files) == 0:
        return jsonify("{'HasError': true, 'Message': 'No file provided'}"), 400

    file = files[0]

    if not allowed_file(file.filename):
        return jsonify("{'HasError': true, 'Message': 'File type must be png, jpg or jpeg'}"), 400

    # Save file to system
    filename = secure_filename(file.filename)
    file.save(filename)

    # Analyse file for teapot
    predictions = get_predictions(filename)
    teapot = check_for_item(predictions, "Teapot")
    coffee_machine = check_for_item(predictions, "Saucer")

    os.remove(filename)

    # Provide a response
    if teapot:
        return jsonify("{'HasError': false, 'Message': 'I'm a teapot'}"), 418
    if coffee_machine:
        return jsonify("{'HasError': false, 'Message': 'Here's your coffee! ☕'}"), 200
    else:
        return jsonify("{'HasError': false, 'Message': 'I'm not a teapot'}"), 200


app.run()

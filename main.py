import json
import os

from flask import Flask, request, Response
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
        return Response("{'HasError': true, 'Message': 'No file provided'}", status=400, mimetype='application/json')

    file = files[0]

    if not allowed_file(file.filename):
        return Response("{'HasError': true, 'Message': 'File type must be png, jpg or jpeg'}", status=400, mimetype='application/json')

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
        return Response("{'HasError': false, 'Message': 'I'm a teapot'}", status=418, mimetype='application/json')
    if coffee_machine:
        return Response("{'HasError': false, 'Message': 'Here's your coffee! ☕'}", status=200, mimetype='application/json')
    else:
        return Response("{'HasError': false, 'Message': 'I'm not a teapot'}", status=200, mimetype='application/json')


app.run()

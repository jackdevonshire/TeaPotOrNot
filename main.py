from ultralytics import YOLO
import json
import os
from flask import Flask, flash, request, redirect, url_for, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/uploads"

model = YOLO('yolov8m-oiv7.pt')  # pretrained YOLOv8n model


def get_predictions(filepath):
    results = model(filepath)
    return json.loads(results[0].tojson())


def is_tea_pot(predictions):
    for classification in predictions:
        name = classification["name"]
        confidence = float(classification["confidence"])

        if name == "Teapot" and confidence > 0.8:
            return True
        else:
            return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


@app.route('/brew', methods=['POST'])
def teapot_or_not():
    files = list(request.files.values())
    if len(files) == 0:
        return Response("{'HasError': true, 'Message': 'No file provided'}", status=400, mimetype='application/json')

    file = files[0]

    if not allowed_file(file.filename):
        return Response("{'HasError': true, 'Message': 'File type must be png, jpg or jpeg'}", status=400, mimetype='application/json')




# predictions = get_predictions("https://d27pcll2dx97vv.cloudfront.net/info/wp-content/uploads/2022/04/Shuiping.jpg")
# print(is_tea_pot(predictions))

app.run()

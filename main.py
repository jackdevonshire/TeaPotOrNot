from ultralytics import YOLO
import json

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


predictions = get_predictions("https://d27pcll2dx97vv.cloudfront.net/info/wp-content/uploads/2022/04/Shuiping.jpg")
print(is_tea_pot(predictions))
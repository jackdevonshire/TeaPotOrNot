from ultralytics import YOLO
import json

# Load a model
model = YOLO('yolov8m-oiv7.pt')  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model('https://d27pcll2dx97vv.cloudfront.net/info/wp-content/uploads/2022/04/Shuiping.jpg')  # return a list of Results objects

result = json.loads(results[0].tojson())

for classification in result:
    name = classification["name"]
    confidence = float(classification["confidence"])

    print(name, confidence)

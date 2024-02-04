from ultralytics import YOLO

# Load a model
model = YOLO('yolov8m-oiv7.pt')  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model(['https://d27pcll2dx97vv.cloudfront.net/info/wp-content/uploads/2022/04/Shuiping.jpg'])  # return a list of Results objects


# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
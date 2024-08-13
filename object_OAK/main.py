from ultralytics import YOLO


# Load the exported ONNX model
onnx_model = YOLO("yolov8n.onnx")

# Run inference
results = onnx_model("https://ultralytics.com/images/bus.jpg")
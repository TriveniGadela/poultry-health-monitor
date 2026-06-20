from ultralytics import YOLO

# Load YOLOv8 nano model
model = YOLO("yolov8n.pt")

# Train the model
results = model.train(
    data="data/data.yaml",
    epochs=20,
    imgsz=512,
    batch=8,
    name="poultry_model",
    patience=5
)

print("Training complete!")
print(f"Best model saved at: runs/detect/poultry_model/weights/best.pt")
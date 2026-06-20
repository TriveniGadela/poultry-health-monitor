from ultralytics import YOLO

# Load fresh YOLOv8 nano model
model = YOLO("yolov8n.pt")

# Train with improved settings
results = model.train(
    data="data/data.yaml",
    epochs=30,
    imgsz=640,
    batch=8,
    name="poultry_model_v2",
    patience=10,
    
    # Data augmentation settings
    hsv_h=0.015,      # slight hue variation
    hsv_s=0.7,        # saturation variation
    hsv_v=0.4,        # brightness variation
    fliplr=0.5,       # 50% chance horizontal flip
    mosaic=1.0,       # combines 4 images into 1
    degrees=10,       # slight rotation
)

print("Training v2 complete!")
print(f"Best model saved at: runs/detect/poultry_model_v2/weights/best.pt")
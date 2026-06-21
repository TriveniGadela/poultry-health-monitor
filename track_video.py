from ultralytics import YOLO

model = YOLO("runs/detect/poultry_model_v2/weights/best.pt")

print("Running tracking on video...")

results = model.track(
    source="data/test_video.mp4",
    conf=0.35,
    persist=True,
    tracker="bytetrack.yaml",
    save=True
)

print("Tracking complete!")
print("Check runs/detect folder for output with tracking IDs")
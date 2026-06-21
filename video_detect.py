from ultralytics import YOLO

model = YOLO("runs/detect/poultry_model_v2/weights/best.pt")

print("Processing video... this may take a few minutes")

results = model(
    "data/test_video.mp4",
    conf=0.35,
    save=True
)

print("Video processing complete!")
print("Check the runs/detect folder for output video")
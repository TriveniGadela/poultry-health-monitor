from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np

# Load your best trained model
MODEL_PATH = "runs/detect/poultry_model_v2/weights/best.pt"
model = YOLO(MODEL_PATH)

# Class names and colors
CLASS_NAMES = {0: "disease", 1: "healthy"}
CLASS_COLORS = {
    "disease": (0, 0, 255),    # Red for disease
    "healthy": (0, 255, 0)     # Green for healthy
}

def detect_birds(image_path, confidence=0.25):
    """
    Run detection on a poultry image.
    Returns: annotated image + detection summary
    """
    # Run detection
    results = model(image_path, conf=confidence, iou=0.5)
    
    # Read original image
    image = cv2.imread(image_path)
    
    # Count results
    healthy_count = 0
    disease_count = 0
    detections = []

    # Draw bounding boxes
    for box in results[0].boxes:
        class_id = int(box.cls)
        confidence_score = float(box.conf)
        class_name = CLASS_NAMES[class_id]
        color = CLASS_COLORS[class_name]

        # Get box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Draw rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Draw label
        label = f"{class_name} {confidence_score:.0%}"
        cv2.putText(image, label, (x1, y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Count
        if class_name == "healthy":
            healthy_count += 1
        else:
            disease_count += 1

        detections.append({
            "class": class_name,
            "confidence": confidence_score
        })

    # Save annotated image
    output_path = "data/detected_result.jpg"
    cv2.imwrite(output_path, image)

    return {
        "output_image": output_path,
        "healthy": healthy_count,
        "disease": disease_count,
        "total": healthy_count + disease_count,
        "detections": detections
    }


# Test it
if __name__ == "__main__":
    test_image = "data/test/images/006_jpg.rf.36a417f455907cfe76c1789f239139f7.jpg"
    result = detect_birds(test_image)
    
    print(f"Total birds detected: {result['total']}")
    print(f"Healthy: {result['healthy']}")
    print(f"Disease: {result['disease']}")
    print(f"Result saved at: {result['output_image']}")
    
    for d in result['detections']:
        print(f"  → {d['class']} ({d['confidence']:.0%})")
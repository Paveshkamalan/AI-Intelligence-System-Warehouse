from ultralytics import YOLO
import cv2
import os


# ==============================
# PATHS
# ==============================

VIDEO_PATH = "data/raw/warehouse_demo.mp4"
OUTPUT_DIR = "data/processed"
OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "warehouse_detection_improved.mp4"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================
# LOAD MODEL
# ==============================

print("Loading YOLO model...")

model = YOLO("yolo11n.pt")

print("YOLO model loaded successfully")


# ==============================
# OPEN VIDEO
# ==============================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"Error: Could not open video: {VIDEO_PATH}")
    exit()


# ==============================
# VIDEO INFORMATION
# ==============================

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print()
print("================================")
print("VIDEO INFORMATION")
print("================================")
print(f"FPS: {fps}")
print(f"Resolution: {width}x{height}")
print(f"Frames: {total_frames}")
print("================================")


# ==============================
# OUTPUT VIDEO
# ==============================

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    OUTPUT_PATH,
    fourcc,
    fps,
    (width, height)
)


# ==============================
# DETECTION SETTINGS
# ==============================

CONFIDENCE = 0.20

# COCO class ID for person = 0
PERSON_CLASS = 0

frame_count = 0
total_person_detections = 0


print()
print("Starting improved person detection...")


# ==============================
# PROCESS VIDEO
# ==============================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    results = model(
        frame,
        imgsz=1280,
        conf=CONFIDENCE,
        classes=[PERSON_CLASS],
        verbose=False
    )

    result = results[0]

    # Count detections
    if result.boxes is not None:
        person_count = len(result.boxes)
        total_person_detections += person_count
    else:
        person_count = 0

    # Draw bounding boxes
    annotated_frame = result.plot()

    # Add person count
    cv2.putText(
        annotated_frame,
        f"People: {person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    out.write(annotated_frame)

    if frame_count % 30 == 0:
        print(
            f"Processed {frame_count}/{total_frames} frames"
        )


# ==============================
# CLEANUP
# ==============================

cap.release()
out.release()


print()
print("================================")
print("IMPROVED DETECTION COMPLETE")
print("================================")
print(f"Processed frames: {frame_count}")
print(f"Total person detections: {total_person_detections}")
print(f"Output: {OUTPUT_PATH}")
print("================================")
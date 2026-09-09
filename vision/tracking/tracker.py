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
    "warehouse_tracking.mp4"
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
# TRACKING SETTINGS
# ==============================

CONFIDENCE = 0.20
PERSON_CLASS = 0

frame_count = 0
unique_ids = set()


print()
print("Starting person tracking...")


# ==============================
# PROCESS VIDEO
# ==============================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # YOLO tracking
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        imgsz=1280,
        conf=CONFIDENCE,
        classes=[PERSON_CLASS],
        verbose=False
    )

    result = results[0]

    current_ids = []

    # Check whether tracking IDs exist
    if result.boxes is not None and result.boxes.id is not None:

        ids = result.boxes.id.int().cpu().tolist()

        current_ids = ids

        # Store every ID encountered
        for track_id in ids:
            unique_ids.add(track_id)

    # Draw tracking information
    annotated_frame = result.plot()

    # Current number of people
    person_count = len(current_ids)

    # Display information
    cv2.putText(
        annotated_frame,
        f"People: {person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Tracked IDs: {len(unique_ids)}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Write frame
    out.write(annotated_frame)

    # Progress
    if frame_count % 30 == 0:
        print(
            f"Processed {frame_count}/{total_frames} frames | "
            f"Unique IDs: {len(unique_ids)}"
        )


# ==============================
# CLEANUP
# ==============================

cap.release()
out.release()


print()
print("================================")
print("TRACKING COMPLETE")
print("================================")
print(f"Processed frames: {frame_count}")
print(f"Unique people tracked: {len(unique_ids)}")
print(f"Output: {OUTPUT_PATH}")
print("================================")
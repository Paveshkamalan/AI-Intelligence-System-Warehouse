import os
import cv2
from ultralytics import YOLO

from configs.cctv_config import CCTV_FOOTAGES


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
MODEL_PATH = os.path.join(PROJECT_ROOT, "yolo11n.pt")


class CCTVAnalyzer:

    def __init__(self):

        print("Loading CCTV AI model...")

        self.model = YOLO(MODEL_PATH)

        print("CCTV AI model loaded successfully")

        self.results = {}

    # ============================================================
    # ANALYZE ONE CAMERA
    # ============================================================

    def analyze_camera(self, footage):

        incident_id = footage["id"]
        filename = footage["file"]

        video_path = os.path.join(
            RAW_DIR,
            filename
        )

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():

            print(
                f"ERROR: Camera {incident_id} "
                f"video could not be opened"
            )

            return {
                "camera_id": incident_id,
                "video": filename,
                "status": "ERROR",
                "error": "Could not open video"
            }

        fps = cap.get(cv2.CAP_PROP_FPS)

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        if fps <= 0:
            fps = 30

        frame_count = 0

        unique_workers = set()

        max_workers = 0

        movement_events = 0

        detected_frames = 0

        # ========================================================
        # PROCESS VIDEO
        # ========================================================

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                imgsz=640,
                conf=0.20,
                classes=[0],
                verbose=False
            )

            result = results[0]

            current_workers = 0

            if (
                result.boxes is not None
                and result.boxes.id is not None
            ):

                ids = (
                    result.boxes.id
                    .int()
                    .cpu()
                    .tolist()
                )

                current_workers = len(ids)

                detected_frames += 1

                for track_id in ids:

                    unique_workers.add(track_id)

                    if frame_count > 1:
                        movement_events += 1

            max_workers = max(
                max_workers,
                current_workers
            )

        cap.release()

        duration = frame_count / fps

        # ========================================================
        # INCIDENT INTELLIGENCE
        # ========================================================

        severity = footage["severity"]

        if severity == "CRITICAL":
            risk_score = 90

        elif severity == "HIGH":
            risk_score = 70

        elif severity == "MEDIUM":
            risk_score = 40

        else:
            risk_score = 20

        # ========================================================
        # FINAL RESULT
        # ========================================================

        result_data = {

            "camera_id": incident_id,

            "video": filename,

            "status": "ANALYZED",

            "frames": frame_count,

            "fps": round(fps, 2),

            "duration": round(duration, 2),

            # Actual maximum people visible
            "workers_detected": max_workers,

            "max_workers_visible": max_workers,

            # Debug/tracking information
            "unique_track_ids": len(unique_workers),

            "detection_frames": detected_frames,

            "movement_events": movement_events,

            # Incident intelligence
            "incident": footage["title"],

            "severity": severity,

            "risk_score": risk_score,

            "alert": footage["alert"],

            "recommended_action": footage["action"]
        }

        self.results[incident_id] = result_data

        return result_data

    # ============================================================
    # ANALYZE CURRENT 3 CAMERAS
    # ============================================================

    def analyze_current_set(self):

        current = CCTV_FOOTAGES[:3]

        output = []

        print("CCTV AI analysis started...")

        for footage in current:

            result = self.analyze_camera(
                footage
            )

            output.append(result)

        print("CCTV AI analysis completed.")

        return output
import sys
import os
import threading
import cv2

from ultralytics import YOLO

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============================================================
# IMPORTS
# ============================================================

from vision.safety.zones import (
    get_zone,
    get_zone_risk,
    draw_zones
)

from vision.safety.event_detector import EventDetector
from vision.safety.risk_engine import RiskEngine
from vision.safety.movement_tracker import MovementTracker
from vision.safety.predictive_risk import PredictiveRisk

from system_state import safety_intelligence


# ============================================================
# PATHS
# ============================================================

VIDEO_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw",
    "warehouse_demo.mp4"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed"
)

OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "warehouse_safety_monitor.mp4"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "yolo11n.pt"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# MONITOR STATE
# ============================================================

monitor_status = {
    "running": False,
    "completed": False,
    "frame": 0,
    "total_frames": 0,
    "fps": 0,
    "error": None
}

stop_event = threading.Event()


# ============================================================
# SAFETY MONITOR
# ============================================================

class SafetyMonitor:

    def __init__(self):

        self.model = None

        self.cap = None
        self.out = None

        self.fps = 0
        self.width = 0
        self.height = 0
        self.total_frames = 0

        self.frame_count = 0
        self.unique_ids = set()
        self.event_count = 0

        self.event_detector = EventDetector()
        self.risk_engine = RiskEngine()
        self.movement_tracker = MovementTracker()
        self.predictive_risk = PredictiveRisk()

    # ========================================================
    # LOAD MODEL
    # ========================================================

    def load_model(self):

        print("Loading YOLO model...")

        self.model = YOLO(MODEL_PATH)

        print("YOLO model loaded successfully")

    # ========================================================
    # OPEN VIDEO
    # ========================================================

    def open_video(self):

        self.cap = cv2.VideoCapture(VIDEO_PATH)

        if not self.cap.isOpened():

            raise RuntimeError(
                f"Could not open video: {VIDEO_PATH}"
            )

        self.fps = self.cap.get(
            cv2.CAP_PROP_FPS
        )

        self.width = int(
            self.cap.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        self.height = int(
            self.cap.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        self.total_frames = int(
            self.cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        monitor_status["fps"] = self.fps
        monitor_status["total_frames"] = self.total_frames

    # ========================================================
    # CREATE OUTPUT VIDEO
    # ========================================================

    def create_output(self):

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        self.out = cv2.VideoWriter(
            OUTPUT_PATH,
            fourcc,
            self.fps,
            (self.width, self.height)
        )

    # ========================================================
    # PROCESS ONE FRAME
    # ========================================================

    def process_frame(self, frame):

        self.frame_count += 1

        # ----------------------------------------------------
        # DRAW ZONES
        # ----------------------------------------------------

        frame = draw_zones(frame)

        # ----------------------------------------------------
        # YOLO + BYTE TRACK
        # ----------------------------------------------------

        results = self.model.track(

            frame,

            persist=True,

            tracker="bytetrack.yaml",

            imgsz=1280,

            conf=0.20,

            classes=[0],

            verbose=False
        )

        result = results[0]

        # ----------------------------------------------------
        # TRACKED PEOPLE
        # ----------------------------------------------------

        if (
            result.boxes is not None
            and result.boxes.id is not None
        ):

            boxes = (
                result.boxes.xyxy
                .cpu()
                .numpy()
            )

            ids = (
                result.boxes.id
                .int()
                .cpu()
                .tolist()
            )

            for box, track_id in zip(
                boxes,
                ids
            ):

                self.unique_ids.add(
                    track_id
                )

                # ------------------------------------------------
                # BOUNDING BOX
                # ------------------------------------------------

                x1, y1, x2, y2 = map(
                    int,
                    box
                )

                # ------------------------------------------------
                # BOTTOM CENTER
                # ------------------------------------------------

                center_x = int(
                    (x1 + x2) / 2
                )

                bottom_y = y2

                point = (
                    center_x,
                    bottom_y
                )

                # ------------------------------------------------
                # MOVEMENT
                # ------------------------------------------------

                movement = (
                    self.movement_tracker.update(
                        track_id=track_id,
                        point=point,
                        frame_number=self.frame_count,
                        fps=self.fps
                    )
                )

                # ------------------------------------------------
                # PREDICTIVE RISK
                # ------------------------------------------------

                prediction = (
                    self.predictive_risk.analyze(
                        track_id,
                        point,
                        movement["velocity"],
                        self.frame_count,
                        self.fps
                    )
                )

                prediction_event = None

                if prediction is not None:

                    prediction_event = {

                        "type":
                            "PREDICTED_HAZARD_ENTRY",

                        "track_id":
                            prediction["track_id"],

                        "current_zone":
                            prediction["current_zone"],

                        "predicted_zone":
                            prediction["predicted_zone"],

                        "predicted_risk":
                            prediction["predicted_risk"],

                        "eta":
                            prediction["eta"],

                        "frame":
                            self.frame_count
                    }

                    # --------------------------------------------
                    # PREDICTED MOVEMENT
                    # --------------------------------------------

                    predicted_point = (
                        prediction["predicted_point"]
                    )

                    cv2.line(
                        frame,
                        point,
                        predicted_point,
                        (255, 0, 255),
                        3
                    )

                    # --------------------------------------------
                    # PREDICTED HAZARD POINT
                    # --------------------------------------------

                    cv2.circle(
                        frame,
                        predicted_point,
                        12,
                        (0, 0, 255),
                        -1
                    )

                    cv2.circle(
                        frame,
                        predicted_point,
                        18,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        "PREDICTED HAZARD",
                        (
                            predicted_point[0] - 70,
                            predicted_point[1] - 25
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA
                    )

                    # --------------------------------------------
                    # WARNING PANEL
                    # --------------------------------------------

                    panel_x = 20
                    panel_y = 70
                    panel_w = 400
                    panel_h = 145

                    cv2.rectangle(
                        frame,
                        (panel_x, panel_y),
                        (
                            panel_x + panel_w,
                            panel_y + panel_h
                        ),
                        (0, 0, 0),
                        -1
                    )

                    cv2.rectangle(
                        frame,
                        (panel_x, panel_y),
                        (
                            panel_x + panel_w,
                            panel_y + panel_h
                        ),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        frame,
                        "PREDICTED HAZARD",
                        (
                            panel_x + 15,
                            panel_y + 30
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA
                    )

                    cv2.putText(
                        frame,
                        f"Worker ID: {prediction['track_id']}",
                        (
                            panel_x + 15,
                            panel_y + 60
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA
                    )

                    cv2.putText(
                        frame,
                        f"Hazard: {prediction['predicted_zone']}",
                        (
                            panel_x + 15,
                            panel_y + 87
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA
                    )

                    cv2.putText(
                        frame,
                        f"ETA: {prediction['eta']} sec",
                        (
                            panel_x + 15,
                            panel_y + 114
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA
                    )

                    cv2.putText(
                        frame,
                        f"RISK: {prediction['predicted_risk']}",
                        (
                            panel_x + 220,
                            panel_y + 114
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA
                    )

                # ------------------------------------------------
                # ZONE
                # ------------------------------------------------

                zone = get_zone(point)

                risk = get_zone_risk(zone)

                # ------------------------------------------------
                # EVENTS
                # ------------------------------------------------

                events = (
                    self.event_detector.update(
                        track_id=track_id,
                        point=point,
                        zone=zone,
                        risk=risk,
                        frame_number=self.frame_count,
                        fps=self.fps
                    )
                )

                if prediction_event is not None:

                    events.append(
                        prediction_event
                    )

                # ------------------------------------------------
                # RISK SCORE
                # ------------------------------------------------

                score, risk_level = (
                    self.risk_engine.calculate_risk(
                        track_id=track_id,
                        zone=zone,
                        zone_risk=risk,
                        events=events
                    )
                )

                # ------------------------------------------------
                # SAFETY INTELLIGENCE
                # ------------------------------------------------

                safety_intelligence.update_worker(
                    track_id=track_id,
                    zone=zone,
                    risk_level=risk_level,
                    score=score,
                    events=events
                )

                # ------------------------------------------------
                # EVENT COUNT
                # ------------------------------------------------

                self.event_count += len(events)

                # ------------------------------------------------
                # DRAW PERSON
                # ------------------------------------------------

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # ------------------------------------------------
                # LABEL
                # ------------------------------------------------

                label = (
                    f"ID {track_id} | "
                    f"{zone} | "
                    f"RISK {risk_level} ({score})"
                )

                cv2.putText(
                    frame,
                    label,
                    (
                        x1,
                        max(20, y1 - 10)
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )

                # ------------------------------------------------
                # POINT
                # ------------------------------------------------

                cv2.circle(
                    frame,
                    point,
                    5,
                    (0, 0, 255),
                    -1
                )

        # ========================================================
        # GLOBAL INFORMATION
        # ========================================================

        cv2.putText(
            frame,
            f"Tracked People: {len(self.unique_ids)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        monitor_status["frame"] = self.frame_count

        return frame

    # ========================================================
    # RUN MONITOR
    # ========================================================

    def run(self):

        if monitor_status["running"]:
            print("Monitor is already running.")
            return

        monitor_status["running"] = True
        monitor_status["completed"] = False
        monitor_status["error"] = None

        try:

            print()
            print("================================")
            print("STARTING SAFETY MONITOR")
            print("================================")

            self.load_model()

            self.open_video()

            self.create_output()

            print(
                f"Video: {VIDEO_PATH}"
            )

            print(
                f"FPS: {self.fps}"
            )

            print(
                f"Resolution: "
                f"{self.width}x{self.height}"
            )

            print(
                f"Frames: "
                f"{self.total_frames}"
            )

            print()
            print(
                "Starting warehouse safety monitoring..."
            )

            while not stop_event.is_set():

                ret, frame = (
                    self.cap.read()
                )

                if not ret:
                    break

                processed_frame = (
                    self.process_frame(frame)
                )

                self.out.write(
                    processed_frame
                )

                if self.frame_count % 30 == 0:

                    print(
                        f"Processed "
                        f"{self.frame_count}/"
                        f"{self.total_frames} frames | "
                        f"Unique IDs: "
                        f"{len(self.unique_ids)}"
                    )

            monitor_status["completed"] = True

            print()
            print("================================")
            print("SAFETY MONITOR COMPLETE")
            print("================================")

            print(
                f"Processed frames: "
                f"{self.frame_count}"
            )

            print(
                f"Unique tracked IDs: "
                f"{len(self.unique_ids)}"
            )

            print(
                f"Safety events detected: "
                f"{self.event_count}"
            )

            print(
                f"Output: {OUTPUT_PATH}"
            )

            # ====================================================
            # FINAL SUMMARY
            # ====================================================

            summary = (
                safety_intelligence.get_summary()
            )

            print()
            print(
                "WAREHOUSE SAFETY INTELLIGENCE"
            )
            print("--------------------------------")

            print(
                f"Workers Tracked: "
                f"{summary['workers']}"
            )

            print(
                f"Critical Risk: "
                f"{summary['critical']}"
            )

            print(
                f"High Risk: "
                f"{summary['high']}"
            )

            print(
                f"Medium Risk: "
                f"{summary['medium']}"
            )

            print(
                f"Low Risk: "
                f"{summary['low']}"
            )

            print(
                f"Predicted Hazards: "
                f"{summary['predicted_hazards']}"
            )

            print(
                f"Total Safety Events: "
                f"{summary['total_events']}"
            )

            highest = (
                summary["highest_risk_worker"]
            )

            if highest is not None:

                print(
                    f"Highest Risk Worker: "
                    f"ID {highest['track_id']}"
                )

                print(
                    f"Highest Risk Zone: "
                    f"{highest['zone']}"
                )

                print(
                    f"Highest Risk Score: "
                    f"{highest['score']}/100"
                )

            print("--------------------------------")

        except Exception as e:

            monitor_status["error"] = str(e)

            print()
            print(
                f"MONITOR ERROR: {e}"
            )

        finally:

            if self.cap is not None:
                self.cap.release()

            if self.out is not None:
                self.out.release()

            monitor_status["running"] = False


# ============================================================
# GLOBAL MONITOR
# ============================================================

monitor = SafetyMonitor()


# ============================================================
# BACKGROUND START
# ============================================================

def start_monitor():

    if monitor_status["running"]:
        return

    stop_event.clear()

    thread = threading.Thread(
        target=monitor.run,
        daemon=True
    )

    thread.start()


# ============================================================
# STOP MONITOR
# ============================================================

def stop_monitor():

    stop_event.set()
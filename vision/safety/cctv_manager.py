import os
import threading

from configs.cctv_config import CCTV_FOOTAGES


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")


class CCTVManager:

    def __init__(self):

        self.current_index = 0
        self.set_number = 0

        self.state = {
            "running": True,
            "current_set": 1,
            "cameras": []
        }

        self.lock = threading.RLock()

        self.load_current_set()

    def load_current_set(self):

        with self.lock:

            selected = CCTV_FOOTAGES[
                self.current_index:self.current_index + 3
            ]

            cameras = []

            for camera_number, footage in enumerate(
                selected,
                start=1
            ):

                cameras.append({
                    "camera_id": camera_number,
                    "incident_id": footage["id"],
                    "file": footage["file"],
                    "title": footage["title"],
                    "severity": footage["severity"],
                    "alert": footage["alert"],
                    "action": footage["action"],
                    "video": f"/api/camera/{footage['id']}"
                })

            self.state["cameras"] = cameras

    def next_set(self):

        with self.lock:

            self.current_index += 3

            if self.current_index >= len(CCTV_FOOTAGES):
                self.current_index = 0

            self.set_number += 1

            self.state["current_set"] = self.set_number + 1

            self.load_current_set()

    def get_state(self):

        with self.lock:
            return {
                "running": self.state["running"],
                "current_set": self.state["current_set"],
                "cameras": list(self.state["cameras"])
            }
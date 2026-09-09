"""
Warehouse Safety Event Detector

Tracks worker movement over time and generates safety events.
"""

import math


class EventDetector:

    def __init__(self):
        self.worker_history = {}

    def update(self, track_id, point, zone, risk, frame_number, fps):
        """
        Update one worker's state and return detected events.
        """

        if track_id not in self.worker_history:
            self.worker_history[track_id] = {
                "first_frame": frame_number,
                "last_frame": frame_number,
                "last_point": point,
                "last_zone": zone,
                "zone_start_frame": frame_number
            }

            return []

        worker = self.worker_history[track_id]

        previous_zone = worker["last_zone"]
        previous_point = worker["last_point"]

        events = []

        # ------------------------------------------------
        # 1. Zone entry
        # ------------------------------------------------

        if zone != previous_zone:

            events.append({
                "type": "ZONE_CHANGE",
                "track_id": track_id,
                "from_zone": previous_zone,
                "to_zone": zone,
                "frame": frame_number
            })

            worker["zone_start_frame"] = frame_number

        # ------------------------------------------------
        # 2. High-risk zone entry
        # ------------------------------------------------

        if zone != previous_zone and risk in ["HIGH", "CRITICAL"]:

            events.append({
                "type": "HIGH_RISK_ENTRY",
                "track_id": track_id,
                "zone": zone,
                "risk": risk,
                "frame": frame_number
            })

        # ------------------------------------------------
        # 3. Dwell time
        # ------------------------------------------------

        zone_duration = (
            frame_number - worker["zone_start_frame"]
        ) / fps

        if risk in ["HIGH", "CRITICAL"] and zone_duration >= 3:

            events.append({
                "type": "LONG_DWELL",
                "track_id": track_id,
                "zone": zone,
                "duration": round(zone_duration, 2),
                "risk": risk,
                "frame": frame_number
            })

            # Reset timer so we don't generate this every frame
            worker["zone_start_frame"] = frame_number

        # ------------------------------------------------
        # 4. Movement speed
        # ------------------------------------------------

        dx = point[0] - previous_point[0]
        dy = point[1] - previous_point[1]

        distance = math.sqrt(dx * dx + dy * dy)

        time_difference = (
            frame_number - worker["last_frame"]
        ) / fps

        if time_difference > 0:

            speed = distance / time_difference

            # Large sudden movement
            if speed > 500:

                events.append({
                    "type": "SUDDEN_MOVEMENT",
                    "track_id": track_id,
                    "speed": round(speed, 2),
                    "zone": zone,
                    "frame": frame_number
                })

        # ------------------------------------------------
        # Update worker state
        # ------------------------------------------------

        worker["last_point"] = point
        worker["last_zone"] = zone
        worker["last_frame"] = frame_number

        return events
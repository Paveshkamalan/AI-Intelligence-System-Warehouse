"""
Worker Movement Tracker

Maintains position history and estimates
worker movement velocity.
"""

import math


class MovementTracker:

    def __init__(self, history_size=15):
        self.history_size = history_size
        self.workers = {}

    def update(self, track_id, point, frame_number, fps):

        if track_id not in self.workers:
            self.workers[track_id] = {
                "positions": [],
                "velocity": (0.0, 0.0),
                "speed": 0.0,
                "direction": (0.0, 0.0),
                "last_frame": frame_number
            }

        worker = self.workers[track_id]

        worker["positions"].append(
            (frame_number, point)
        )

        if len(worker["positions"]) > self.history_size:
            worker["positions"].pop(0)

        # Need at least two positions
        if len(worker["positions"]) >= 2:

            old_frame, old_point = worker["positions"][0]
            new_frame, new_point = worker["positions"][-1]

            frame_difference = new_frame - old_frame

            if frame_difference > 0:

                time_difference = frame_difference / fps

                dx = new_point[0] - old_point[0]
                dy = new_point[1] - old_point[1]

                vx = dx / time_difference
                vy = dy / time_difference

                speed = math.sqrt(
                    vx * vx + vy * vy
                )

                if speed > 0:
                    direction = (
                        vx / speed,
                        vy / speed
                    )
                else:
                    direction = (0.0, 0.0)

                worker["velocity"] = (vx, vy)
                worker["speed"] = speed
                worker["direction"] = direction

        worker["last_frame"] = frame_number

        return {
            "velocity": worker["velocity"],
            "speed": worker["speed"],
            "direction": worker["direction"]
        }

    def predict_position(self, track_id, seconds_ahead=1.0):

        if track_id not in self.workers:
            return None

        worker = self.workers[track_id]

        if not worker["positions"]:
            return None

        _, current_point = worker["positions"][-1]

        vx, vy = worker["velocity"]

        predicted_x = current_point[0] + vx * seconds_ahead
        predicted_y = current_point[1] + vy * seconds_ahead
        return (
                int(predicted_x),
                int(predicted_y)
        )

    def get_speed(self, track_id):
        if track_id not in self.workers:
            return 0.0

        return self.workers[track_id]["speed"]

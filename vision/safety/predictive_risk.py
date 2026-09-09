"""
Predictive Safety Risk Engine

Predicts whether a worker is moving toward a
high-risk or critical warehouse zone and estimates
time-to-hazard.
"""

import math

from vision.safety.zones import get_zone, get_zone_risk


class PredictiveRisk:

    def __init__(self, prediction_horizon=2.0, cooldown=2.0):

        # How far into the future we predict
        self.prediction_horizon = prediction_horizon

        # Prevent the same prediction from being
        # printed repeatedly
        self.cooldown = cooldown

        self.last_predictions = {}

        self.prediction_events = 0

    def analyze(
        self,
        track_id,
        current_point,
        velocity,
        current_frame,
        fps
    ):

        if velocity is None:
            return None

        vx, vy = velocity

        speed = math.sqrt(vx * vx + vy * vy)

        # Worker is essentially stationary
        if speed < 20:
            return None

        current_zone = get_zone(current_point)

        # Predict position in the future
        predicted_x = int(
            current_point[0] + vx * self.prediction_horizon
        )

        predicted_y = int(
            current_point[1] + vy * self.prediction_horizon
        )

        predicted_point = (
            predicted_x,
            predicted_y
        )

        predicted_zone = get_zone(predicted_point)

        predicted_risk = get_zone_risk(predicted_zone)

        # No dangerous zone ahead
        if predicted_zone == current_zone:
            return None

        if predicted_risk not in ["HIGH", "CRITICAL"]:
            return None

        # Estimate distance to predicted position
        dx = predicted_point[0] - current_point[0]
        dy = predicted_point[1] - current_point[1]

        distance = math.sqrt(dx * dx + dy * dy)

        # Estimate time to reach predicted point
        if speed > 0:
            eta = distance / speed
        else:
            eta = self.prediction_horizon

        eta = min(eta, self.prediction_horizon)

        # Duplicate suppression
        prediction_key = (
            track_id,
            predicted_zone
        )

        current_time = current_frame / fps

        last_time = self.last_predictions.get(
            prediction_key,
            -999
        )

        if current_time - last_time < self.cooldown:
            return None

        self.last_predictions[prediction_key] = current_time

        self.prediction_events += 1

        return {
            "type": "PREDICTED_HAZARD_ENTRY",

            "track_id": track_id,

            "current_zone": current_zone,

            "predicted_zone": predicted_zone,

            "predicted_risk": predicted_risk,

            "current_point": current_point,

            "predicted_point": predicted_point,

            "speed": round(speed, 2),

            "distance": round(distance, 2),

            "eta": round(eta, 2)
        }

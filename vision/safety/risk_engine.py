"""
Warehouse Safety Risk Engine

Maintains persistent risk for every tracked worker.
"""

class RiskEngine:

    def __init__(self):
        self.worker_risks = {}

    def calculate_risk(
        self,
        track_id,
        zone,
        zone_risk,
        events
    ):

        base_scores = {
            "LOW": 10,
            "MEDIUM": 30,
            "HIGH": 55,
            "CRITICAL": 80,
            "UNKNOWN": 0
        }

        # Create worker state
        if track_id not in self.worker_risks:

            self.worker_risks[track_id] = {
                "score": base_scores.get(zone_risk, 0),
                "level": "LOW",
                "zone": zone,
                "events": 0
            }

        worker = self.worker_risks[track_id]

        # Update zone
        worker["zone"] = zone

        # Slowly move score toward the current zone risk.
        # This prevents a worker from keeping an old
        # extremely high score forever after leaving danger.
        base_score = base_scores.get(zone_risk, 0)

        worker["score"] = max(
            worker["score"] - 1,
            base_score
        )

        # Add risk from events
        for event in events:

            event_type = event["type"]

            worker["events"] += 1

            if event_type == "HIGH_RISK_ENTRY":
                worker["score"] += 15

            elif event_type == "LONG_DWELL":
                worker["score"] += 10

            elif event_type == "SUDDEN_MOVEMENT":
                worker["score"] += 1

            elif event_type == "ZONE_CHANGE":
                worker["score"] += 2

            elif event_type == "PREDICTED_HAZARD_ENTRY":
                worker["score"] += 12

        # Limit score
        worker["score"] = min(
            worker["score"],
            100
        )

        # Determine level
        if worker["score"] >= 75:
            worker["level"] = "CRITICAL"

        elif worker["score"] >= 50:
            worker["level"] = "HIGH"

        elif worker["score"] >= 25:
            worker["level"] = "MEDIUM"

        else:
            worker["level"] = "LOW"

        return (
            worker["score"],
            worker["level"]
        )
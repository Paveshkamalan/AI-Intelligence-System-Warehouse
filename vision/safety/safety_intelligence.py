"""
Warehouse Safety Intelligence

Maintains warehouse-level safety statistics,
event history, and worker risk information.
"""


class SafetyIntelligence:

    def __init__(self, max_events=100):

        self.max_events = max_events

        # Complete event history
        self.event_history = []

        # Event counters
        self.event_counts = {
            "ZONE_CHANGE": 0,
            "HIGH_RISK_ENTRY": 0,
            "LONG_DWELL": 0,
            "SUDDEN_MOVEMENT": 0,
            "PREDICTED_HAZARD_ENTRY": 0
        }

        # Current worker states
        self.workers = {}

    def update_worker(
        self,
        track_id,
        zone,
        risk_level,
        score,
        events
    ):

        # Store latest worker state
        self.workers[track_id] = {
            "zone": zone,
            "risk_level": risk_level,
            "score": score
        }

        # Process events
        for event in events:

            event_type = event["type"]

            if event_type in self.event_counts:
                self.event_counts[event_type] += 1

            # Add useful metadata
            event_record = dict(event)

            event_record["worker_risk"] = risk_level
            event_record["worker_score"] = score

            self.event_history.append(event_record)

        # Keep history limited
        if len(self.event_history) > self.max_events:

            self.event_history = self.event_history[
                -self.max_events:
            ]

    def get_worker_count(self):
        return len(self.workers)

    def get_risk_counts(self):

        counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        for worker in self.workers.values():

            level = worker["risk_level"]

            if level in counts:
                counts[level] += 1

        return counts

    def get_prediction_count(self):

        return self.event_counts[
            "PREDICTED_HAZARD_ENTRY"
        ]

    def get_total_events(self):

        return len(self.event_history)

    def get_highest_risk_worker(self):

        if not self.workers:
            return None

        highest_id = max(
            self.workers,
            key=lambda worker_id:
                self.workers[worker_id]["score"]
        )

        return {
            "track_id": highest_id,
            **self.workers[highest_id]
        }

    def get_summary(self):

        risk_counts = self.get_risk_counts()
        highest = self.get_highest_risk_worker()

        return {
            "workers": self.get_worker_count(),
            "critical": risk_counts["CRITICAL"],
            "high": risk_counts["HIGH"],
            "medium": risk_counts["MEDIUM"],
            "low": risk_counts["LOW"],
            "predicted_hazards": self.get_prediction_count(),
            "total_events": self.get_total_events(),
            "highest_risk_worker": highest
        }
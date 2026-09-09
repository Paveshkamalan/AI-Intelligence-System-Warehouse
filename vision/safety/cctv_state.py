class CCTVState:

    def __init__(self):
        self.results = []

    def set_results(self, results):
        self.results = results

    def get_results(self):
        return self.results

    def get_summary(self):

        if not self.results:
            return {
                "cameras": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "highest_risk": 0
            }

        critical = sum(
            1 for r in self.results
            if r.get("severity") == "CRITICAL"
        )

        high = sum(
            1 for r in self.results
            if r.get("severity") == "HIGH"
        )

        medium = sum(
            1 for r in self.results
            if r.get("severity") == "MEDIUM"
        )

        low = sum(
            1 for r in self.results
            if r.get("severity") == "LOW"
        )

        highest = max(
            self.results,
            key=lambda r: r.get("risk_score", 0)
        )

        return {
            "cameras": len(self.results),
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
            "highest_risk": highest.get("risk_score", 0),
            "highest_camera": highest.get("camera_id"),
            "highest_incident": highest.get("incident")
        }


cctv_state = CCTVState()
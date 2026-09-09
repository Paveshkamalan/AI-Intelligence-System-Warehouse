from vision.safety.cctv_analyzer import CCTVAnalyzer


analyzer = CCTVAnalyzer()

results = analyzer.analyze_current_set()

print()
print("=" * 60)
print("FINAL CCTV AI RESULTS")
print("=" * 60)

for result in results:

    print()
    print(
        f"CAMERA {result['camera_id']}"
    )

    print(
        f"Workers: "
        f"{result.get('workers_detected', 0)}"
    )

    print(
        f"Risk: "
        f"{result.get('severity', 'UNKNOWN')}"
    )

    print(
        f"Score: "
        f"{result.get('risk_score', 0)}/100"
    )

    print(
        f"Incident: "
        f"{result.get('incident', '')}"
    )

    print(
        f"Alert: "
        f"{result.get('alert', '')}"
    )
import os
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from system_state import safety_intelligence
from vision.safety.safety_monitor import (
    start_monitor,
    stop_monitor,
    monitor_status
)
from configs.cctv_config import CCTV_FOOTAGES
from vision.safety.cctv_manager import CCTVManager
from vision.safety.cctv_analyzer import CCTVAnalyzer
from vision.safety.cctv_state import cctv_state

FRONTEND_DIR = os.path.join(
    os.path.dirname(__file__),
    "frontend"
)

def run_cctv_analysis():
    try:
        analyzer = CCTVAnalyzer()
        results = analyzer.analyze_current_set()
        cctv_state.set_results(results)
    except Exception as e:
        print(f"CCTV analysis error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n================================")
    print("WAREHOUSE SAFETY AI API")
    print("================================")
    print("Starting safety monitoring...")

    start_monitor()
    threading.Thread(
        target=run_cctv_analysis,
        daemon=True
    ).start()

    yield

    print("Stopping safety monitoring...")
    stop_monitor()


app = FastAPI(
    title="Warehouse Safety AI",
    description="AI-powered warehouse safety monitoring API",
    version="1.0.0",
    lifespan=lifespan
)
cctv_manager = CCTVManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/")
def root():
    return {
        "system": "Warehouse Safety AI",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/monitor")
def get_monitor_status():
    return monitor_status


@app.get("/api/status")
def get_status():
    return safety_intelligence.get_summary()


@app.get("/api/workers")
def get_workers():

    workers = []

    for track_id, data in safety_intelligence.workers.items():
        workers.append({
            "track_id": track_id,
            **data
        })

    return {
        "workers": workers
    }


@app.get("/api/events")
def get_events():
    return {
        "events": safety_intelligence.event_history
    }

@app.get("/dashboard")
def dashboard():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "index.html")
    )

@app.get("/api/video")
def get_video():
    video_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "processed",
        "warehouse_safety_monitor_h264.mp4"
    )

    return FileResponse(
        video_path,
        media_type="video/mp4"
    )

@app.get("/style.css")
def style():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "style.css"),
        media_type="text/css"
    )


@app.get("/app.js")
def javascript():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "app.js"),
        media_type="application/javascript"
    )

@app.get("/api/cctv")
def get_cctv():

    return cctv_manager.get_state()

@app.post("/api/cctv/next")
def next_cctv_set():

    cctv_manager.next_set()

    return cctv_manager.get_state()

@app.get("/api/camera/{incident_id}")
def get_camera_video(incident_id: int):

    footage = next(
        (
            item for item in CCTV_FOOTAGES
            if item["id"] == incident_id
        ),
        None
    )

    if footage is None:
        return {"error": "Camera footage not found"}

    video_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "raw",
        footage["file"]
    )

    return FileResponse(
        video_path,
        media_type="video/mp4"
    )

@app.get("/api/cctv/results")
def get_cctv_results():
    return {
        "cameras": cctv_state.get_results(),
        "summary": cctv_state.get_summary()
    }

def run_cctv_analysis():
    try:
        analyzer = CCTVAnalyzer()
        results = analyzer.analyze_current_set()
        cctv_state.set_results(results)
        print("CCTV AI analysis completed.")
    except Exception as e:
        print(f"CCTV analysis error: {e}")


# START CCTV AI ANALYSIS
threading.Thread(
    target=run_cctv_analysis,
    daemon=True
).start()
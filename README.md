# 🏭 Warehouse Safety Intelligence Platform

An AI-powered warehouse safety monitoring system that uses computer vision, worker tracking, risk analysis, and CCTV intelligence to identify and prioritize workplace safety hazards.

## 🚀 Overview

The Warehouse Safety Intelligence Platform analyzes CCTV footage to detect workers, track their movement, identify safety incidents, calculate risk levels, and provide recommended safety actions.

The system combines:

* YOLO-based object detection
* ByteTrack multi-object tracking
* Worker-level tracking
* Safety risk scoring
* Zone-based risk analysis
* CCTV incident analysis
* Predictive risk analysis
* FastAPI backend
* Real-time web dashboard

## 🧠 System Architecture

CCTV / Video Footage
        ↓
YOLO Object Detection
        ↓
ByteTrack Worker Tracking
        ↓
Zone & Safety Analysis
        ↓
Incident Detection
        ↓
Risk Engine
        ↓
Predictive Risk Analysis
        ↓
Safety Intelligence
        ↓
FastAPI Backend
        ↓
Web Dashboard

## ✨ Key Features

### 1. Worker Detection

Detects workers from warehouse CCTV footage using YOLO.

### 2. Persistent Tracking

ByteTrack assigns tracking IDs to detected workers, allowing the system to monitor workers across video frames.

### 3. Safety Risk Analysis

Each detected incident is assigned a severity level:

* LOW
* MEDIUM
* HIGH
* CRITICAL

### 4. CCTV Intelligence

The system analyzes multiple warehouse incident scenarios and provides:

* Incident type
* Severity
* Risk score
* Workers detected
* Detection coverage
* Safety alert
* Recommended action

### 5. Safety Dashboard

The web dashboard provides a centralized view of warehouse safety intelligence.

It includes:

* CCTV feeds
* Risk overview
* Worker information
* Safety events
* Incident analysis
* AI safety intelligence

## 🎥 Supported Safety Scenarios

The current demonstration dataset includes scenarios such as:

* Unsafe material handling
* Improper heavy-load stacking
* Wet-floor hazards
* Unsafe carton handling
* Unsafe storage practices
* Unsafe material throwing

## 🛠️ Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming          | Python                |
| Computer Vision      | OpenCV                |
| Object Detection     | YOLO                  |
| Tracking             | ByteTrack             |
| Backend              | FastAPI               |
| Frontend             | HTML, CSS, JavaScript |
| Numerical Processing | NumPy                 |
| Video Processing     | OpenCV / FFmpeg       |

## 📁 Project Structure

warehouse-ai/
│
├── configs/
│   └── cctv_config.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── vision/
│   └── safety/
│       ├── cctv_analyzer.py
│       ├── cctv_manager.py
│       ├── cctv_state.py
│       ├── event_detector.py
│       ├── movement_tracker.py
│       ├── predictive_risk.py
│       ├── risk_engine.py
│       ├── safety_intelligence.py
│       ├── safety_monitor.py
│       └── zones.py
│
├── api.py
├── system_state.py
├── yolo11n.pt
├── requirements.txt
├── .gitignore
└── README.md

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Paveshkamalan/warehouse-safety-ai.git
cd warehouse-safety-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/dashboard
```

## 📊 Example System Output

WAREHOUSE SAFETY INTELLIGENCE

Workers Tracked: 7
Critical Risk: 0
High Risk: 5
Medium Risk: 1
Low Risk: 1
Predicted Hazards: 2
Total Safety Events: 6

Highest Risk Worker: ID 9
Highest Risk Zone: Loading Bay
Highest Risk Score: 60/100

## 🔮 Future Improvements

Potential future extensions include:

* Automatic CCTV feed rotation
* LLM-powered Safety Agent
* Automated incident report generation
* Historical safety analytics
* Advanced action recognition
* Real-time alerts
* Email/SMS notifications
* Warehouse digital twin
* Edge AI deployment

## 🏆 Hackathon Project

This project was developed as an AI-powered warehouse safety intelligence solution focused on moving beyond simple object detection toward worker-centric, contextual, and predictive safety monitoring.

## 👨‍💻 Author

**Pavesh Kamalan R**

B.Tech Computer Science Engineering
Vellore Institute of Technology

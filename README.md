🏭 AI Video Intelligence for Warehouse Handling

An AI-powered Field Intelligence Assistant that transforms warehouse
video into actionable safety intelligence---identifying damage-causing
handling risks, tracking activity, prioritizing incidents, and
enabling early intervention.

🏆 Project Vision

Warehouses process thousands of products through loading, unloading,
movement, stacking, pallet handling, and material transfer every day.

Many operational incidents and product-damage risks are not caused by
equipment failure. They emerge from how materials are handled:

Dropping or throwing products

Dragging products instead of using suitable equipment

Improper or unstable stacking

Rough handling

Unsafe movement

Incorrect product positioning

Unsafe loading and unloading practices

Traditional CCTV answers:

"What happened?"

This project moves toward:

"What is happening, why is it risky, and what should the team do
next?"

The platform converts conventional video surveillance into an
AI-powered operational intelligence layer focused on prevention rather
than retrospective investigation.

🎯 Challenge Alignment

The solution is designed around the challenge's intended evolution:

Traditional CCTV
Camera
   ↓
Recording
   ↓
Human Review
   ↓
Incident Discovered
   ↓
Corrective Action

→ AI Field Intelligence

Camera
   ↓
AI Perception
   ↓
Object Detection & Tracking
   ↓
Behaviour / Incident Context
   ↓
Risk Classification
   ↓
Alert & Recommendation
   ↓
Early Intervention
   ↓
Damage Prevention

The central objective is not simply to monitor people.

It is to identify behaviours and conditions that could cause product
damage or unsafe warehouse operations, allowing teams to intervene
earlier.

💡 What Makes the Approach Different?

A basic computer-vision system can detect a person or object in a frame.

This platform adds multiple intelligence layers:

DETECT
  ↓
TRACK
  ↓
UNDERSTAND CONTEXT
  ↓
IDENTIFY RISK
  ↓
PRIORITIZE
  ↓
PREDICT
  ↓
RECOMMEND ACTION
  ↓
PREVENT

From pixels to operational decisions

Instead of generating thousands of disconnected detections, the system
organizes visual observations into worker activity, incident context,
risk levels, safety events, and recommended intervention.

🧠 System Architecture

                    ┌──────────────────────┐
                    │   CCTV / Video Input │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Video Ingestion    │
                    │     OpenCV            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   YOLO Detection     │
                    │   Person Detection   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ByteTrack          │
                    │ Persistent Tracking  │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │     Context & Safety Layer      │
              │                                 │
              │ Zones • Movement • Incidents    │
              └───────────────┬─────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │    Risk Engine       │
                    │ Severity + Scoring   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Predictive Risk      │
                    │ Intelligence         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Safety Intelligence  │
                    │ Workers • Events     │
                    │ Zones • Risk         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI          │
                    │   REST API Layer     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Safety Operations    │
                    │ Dashboard            │
                    └──────────────────────┘

🔥 Core Capabilities

01 --- AI Video Perception

The system ingests recorded warehouse footage and applies computer
vision to identify workers and track visual activity across frames.

Technology

YOLO

OpenCV

ByteTrack

02 --- Persistent Worker Tracking

Instead of treating every frame independently, detected workers are
assigned persistent tracking identities.

Frame 01 ──┐
Frame 02 ──┤
Frame 03 ──┼──► Worker ID
Frame 04 ──┤
Frame N  ──┘

This provides temporal context for worker-centric safety analysis.

03 --- Zone-Based Risk Intelligence

Warehouse locations can have different operational risk profiles.

The system incorporates zone context into safety analysis, allowing the
same worker activity to be evaluated differently depending on where it
occurs.

Example zones include:

Loading Bay

Vehicle Zone

Worker Operating Area

Wet Hazard Zone

Walkway

Storage Area

04 --- Incident & Behaviour Intelligence

The current demonstration configuration covers warehouse handling
scenarios including:

#   Demonstration Scenario               Risk

01   Unsafe Material Handling             HIGH
02   Improper Heavy Load Stacking         CRITICAL
03   Wet Floor Safety Hazard              CRITICAL
04   Unsafe Carton Handling               HIGH
05   Multiple Storage Violations          CRITICAL
06   Unsafe Material Throwing             HIGH
07   Unsafe Carton Handling / Strap Use   HIGH

The architecture is designed to expand the behaviour taxonomy as
additional validated scenarios and trained behaviour models become
available.

🚨 Risk Classification

The system converts incident context into a structured risk level and
score.

LOW       → 20
MEDIUM    → 40
HIGH      → 70
CRITICAL  → 90

A risk record can contain:

Incident type

Severity

Risk score

Worker visibility

Detection coverage

Safety alert

Recommended corrective action

Example

CAMERA 02
────────────────────────────────

Incident:
Improper Heavy Load Stacking

Severity:
CRITICAL

Risk Score:
90 / 100

Alert:
Heavy product detected on improperly stacked packets.

Recommended Action:
Stop activity and correct stacking immediately.

🔮 Predictive Risk Intelligence

The platform includes a predictive-risk layer to move safety monitoring
beyond retrospective detection.

Current Observation
        ↓
Movement + Zone + Risk Context
        ↓
Emerging Hazard
        ↓
Potential Future Risk
        ↓
Early Intervention

The objective is to help supervisors act before a potential incident
becomes product damage or a safety event.

🧠 Central Safety Intelligence

The platform aggregates safety information into a centralized
operational state.

The dashboard can surface:

Workers tracked

Critical-risk workers/events

High-risk workers/events

Medium and low risk

Predicted hazards

Total safety events

Highest-risk worker

Highest-risk zone

Highest-risk score

Example system output:

WAREHOUSE SAFETY INTELLIGENCE
──────────────────────────────

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

📹 Multi-Camera CCTV Intelligence

The prototype includes a multi-camera architecture for analyzing
warehouse footage.

             ┌───────────────┐
             │   CAMERA 01   │
             └───────┬───────┘
                     │
             ┌───────▼───────┐
             │   CAMERA 02   │
             └───────┬───────┘
                     │
             ┌───────▼───────┐
             │   CAMERA 03   │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │ CCTV AI Engine│
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │   Risk & AI   │
             │ Intelligence  │
             └───────────────┘

The architecture can later be connected to live RTSP/VMS feeds instead
of recorded demonstration footage.

🖥️ Safety Operations Dashboard

The web dashboard acts as the operational command center.

Dashboard capabilities

📹 CCTV video monitoring

👷 Worker tracking

🚨 Safety event visibility

📊 Risk overview

🎯 Risk scoring

🗺️ Zone-aware intelligence

🔮 Predictive hazard information

🧠 Central safety intelligence

⚠️ Recommended corrective actions

The design goal is simple:

Give a warehouse supervisor the information required to understand
risk and intervene quickly.

🏗️ Project Structure

AI-Intelligence-System-Warehouse/
│
├── configs/
│   └── cctv_config.py
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
├── test_cctv.py
├── requirements.txt
├── yolo11n.pt
├── .gitignore
└── README.md

🛠️ Technology Stack

Layer                   Technology

Programming             Python
Computer Vision         OpenCV
Object Detection        YOLO
Multi-Object Tracking   ByteTrack
Numerical Processing    NumPy
Backend                 FastAPI
Frontend                HTML / CSS / JavaScript
Video Processing        FFmpeg
API Communication       REST

⚙️ Installation

Prerequisites

Python 3.x

Git

FFmpeg

Windows, Linux, or macOS

A machine capable of running YOLO inference

1. Clone the repository

git clone https://github.com/Paveshkamalan/AI-Intelligence-System-Warehouse.git
cd AI-Intelligence-System-Warehouse

2. Create a virtual environment

Windows

python -m venv .venv
.venv\Scripts\activate

Linux / macOS

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

📹 Video Dataset

Large demonstration video files are intentionally excluded from the Git
repository.

Create:

data/
└── raw/

and place the required CCTV footage inside:

data/raw/

The configured filenames and scenario metadata are maintained in:

configs/cctv_config.py

This keeps the source repository lightweight while allowing the
application to operate on the supplied warehouse footage.

▶️ Running the Application

Start the FastAPI application:

uvicorn api:app --reload

Then open:

http://127.0.0.1:8000/dashboard

🔌 API

The backend exposes REST endpoints for the dashboard and monitoring
system.

Endpoint              Purpose

/                   System information
/api/health         Health check
/api/status         Safety intelligence summary
/api/workers        Worker tracking data
/api/events         Safety event history
/api/monitor        Monitor status
/api/cctv           CCTV configuration/state
/api/cctv/results   CCTV AI analysis results
/api/video          Processed monitoring video
/api/camera/{id}    CCTV footage endpoint

🔬 AI Strategy

The system is intentionally designed as a layered intelligence pipeline.

Layer 1 --- Perception

Video → Detection

Understand what is visible.

Layer 2 --- Tracking

Detection → Persistent Objects / Workers

Understand what continues across time.

Layer 3 --- Context

Tracking + Zone + Movement + Incident Context

Understand where and under what conditions activity occurs.

Layer 4 --- Risk

Context → Severity → Risk Score

Prioritize what requires attention.

Layer 5 --- Prediction

Current Risk + Movement + Context
                 ↓
          Emerging Hazard

Identify situations that may require intervention.

Layer 6 --- Action

Risk → Alert → Recommended Action

Convert AI output into an operational decision.

🎯 Prevention-First Design

The platform is designed around a fundamental operational shift:

Damage Detection
       ↓
Damage Prevention

Instead of only reporting:

"A product was damaged."

the desired operational outcome is:

"A high-risk handling behaviour was identified early enough for
corrective intervention."

This makes the system valuable even when damage has not yet
occurred.

👥 Intended Users

The platform is designed for operational roles such as:

Warehouse Supervisors

Loading / Unloading Operators

Logistics Managers

Quality Professionals

Safety Professionals

Each role can use the intelligence layer to understand risky processes
and improve handling discipline.

📈 Success Metrics

The architecture supports measuring more than model accuracy.

AI Performance

Behaviour detection accuracy

Precision / recall

False-positive rate

Detection latency

Operational Performance

High-risk events per shift

Repeat behaviour frequency

Average response time

Risk events by loading bay

Business Impact

Potential damage events prevented

Reduction in handling-related incidents

Reduction in product damage

Reduction in rework / replacement

Estimated financial impact

Human Impact

Supervisor usability

Operator acceptance

Training opportunities identified

User feedback score

🔐 Responsible AI

Warehouse video intelligence must be used for process improvement and
prevention, not indiscriminate employee surveillance.

The production architecture should therefore consider:

Privacy

Employee transparency and consent

Data minimization

Secure video storage

Role-based access

Appropriate data-retention periods

Human review of significant incidents

False-positive management

Explainable alerts

Avoiding automated punitive decisions

Bias and performance across operating conditions

The system should distinguish:

Observed Behaviour
        ↓
Potential Risk
        ↓
Confirmed Damage

A potential risk should not automatically be presented as confirmed
product damage without sufficient evidence.

🚀 Roadmap

Phase 1 --- Current Prototype

Video ingestion

YOLO worker detection

ByteTrack tracking

Safety zones

Movement analysis

Safety event detection

Risk engine

Predictive risk layer

Multi-camera architecture

FastAPI backend

Web safety dashboard

Recommended safety actions

Phase 2 --- Behaviour Intelligence

Expand to 10+ validated behaviour scenarios

Temporal action recognition

Product/object-specific tracking

Drop and impact detection

Loading-sequence verification

Pallet stability assessment

Phase 3 --- AI Warehouse Assistant

Conversational AI supervisor assistant

Natural-language incident explanations

"Why was this event high risk?" reasoning

Shift-level summaries

Automated incident reports

Safety training recommendations

Phase 4 --- Production Intelligence

Live RTSP CCTV streams

Edge AI deployment

Real-time notifications

Historical analytics

Behaviour heat maps

Product-specific risk models

Forklift / pedestrian interaction monitoring

PPE compliance

Warehouse management integration

CCTV/VMS integration

Multi-warehouse monitoring

🌐 Long-Term Vision

The ultimate vision is to evolve the platform from a warehouse CCTV
solution into an AI Field Intelligence Platform for Physical
Operations.

Warehouse
    ↓
Factory
    ↓
Distribution Centre
    ↓
Loading Bay
    ↓
Retail
    ↓
Field Service

The same architecture can eventually understand complete physical
processes rather than isolated visual events.

Long-term intelligence loop

PERCEIVE
   ↓
UNDERSTAND
   ↓
ASSESS
   ↓
PREDICT
   ↓
INTERVENE
   ↓
LEARN
   ↓
IMPROVE OPERATIONS

🏆 Project Impact

From:

CCTV Surveillance

To:

Operational Intelligence

From:

Incident Investigation

To:

Early Intervention

From:

Damage Detection

To:

Damage Prevention

👨‍💻 Author

Pavesh Kamalan

B.Tech Computer Science Engineering
Vellore Institute of Technology

📜 License

This project is intended as a hackathon / prototype implementation.

See the repository for applicable licensing information.

⭐ Final Takeaway

The goal is not to build another CCTV system.

The goal is to build an AI field intelligence layer that understands
warehouse activity, identifies behaviours that could cause damage,
prioritizes risk, and helps people intervene before the incident
becomes a loss.

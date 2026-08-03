# RoadVision: AI-Powered Intelligent Road Damage Detection & Monitoring System

RoadVision is an enterprise-grade AI, Computer Vision, and Smart City MLOps platform designed to automate urban road surface damage inspection. Built as a **Flutter Mobile Application (`flutter_app/`)** backed by a **FastAPI Backend (`backend/`)**, **YOLOv11 + MiDaS AI Engine (`ai/`)**, and **PostGIS 10m Spatial Buffer Deduplication (`database/`)**.

---

## 🏛 Project Architecture & Folder Structure

```
RoadVision/
├── flutter_app/                # Flutter Mobile Application (Citizen + Admin Roles)
│   ├── lib/
│   │   ├── config/             # Theme & color palette
│   │   ├── services/           # FastAPI HTTP client service
│   │   ├── screens/
│   │   │   ├── auth/           # Login & Registration
│   │   │   ├── citizen/        # Report Damage, Nearby Defects, Emergency Contact
│   │   │   └── admin/          # Overview, Analytics, GIS Map, Repair Lifecycle
│   │   └── main.dart
│   └── pubspec.yaml
├── backend/                    # Production FastAPI Backend Service
│   ├── api/                    # REST routers & Pydantic schemas
│   ├── config/                 # Environment settings
│   └── main.py                 # FastAPI application launcher
├── ai/                         # Deep Learning & Computer Vision Engine
│   ├── depth_estimator.py      # MiDaS Monocular Depth & 3D Metric Calculator
│   ├── geocoding.py            # Reverse Geocoding via Nominatim
│   ├── image_processing.py     # OpenCV CLAHE & Bilateral noise filter
│   ├── model_loader.py         # YOLO detector singleton
│   ├── pipeline.py             # Integrated Core AI Pipeline
│   ├── road_health.py          # Road Health Score (0-100%) & Condition Evaluator
│   └── severity_engine.py      # Priority Score Matrix (0-100)
├── database/                   # PostGIS Spatial Database & ORM
│   ├── db.py                   # Async 10m spatial buffer deduplication (`ST_DWithin`)
│   └── schema.sql              # PostGIS DDL schema & 8-Stage Repair Lifecycle
├── docker/                     # Container Deployment
│   ├── Dockerfile.api
│   └── docker-compose.yml
├── docs/                       # Project Documentation & Architecture Diagrams
│   ├── AI_PIPELINE_DIAGRAM.md
│   ├── GOVERNMENT_FLEET_WORKFLOW.md
│   ├── REPAIR_LIFECYCLE.md
│   ├── SRS.md
│   └── USE_CASE_DIAGRAM.md
├── .github/                    # CI/CD Workflows
│   └── workflows/ci.yml
├── requirements.txt            # Python dependencies
└── test_inference.py          # Integration test script
```

---

## 🚗 1. Government Fleet Continuous Inspection Workflow

```
               [ Government Bus / Garbage Collection Truck ]
                                    │
                                    ▼
                         [ Front Dashboard Camera ]
                                    │
                       (Captures Frame Every 5 Seconds)
                                    │
                                    ▼
                      [ GPS Sensor & 4G/5G Telematics ]
                                    │
                       (Attaches Lat/Lng & Vehicle ID)
                                    │
                                    ▼
                    [ FastAPI High-Throughput Fleet API ]
                        (POST /api/v1/predict-batch)
                                    │
                                    ▼
                      [ RoadVision Core AI Pipeline ]
                      (YOLOv11 Detector + MiDaS Depth)
                                    │
                                    ▼
                   [ Priority & Severity Scoring Engine ]
                                    │
                                    ▼
                [ PostGIS 10m Spatial Buffer Deduplication ]
                (Merges overlapping sightings within 10m)
                                    │
                                    ▼
                     [ PostgreSQL + PostGIS Storage ]
                                    │
                                    ▼
              [ Flutter Mobile Application (Admin Dashboard) ]
```

---

## 🧠 2. End-to-End AI Inspection Pipeline Execution Sequence

```
                              [ Input Image ]
                                     │
                                     ▼
                        [ OpenCV Image Preprocessing ]
                    (CLAHE Contrast + Bilateral Noise Filter)
                                     │
                                     ▼
                       [ YOLOv11 Multi-Damage Detector ]
                                     │
                                     ▼
                         [ Damage Classification ]
               (Pothole, Longitudinal, Transverse, Alligator)
                                     │
                                     ▼
                      [ MiDaS Monocular Depth Estimator ]
                     (Dense 3D Relative Depth Gradient)
                                     │
                                     ▼
                [ Physical 3D Metric Calculator ]
            ┌────────────────────────┼────────────────────────┐
            ▼                        ▼                        ▼
     Width Estimation        Length Estimation         Area Estimation
            │                        │                        │
            └────────────────────────┼────────────────────────┘
                                     │
                                     ▼
                             Depth Estimation
                                     │
                                     ▼
                        [ Severity & Priority Engine ]
                    (Priority Score 0-100 & Hazard Rating)
                                     │
                                     ▼
                      [ Road Health Score Evaluator ]
                    (Overall Health % & Condition Rating)
                                     │
                                     ▼
                   [ PostGIS Spatial Duplicate Detection ]
                    (ST_DWithin 10-Meter Buffer Merge)
                                     │
                                     ▼
                      [ PostgreSQL + PostGIS Storage ]
                                     │
                                     ▼
                   [ Flutter Mobile Response Payload ]
```

---

## 📊 3. Output AI Inspection JSON Schema

```json
{
  "damage_type": "Pothole",
  "confidence": 0.94,
  "severity": "Critical",
  "priority_score": 91,
  "estimated_width_m": 0.85,
  "estimated_length_m": 0.96,
  "estimated_area_m2": 0.81,
  "estimated_depth_cm": 9.2,
  "road_occupancy": 8.4,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "road_name": "Market Street",
  "city": "San Francisco",
  "timestamp": "2026-08-03T18:46:48Z",
  "source": "Citizen",
  "road_health_score": 22.0,
  "road_condition": "Critical"
}
```

---

## 🔄 4. 8-Stage Municipal Repair Lifecycle

```
1. Reported ➔ 2. AI Detection ➔ 3. Pending Verification ➔ 4. Verified
➔ 5. Assigned ➔ 6. Repair In Progress ➔ 7. Completed ➔ 8. Closed
```

---

## ⚡ Quickstart Guide

### 1. Launch FastAPI Backend Service
```bash
python backend/main.py
```
Open Swagger API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Launch Flutter Mobile Application
```bash
cd flutter_app
flutter pub get
flutter run
```

### 3. Run AI Pipeline Test
```bash
python test_inference.py
```

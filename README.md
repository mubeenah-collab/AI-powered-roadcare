# RoadVision: AI-Powered Intelligent Road Damage Detection & Monitoring System

RoadVision is an enterprise-grade AI, Computer Vision, and Smart City MLOps platform designed to automate urban road surface damage inspection. Built as a **Flutter Mobile Application (`flutter_app/`)** backed by a **FastAPI Backend (`backend/`)**, **YOLOv11 + MiDaS AI Engine (`ai/`)**, and **PostGIS 10m Spatial Buffer Deduplication (`database/`)**.

---

## 📍 Location Enhancement: Human-Readable Address Architecture

RoadVision separates **Internal Spatial Coordinates** from **User-Facing Display Addresses**:

- **Internal Coordinates**: `latitude`, `longitude`, `geom (GEOMETRY(Point, 4326))` stored for PostGIS 10m spatial buffer joins (`ST_DWithin`), GIS mapping, heatmaps, and duplicate detection.
- **Display Address**: Reverse-geocoded via OpenStreetMap Nominatim / Geopy into structured fields (`road_name`, `area`, `city`, `district`, `state`, `country`, `postal_code`).
- **User Interface Guarantee**: Raw GPS numbers are hidden from citizens and municipal administrators. All mobile cards and map popups display clean, formatted addresses (e.g. *"Anna Salai, Teynampet, Chennai, Tamil Nadu"*).

---

## 🏛 Project Architecture & Folder Structure

```
RoadVision/
├── flutter_app/                # Flutter Mobile Application (Human-Readable UI)
│   ├── lib/
│   │   ├── config/             # Theme & color palette
│   │   ├── services/           # FastAPI HTTP client service
│   │   ├── screens/
│   │   │   ├── auth/           # Login & Registration
│   │   │   ├── citizen/        # Human-readable address report cards & history
│   │   │   └── admin/          # Overview, GIS Map popups, Repair Lifecycle
│   │   └── main.dart
│   └── pubspec.yaml
├── backend/                    # Production FastAPI Backend Service
│   ├── api/                    # REST routers & Pydantic schemas (LocationSchema)
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
│   └── schema.sql              # PostGIS DDL schema with address columns
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

## 📊 Standardized API Response JSON Payload

```json
{
  "damage_type": "Pothole",
  "confidence": 0.964,
  "severity": "High",
  "priority_score": 89,
  "estimated_width_m": 0.82,
  "estimated_length_m": 1.05,
  "estimated_area_m2": 0.86,
  "estimated_depth_cm": 8.7,
  "road_occupancy": 8.4,
  "location": {
    "road_name": "Anna Salai",
    "area": "Teynampet",
    "city": "Chennai",
    "district": "Chennai",
    "state": "Tamil Nadu",
    "country": "India",
    "postal_code": "600018",
    "formatted_address": "Anna Salai, Teynampet, Chennai, Tamil Nadu"
  },
  "coordinates": {
    "latitude": 12.926543,
    "longitude": 80.143287
  },
  "complaint_id": "RV-2026-001245",
  "status": "Pending Verification",
  "timestamp": "2026-08-03T18:46:48Z",
  "source": "Citizen",
  "road_health_score": 24.5,
  "road_condition": "Poor"
}
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

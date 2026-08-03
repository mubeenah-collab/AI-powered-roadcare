# RoadVision: AI-Powered Intelligent Road Damage Detection & Monitoring System

RoadVision is an enterprise-grade AI, Computer Vision, and Smart City MLOps platform designed to automate urban road surface damage inspection. Built as a **Flutter Mobile Application (`flutter_app/`)** backed by a **FastAPI Backend (`backend/`)**, **YOLOv11 + MiDaS AI Engine (`ai/`)**, and **PostGIS 10m Spatial Buffer Deduplication (`database/`)**.

---

## 🏛 System Architecture & Component Layout

```
RoadVision/
├── flutter_app/                # Flutter Mobile Application (Citizen + Admin Roles)
│   ├── lib/
│   │   ├── config/             # Theme & color palette
│   │   ├── services/           # FastAPI HTTP client service
│   │   ├── screens/
│   │   │   ├── auth/           # Login & Registration
│   │   │   ├── citizen/        # Report, Weather, Timeline, Before/After View
│   │   │   └── admin/          # Analytics, Fleet Cards, GIS Map, Lifecycle
│   │   └── main.dart
│   └── pubspec.yaml
├── backend/                    # Production FastAPI Backend Service
│   ├── api/                    # REST routers & Pydantic schemas (Weather & Fleet)
│   ├── config/                 # Environment settings
│   └── main.py                 # FastAPI application launcher
├── ai/                         # Deep Learning & Computer Vision Engine
│   ├── depth_estimator.py      # MiDaS Monocular Depth & 3D Metric Calculator
│   ├── geocoding.py            # Reverse Geocoding via Nominatim (Indian Roads)
│   ├── image_processing.py     # OpenCV CLAHE & Bilateral noise filter
│   ├── model_loader.py         # YOLO detector singleton
│   ├── pipeline.py             # Integrated Core AI Pipeline
│   ├── road_health.py          # Road Health Score (0-100%) & Condition Evaluator
│   ├── severity_engine.py      # Priority Score Matrix (0-100)
│   └── weather_service.py      # Live Weather Service & Rain Priority Boost
├── database/                   # PostGIS Spatial Database & ORM
│   ├── db.py                   # Async 10m spatial buffer deduplication (`ST_DWithin`)
│   └── schema.sql              # PostGIS DDL schema with Weather & Fleet columns
├── docker/                     # Container Deployment
│   ├── Dockerfile.api
│   └── docker-compose.yml
├── docs/                       # Project Documentation & System Diagrams
│   ├── AI_PIPELINE_DIAGRAM.md
│   ├── DEFENSE_GUIDE.md
│   ├── GOVERNMENT_FLEET_WORKFLOW.md
│   ├── REPAIR_LIFECYCLE.md
│   ├── SEQUENCE_DIAGRAM.md
│   └── SRS.md
├── .github/                    # CI/CD Workflows
│   └── workflows/ci.yml
├── requirements.txt            # Python dependencies
└── test_inference.py          # Integration test script
```

---

## 🇮🇳 1. Indian Location Support

RoadVision displays realistic Indian addresses across all mobile views, API responses, and reports:
- **Anna Salai, Teynampet, Chennai, Tamil Nadu**
- **GST Road, Chromepet, Chennai, Tamil Nadu**
- **OMR Road, Sholinganallur, Chennai, Tamil Nadu**
- **Mount Road, Chennai**
- **Velachery Main Road, Chennai**
- **Bengaluru Outer Ring Road**
- **MG Road, Bengaluru**
- **Marine Drive, Mumbai**

Raw GPS coordinates (`latitude`, `longitude`) are preserved internally for PostGIS 10m spatial buffer joins (`ST_DWithin`) and heatmaps.

---

## ⛅ 2. Live Weather Information & Rain Priority Boost

Weather parameters are fetched automatically based on location:
- **Condition**: Rainy / Heavy Rain
- **Temperature**: 31°C
- **Humidity**: 82%
- **Visibility**: 4.0 km
- **Wind Speed**: 18 km/h
- **Rain Probability**: 85%
- **Weather Risk**: High (+15 Priority Score Boost applied during heavy rainfall to prioritize waterlogged defects)

---

## 📊 3. Standardized API Response JSON Payload

```json
{
  "complaint_id": "RV-2026-001245",
  "source": "Citizen",
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
  "weather": {
    "condition": "Rainy",
    "temperature_c": 31.0,
    "humidity_pct": 82,
    "visibility_km": 4.0,
    "wind_speed_kmh": 18,
    "rain_probability_pct": 85,
    "weather_risk": "High",
    "priority_boost": 15,
    "weather_risk_reason": "Continuous rainfall may worsen pothole damage."
  },
  "fleet_info": {
    "vehicle_id": "TN01-GOV-024",
    "vehicle_type": "Government Bus",
    "department": "Greater Chennai Corporation",
    "camera_id": "CAM-003",
    "driver_name": "R. Sundaram",
    "inspection_route": "Anna Salai Route",
    "shift": "Morning"
  },
  "timeline": [
    {
      "date_time": "2026-08-03 18:46:48",
      "stage": "Reported",
      "officer_name": "System Ingestion",
      "comments": "Road damage report received via Citizen."
    },
    {
      "date_time": "2026-08-03 18:46:48",
      "stage": "AI Detection Completed",
      "officer_name": "RoadVision AI Core Engine",
      "comments": "YOLOv11 classified Pothole with 96% confidence."
    }
  ],
  "before_image_url": "assets/images/before_repair_sample.jpg",
  "after_image_url": "assets/images/after_repair_sample.jpg",
  "status": "Pending Verification",
  "timestamp": "2026-08-03T18:46:48Z",
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

### 3. Run Pipeline Test Script
```bash
python test_inference.py
```

# RoadVision: AI-Powered Intelligent Road Damage Detection & Monitoring System

RoadVision is an enterprise-grade AI, Computer Vision, and Smart City MLOps platform designed to automate urban road surface damage inspection. Built as a **Unified Flutter Mobile Application (Citizen + Admin Dashboards)** backed by a **FastAPI Inference Service** and **PostGIS 10m Spatial Buffer Deduplication**.

---

## 📱 Mobile-First System Architecture

```
                                  +------------------------------------+
                                  |   FLUTTER MOBILE APP (Citizen Role)|
                                  +-----------------+------------------+
                                                    | (Camera Capture + GPS)
                                                    v
+------------------------------------+    +------------------------------------+
|  GOVT FLEET CONTINUOUS MONITORING  |--->|    FastAPI Ingestion Gateway       |
| (Buses, Garbage Trucks, Municipal) |    +-----------------+------------------+
+------------------------------------+                      |
  (Auto 4G/5G Stream + GPS Coordinates)                     v
                                          +------------------------------------+
                                          |     RoadVision AI Pipeline Engine  |
                                          | 1. OpenCV Preprocessing & CLAHE    |
                                          | 2. YOLOv11 Multi-Damage Detector   |
                                          | 3. MiDaS Monocular 3D Depth Engine |
                                          | 4. Priority & Severity Calculator  |
                                          +-----------------+------------------+
                                                            |
                                                            v
                                          +------------------------------------+
                                          |  PostGIS Spatial Deduplication DB  |
                                          |  (10m ST_DWithin Buffer Merge)     |
                                          +-----------------+------------------+
                                                            |
                                                            v
                                          +------------------------------------+
                                          |  FLUTTER MOBILE APP (Admin Role)   |
                                          +------------------------------------+
```

---

## 📂 Project Folder Structure

```
RoadVision-AI/
├── config/                     # System settings, model paths & severity weights
│   └── settings.py
├── dataset/                    # RDD2022 dataset preparation & YOLO YAML configs
│   ├── dataset_prep.py        # VOC XML to YOLO TXT converter & dataset splitter
│   └── rdd2022.yaml           # Ultralytics dataset configuration
├── database/                   # PostGIS spatial DDL schema & ORM queries
│   ├── schema.sql              # PostgreSQL + PostGIS DDL script
│   └── db.py                   # Async spatial queries & 10m deduplication logic
├── utils/                      # Core Computer Vision, Math & Geocoding modules
│   ├── image_processing.py     # OpenCV CLAHE, Bilateral filtering & Draw overlay
│   ├── depth_estimator.py      # MiDaS Monocular Depth & 3D metric calculations
│   ├── severity_engine.py      # Priority Score Matrix (0-100) & Severity levels
│   └── geocoding.py            # Nominatim Reverse Geocoding & Address lookup
├── models/                     # Model weights manager
│   └── model_loader.py
├── training/                   # YOLO GPU Training & Evaluation Suite
│   ├── train.py                # Hyperparameter tuning & Albumentations pipeline
│   └── evaluate.py             # mAP50, mAP50-95, Precision, Recall evaluator
├── inference/                  # Production Core Pipeline
│   └── pipeline.py             # Integrated Detector + Depth Estimator
├── api/                        # FastAPI REST Web Service
│   ├── main.py                 # FastAPI Application entry point
│   ├── schemas.py              # Pydantic JSON request & response schemas
│   └── router.py               # REST API endpoints (/auth, /citizen, /admin, /predict)
├── mobile/                     # Flutter Mobile Application (Citizen + Admin Roles)
│   ├── lib/
│   │   ├── config/
│   │   │   └── theme.dart      # Dark mode color palette
│   │   ├── services/
│   │   │   └── api_service.dart# HTTP API client for FastAPI backend
│   │   ├── screens/
│   │   │   ├── auth/          # Login & Registration screens
│   │   │   ├── citizen/       # Citizen Dashboard (Camera, GPS, Complaint Tracking)
│   │   │   └── admin/         # Admin Dashboard (Verification, Assign Team, GIS Map)
│   │   └── main.dart          # Main Flutter application launcher
│   └── pubspec.yaml            # Flutter packages & dependencies
├── docker/                     # Production Deployment Containers
│   ├── Dockerfile.api          # FastAPI container definition
│   └── docker-compose.yml      # Multi-container orchestration (API + PostGIS + Redis)
├── test_inference.py          # Standalone execution test script
├── requirements.txt            # Python dependencies
└── README.md                   # Project Documentation & Defense Manual
```

---

## ⚡ Quickstart Guide

### 1. Launch FastAPI Backend Service
```bash
python api/main.py
```
Open interactive Swagger API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Launch Flutter Mobile Application
```bash
cd mobile
flutter pub get
flutter run
```

---

## 🎓 Defense Guide for Engineering Project Reviews

1. **Flutter Single App Architecture**: Role-based access directs Citizens to the damage reporting portal and Administrators to the municipal verification dashboard within a single cross-platform codebase.
2. **Dual-Channel Ingestion**: Explains how mobile citizen uploads and government vehicle continuous dashcam streaming automate city-wide road inspection.
3. **Monocular Depth Engine**: Demonstrates how MiDaS Monocular Depth estimation extracts 3D physical width, length, area, depth ($cm$), and road occupancy $\%$ from standard mobile images.

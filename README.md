# RoadVision: AI-Powered Intelligent Road Damage Detection & Monitoring System

RoadVision is an enterprise-grade AI, Computer Vision, and Smart City MLOps platform designed to automate urban road surface damage inspection. By integrating **Citizen Reporting** and **Continuous Government Fleet Vehicle Monitoring**, RoadVision replaces manual, slow, and expensive surveys with real-time AI damage detection, monocular depth estimation, spatial deduplication via PostGIS, multi-factor priority scoring, and GIS-mapped maintenance dispatching.

---

## 🏛 System Architecture & Dual-Source Ingestion

```
                                  +------------------------------------+
                                  |    CITIZEN REPORTING (Mobile App)  |
                                  +-----------------+------------------+
                                                    | (Manual Upload + GPS)
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
                                          | React + Leaflet GIS Admin Dashboard|
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
│   └── router.py               # API Endpoints (/predict, /predict-batch, /complaints)
├── frontend/                   # React + Tailwind + Leaflet GIS Dashboard
│   ├── src/
│   │   ├── components/
│   │   │   └── MapView.jsx     # Interactive Leaflet map with severity markers
│   │   ├── App.jsx             # Main Dashboard interface
│   │   └── package.json
├── docker/                     # Production Deployment Containers
│   ├── Dockerfile.api          # FastAPI container definition
│   └── docker-compose.yml      # Multi-container orchestration (API + PostGIS + Redis)
├── test_inference.py          # Standalone execution test script
├── requirements.txt            # Python dependencies
└── README.md                   # Project Documentation & Defense Manual
```

---

## 🔬 AI Engine Details & Model Justifications

### 1. YOLOv11 / YOLOv8 Object Detector
- **Why Chosen**: YOLO (You Only Look Once) is an anchor-free single-stage object detector providing ultra-fast inference suitable for both high-throughput server APIs and edge deployment on municipal vehicles.
- **Classes Configured**:
  1. `Longitudinal Crack` (RDD `D00`)
  2. `Transverse Crack` (RDD `D10`)
  3. `Alligator Crack` (RDD `D20`)
  4. `Pothole` (RDD `D40`)
  5. `Surface Wear` (RDD `D44`)
  6. `Road Edge Failure` (RDD `D50`)

### 2. OpenCV Image Preprocessing
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: Enhances local contrast across dark asphalt regions without over-amplifying noise, crucial for detecting fine cracks in shadowed or direct sunlight road conditions.
- **Bilateral Filtering**: Smooths high-frequency road grain textures while preserving sharp defect edges.

### 3. MiDaS Monocular Depth Estimation
- **Why Chosen**: Monocular depth models (MiDaS v3.0 DPT) estimate dense relative depth maps from a single 2D camera image without requiring expensive LiDAR sensors.
- **3D Metric Derivations**:
  - **Width & Length ($m$)**: Calculated via pinhole camera perspective geometry.
  - **Estimated Depth ($cm$)**: Computed from the relative depth map gradient delta between the surrounding road plane and the defect depression center.
  - **Road Occupancy %**: Percentage of Visible Road Plane area occupied by the defect bounding box.

---

## 🧮 Priority Scoring Formula (0 – 100)

RoadVision uses a multi-factor priority scoring algorithm:

$$\text{Priority Score} = \min\left(100, \left(S_{\text{Type}} + S_{\text{Area}} + S_{\text{Depth}} + S_{\text{Verification}}\right) \times \text{Confidence}\right)$$

Where:
- $S_{\text{Type}}$: Damage class risk weight (Potholes = 25 pts, Alligator Cracks = 21.25 pts, Longitudinal Cracks = 12.5 pts).
- $S_{\text{Area}}$: Road occupancy score scaled to max 25 pts for $>15\%$ occupancy.
- $S_{\text{Depth}}$: Depth severity score scaled to max 25 pts for depth $>10\text{ cm}$.
- $S_{\text{Verification}}$: Logarithmic boost for spatial duplicate verifications across fleet passes ($\log(N+1) \times 4$).

### Severity Categories:
- **Low**: Priority $< 35$
- **Medium**: Priority $35 - 59$
- **High**: Priority $60 - 79$
- **Critical**: Priority $\ge 80$ (or Pothole Depth $\ge 8\text{ cm}$)

---

## 🌍 PostGIS Spatial Deduplication Logic

When thousands of government vehicles and citizens submit reports, the same pothole will be photographed multiple times. PostGIS prevents duplicate complaints using spatial buffer joins:

```sql
SELECT id, priority_score, verification_count 
FROM damage_reports 
WHERE ST_DWithin(
    geom::geography, 
    ST_SetSRID(ST_MakePoint(new_longitude, new_latitude), 4326)::geography, 
    10.0 -- 10 Meters Buffer Radius
)
AND damage_type = new_damage_type
AND status IN ('pending', 'assigned', 'in_progress')
LIMIT 1;
```

**If a spatial match is found within 10 meters**:
1. Merges the new capture into the primary complaint record.
2. Increments `verification_count`.
3. Dynamically boosts the `priority_score` and updates severity.

---

## ⚡ Quickstart Guide

### 1. Installation & Environment Setup
```bash
# Clone repository and enter project root
cd "c:/AI Road vision"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install required dependencies
pip install -r requirements.txt
```

### 2. Run Integration Test Script
Verify detector, depth estimator, OpenCV pipeline, and JSON output generation:
```bash
python test_inference.py
```
Output:
- Printed structured JSON report.
- Generated annotated image saved to `output_annotated.jpg`.

### 3. Launch FastAPI Server
```bash
python api/main.py
```
Access Interactive Swagger API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Train Model on Custom RDD2022 Dataset
```bash
# Prepare RDD2022 dataset from raw folder
python dataset/dataset_prep.py --input path/to/raw_rdd2022 --output dataset

# Train YOLOv11 / YOLOv8 model on GPU
python training/train.py --epochs 50 --batch 16 --imgsz 640
```

### 5. Launch Full Stack with Docker Compose (API + PostGIS + Redis)
```bash
cd docker
docker-compose up --build
```

---

## 🎓 Project Review & Defense Q&A Guide for Engineering Students

### Key Presentation Talking Points:
1. **System Innovation**: Explain why dual-source monitoring (Citizen + Govt Fleet) solves the reactive maintenance problem.
2. **Evaluation Metrics**:
   - **Precision (P)**: Proportion of true damage detections out of all predicted detections.
   - **Recall (R)**: Proportion of actual road damages correctly detected by the model.
   - **mAP@50**: Mean Average Precision at Intersection over Union (IoU) threshold of 0.50.
   - **mAP@50-95**: Mean Average Precision computed across IoU thresholds from 0.50 to 0.95 (measures localization precision).
3. **Monocular Depth vs LiDAR**:
   - LiDAR hardware costs upwards of \$5,000 per vehicle. Monocular depth estimation via MiDaS enables standard \$50 dashcams on garbage trucks and buses to estimate physical depth.
4. **Spatial Deduplication**:
   - Explain how PostGIS `ST_DWithin` spatial indexing prevents complaint duplication and prioritizes frequently reported defects.

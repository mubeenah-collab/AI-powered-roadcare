<div align="center">

# 🛣️ RoadVision

### **AI-Powered Intelligent Road Damage Detection & Monitoring System**

*A mobile-first Smart City AI solution for automated road defect inspection, crowdsourced citizen reporting, continuous municipal fleet surveillance, and 3D depth spatial analytics.*

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.3-336791?style=for-the-badge&logo=postgis&logoColor=white)](https://postgis.net)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

</div>

---

## 📌 Project Overview

**RoadVision** is an intelligent road damage detection and monitoring platform designed to transform municipal road maintenance from a manual, reactive process into an automated, data-driven Smart City solution. 

The system leverages dual independent data collection channels:
1. **Citizen Crowdsourcing**: Citizens capture pavement damage using their mobile camera. GPS coordinates are automatically recorded, and human-readable Indian addresses are generated while AI instantly diagnoses damage type, severity, and metric dimensions.
2. **Continuous Government Fleet Surveillance**: Dashboard cameras installed on municipal vehicles (public buses, garbage collection trucks, municipal inspection vans) continuously record road conditions while driving daily routes, transmitting telematics frames over 4G/5G networks.

By combining real-time computer vision, 3D monocular depth estimation, weather risk analysis, and spatial GIS deduplication, RoadVision enables public works departments to prioritize repairs, optimize municipal budgets, and eliminate manual road inspection overhead.

---

## ⚠️ Problem Statement

Conventional municipal road inspections suffer from critical operational challenges:
- **Manual & Labor-Intensive**: Visual surveys require human inspectors to drive thousands of kilometers, making comprehensive coverage impossible.
- **Reactive Repair Cycles**: By the time potholes or structural cracks are identified, water ingress and traffic loads have expanded damage, leading to severe vehicle accidents and inflated repair costs.
- **Inconsistent Citizen Reporting**: Complaints submitted through phone calls or forms lack precise spatial coordinates, depth metrics, or standardized severity ratings.
- **Duplicate Resource Allocation**: Multiple citizens often report the same pothole, resulting in redundant municipal site visits and fragmented tracking.

---

## 🎯 Objectives

- **Automate Pavement Inspection**: Eliminate manual visual surveys using real-time Computer Vision.
- **Enable Dual-Channel Ingestion**: Seamlessly combine crowdsourced mobile reports with continuous municipal fleet surveillance telematics.
- **3D Metric Estimation**: Compute physical width ($m$), length ($m$), area ($m^2$), depth ($cm$), and road occupancy percentage using monocular depth estimation.
- **Weather-Aware Risk Scoring**: Dynamically boost repair priority when heavy monsoon rainfall is detected to prevent rapid pavement erosion.
- **Spatial Deduplication**: Utilize PostGIS spatial indexing to deduplicate defects within a 10-meter radius automatically.
- **End-to-End Lifecycle Tracking**: Provide an 8-stage repair workflow with Before & After photo verification.

---

## ✨ Key Features

### 📱 Citizen Mobile Application
- **Mobile-First Experience**: Flutter cross-platform mobile application supporting Citizen and Administrator role-based authentication.
- **Camera & Gallery Upload**: Instant image capture with camera focus optimization and gallery pick support.
- **Automated GPS & Indian Address Resolution**: Automatically captures latitude and longitude while displaying human-readable Indian addresses (*"Anna Salai, Teynampet, Chennai, Tamil Nadu"*).
- **AI Damage Diagnosis**: Instant visual feedback featuring an **AI Confidence Bar** (`██████████░░ 96.4%`) with dynamic color indicators.
- **Live Weather Hazard Banner**: Displays local ambient temperature, humidity, visibility, and rain risk level.
- **Visual Repair Timeline**: Tracks complaint progress step-by-step from `Reported` to `Closed`.
- **Before & After Repair Comparison**: Side-by-side visual verification of repaired road surfaces.

### 🚌 Government Fleet Surveillance Module
- **Continuous Dashcam Streaming**: Ingests automated frame streams captured by municipal buses and garbage trucks.
- **Fleet Telematics Metadata**: Attaches Vehicle ID (`TN01-GOV-024`), Vehicle Type, Department, Camera ID, Driver Name, Inspection Route, and Shift.
- **High-Throughput Batch Processing**: Asynchronous ingestion endpoint designed for high-density municipal fleet streams.

### 📊 Administrator Module
- **Executive Analytics Dashboard**: Overview cards tracking total scanned kilometers, average AI accuracy, average repair SLA, and damage type distributions.
- **Interactive GIS Map & Heatmaps**: Visualizes defect markers and density heatmaps categorized by risk levels (Low, Medium, High, Critical).
- **Workorder Lifecycle Dispatch**: Assign contractors, update repair statuses, and manage municipal paving crews.
- **Before/After Verification**: Inspector verification interface for validating completed contractor repairs.

### 🧠 Core AI Pipeline
- **YOLOv11 Multi-Class Detection**: Real-time classification of Potholes, Longitudinal Cracks, Transverse Cracks, Alligator Cracks, Surface Damage, and Road Edge Failures.
- **MiDaS 3D Monocular Depth Estimation**: Computes relative 3D depth maps to estimate physical width, length, surface area, and depth in centimeters.
- **Road Health Score Engine (0–100%)**: Evaluates overall pavement segment health (**Excellent**, **Good**, **Fair**, **Poor**, **Critical**).
- **Severity & Priority Score Matrix**: Evaluates multi-factor priority scores combining defect type, depth, confidence, and weather rain risk.

---

## 🛠️ Technology Stack

| Domain | Technology | Description |
| :--- | :--- | :--- |
| **Mobile Frontend** | ![Flutter](https://img.shields.io/badge/-Flutter-02569B?logo=flutter&logoColor=white) | Unified Cross-Platform Mobile Application (Citizen & Admin Roles) |
| **Backend Web API** | ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white) | High-Performance Asynchronous Python Web API Framework |
| **AI Framework** | ![PyTorch](https://img.shields.io/badge/-PyTorch-EE4C2C?logo=pytorch&logoColor=white) | Deep Learning Framework for Computer Vision Models |
| **Object Detection** | ![YOLOv11](https://img.shields.io/badge/-YOLOv11-00FFFF?logo=ultralytics&logoColor=black) | Real-time Pavement Damage Multi-Class Detection Engine |
| **3D Depth Engine** | ![MiDaS](https://img.shields.io/badge/-MiDaS--v3.0-FF6F00?logo=intel&logoColor=white) | Dense Monocular Depth Estimation Model |
| **Computer Vision** | ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?logo=opencv&logoColor=white) | CLAHE Contrast Enhancement and Bilateral Noise Filtering |
| **Relational Database** | ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL--15-4169E1?logo=postgresql&logoColor=white) | Enterprise Database Engine |
| **Spatial Extension** | ![PostGIS](https://img.shields.io/badge/-PostGIS--3.3-336791?logo=postgis&logoColor=white) | Spatial Data Storage, GIST Indexing, and 10m Buffer Deduplication |
| **Database ORM** | ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy--2.0-D71F00?logo=sqlalchemy&logoColor=white) | Asynchronous Database Persistence Layer (`asyncpg`) |
| **GIS Mapping** | ![OpenStreetMap](https://img.shields.io/badge/-OpenStreetMap-7EBC6F?logo=openstreetmap&logoColor=white) | Reverse Geocoding and Map Tile Rendering |
| **Containerization** | ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white) | Multi-Container Orchestration (API + PostGIS + Redis) |
| **CI/CD Pipeline** | ![GitHub Actions](https://img.shields.io/badge/-GitHub_Actions-2088FF?logo=githubactions&logoColor=white) | Automated Integration Testing and Flutter Build Workflow |

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Mobile Application Layer
        A[📱 Citizen Mobile Role]
        B[🚌 Government Fleet Dashcam Stream]
        C[👨‍💼 Municipal Administrator Role]
    end

    subgraph API Gateway & Business Services
        D[⚡ FastAPI REST API Gateway]
        E[⛅ Live Weather Risk Service]
        F[🗺️ Indian Reverse Geocode Engine]
    end

    subgraph AI Computer Vision Engine
        G[📷 OpenCV Preprocessor CLAHE]
        H[🎯 YOLOv11 Damage Detector]
        I[📐 MiDaS 3D Depth Estimator]
        J[⚖️ Severity & Road Health Engine]
    end

    subgraph Spatial Data Layer
        K[(🗄️ PostgreSQL 15 + PostGIS 3.3)]
    end

    A -->|1. Upload Image & GPS| D
    B -->|2. Batch Telematics Stream| D
    D --> E
    D --> F
    D --> G
    G --> H
    H --> I
    I --> J
    J -->|3. Async ORM Store| K
    K -->|4. PostGIS ST_DWithin Deduplication| D
    D -->|5. Analytics & GIS Heatmaps| C
```

---

## 📱 Application Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Citizen/Fleet as Citizen / Fleet Dashcam
    participant App as Flutter Mobile App
    participant API as FastAPI Backend
    participant AI as AI Engine (YOLO + MiDaS)
    participant GIS as PostGIS Spatial DB
    actor Admin as Municipal Engineer

    Citizen/Fleet->>App: Capture Photo & Auto-GPS
    App->>API: POST /predict (Multipart Image + GPS)
    API->>AI: Image Preprocessing & Inference
    AI-->>API: Defect Type, Confidence, 3D Metrics
    API->>GIS: Query ST_DWithin (10m Radius Buffer)
    alt Duplicate Found within 10m
        GIS-->>API: Increment Verification Count
    else New Defect
        GIS-->>API: Persist New Spatial Record
    end
    API-->>App: Return Address, Weather, Score Payload
    Admin->>App: View GIS Map & Assign Contractor
```

---

## 🧠 AI Pipeline Workflow

```mermaid
flowchart LR
    A[Raw Road Image] --> B[OpenCV CLAHE Contrast Enhancement]
    B --> C[Bilateral Edge-Preserving Noise Filter]
    C --> D[YOLOv11 Defect Classification]
    D --> E[MiDaS Monocular 3D Depth Estimation]
    E --> F[Metric Calculator: Width, Length, Area, Depth]
    F --> G[Weather Rain Risk Assessment]
    G --> H[Road Health Score Evaluator 0-100%]
    H --> I[PostgreSQL + PostGIS Persistence]
```

---

## 🗄️ Database Spatial Architecture

```mermaid
erDiagram
    USERS {
        string id PK
        string email UK
        string full_name
        string role
        timestamp created_at
    }

    DAMAGE_REPORTS {
        string id PK
        string damage_type
        float confidence
        string severity
        int priority_score
        float estimated_depth_cm
        float road_health_score
        float latitude
        float longitude
        geometry geom
        string formatted_address
        string status
        jsonb timeline
    }

    FLEET_VEHICLES {
        string vehicle_id PK
        string vehicle_type
        string department
        string camera_id
        string inspection_route
    }

    NOTIFICATIONS {
        string id PK
        string user_id FK
        string title
        text message
        boolean is_read
    }

    USERS ||--o{ NOTIFICATIONS : receives
    FLEET_VEHICLES ||--o{ DAMAGE_REPORTS : inspects
```

---

## 📁 Folder Structure

```
RoadVision/
├── .github/ workflows/    # GitHub Actions automated test & build scripts
├── ai/                    # Deep learning models, OpenCV CLAHE, MiDaS depth, & weather engine
├── backend/               # FastAPI application launcher, API routes, and Pydantic schemas
├── database/              # PostgreSQL schema DDL, async SQLAlchemy connection, and ORM models
├── dataset/               # RDD2022 dataset preparation tools and conversion scripts
├── docker/                # Production Dockerfile and multi-container docker-compose stack
├── docs/                  # System diagrams, SRS documentation, and evaluation guides
├── flutter_app/           # Unified Flutter mobile codebase for Citizen & Admin interfaces
├── .env.example           # Configuration template for system environment variables
├── .gitignore             # Exclusion rules for temporary cache and credential files
├── LICENSE                # MIT Open-Source License
├── README.md              # Project documentation manual
├── requirements.txt       # Python dependency specifications
└── test_inference.py      # End-to-end integration pipeline execution test script
```

---

## 📸 Screenshots & UI Previews

<div align="center">

### Mobile Application Views

| Citizen Inspection Portal | Live Weather Hazard Impact | Visual Repair Timeline |
| :---: | :---: | :---: |
| ![Citizen Inspection](https://raw.githubusercontent.com/mubeenah-collab/AI-powered-roadcare/main/docs/screenshots/citizen_dashboard.png) | ![Weather Card](https://raw.githubusercontent.com/mubeenah-collab/AI-powered-roadcare/main/docs/screenshots/weather_card.png) | ![Complaint Timeline](https://raw.githubusercontent.com/mubeenah-collab/AI-powered-roadcare/main/docs/screenshots/timeline.png) |

<br/>

### Administrator Monitoring & Analytics Views

| Executive Dashboard KPIs | OpenStreetMap GIS Heatmap | Before & After Repair Audit |
| :---: | :---: | :---: |
| ![Analytics Dashboard](https://raw.githubusercontent.com/mubeenah-collab/AI-powered-roadcare/main/docs/screenshots/admin_dashboard.png) | ![GIS Map View](https://raw.githubusercontent.com/mubeenah-collab/AI-powered-roadcare/main/docs/screenshots/gis_map.png) | ![Before After Repair](https://raw.githubusercontent.com/mubeenah-collab/AI-powered-roadcare/main/docs/screenshots/before_after.png) |

</div>

---

## ⚙️ Installation Guide

### Prerequisites
- **Python 3.10+**
- **Flutter SDK 3.x**
- **Docker Desktop** (for containerized deployment)
- **PostgreSQL 15 + PostGIS 3.3** (if running without Docker)

### 1. Clone Repository
```bash
git clone https://github.com/mubeenah-collab/AI-powered-roadcare.git
cd AI-powered-roadcare
```

### 2. Backend Setup
```bash
# Create Python virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Activate environment (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Flutter Application Setup
```bash
cd flutter_app
flutter pub get
```

---

## 🚀 Running the System

### Method A: Containerized Deployment (Recommended)
```bash
docker-compose -f docker/docker-compose.yml up --build
```
The FastAPI backend service will start at `http://localhost:8000`. Open Swagger docs at `http://localhost:8000/docs`.

### Method B: Manual Local Startup

#### 1. Start FastAPI Backend
```bash
python backend/main.py
```

#### 2. Start Flutter Mobile App
```bash
cd flutter_app
flutter run
```

#### 3. Run AI Inference Diagnostic Test
```bash
python test_inference.py
```

---

## 📡 API Endpoints Summary

Interactive Swagger OpenAPI documentation is served live at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/predict` | Single road damage inspection, AI diagnosis, and geocoding |
| `POST` | `/api/v1/predict-batch` | Government fleet high-throughput continuous frame ingestion |
| `GET` | `/api/v1/admin/complaints` | Retrieves active municipal complaints sorted by priority score |
| `PUT` | `/api/v1/admin/repair-complete/{id}` | Submits after-repair verification photo and marks repair complete |
| `GET` | `/api/v1/admin/dashboard` | Executive KPI analytics dashboard summary metrics |
| `GET` | `/health` | System health check endpoint |

---

## 🔮 Future Enhancements

- 🛸 **Autonomous Drone Inspection**: Extend pipeline to process high-altitude aerial survey streams.
- 🔮 **Predictive Degradation Modeling**: Implement time-series algorithms to forecast asphalt erosion.
- 📱 **Edge-AI Offline Inference**: Export YOLOv11 models to ONNX / TFLite for offline mobile inference.
- 🌐 **Multi-Language Support**: Localization support for regional Indian languages across dashboards.
- 🛰️ **IoT Telematics Sensors**: Integrate vehicle accelerometer sensors to detect physical impact bumps automatically.

---

## 👥 Contributors

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/mubeenah-collab/AI-powered-roadcare/issues).

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for real-time object detection architecture.
- [Intel ISL MiDaS](https://github.com/isl-org/MiDaS) for monocular depth estimation models.
- [FastAPI](https://fastapi.tiangolo.com/) for high-performance Python web services.
- [Flutter](https://flutter.dev/) for cross-platform mobile app development.
- [PostGIS](https://postgis.net/) for enterprise spatial database extensions.
- [OpenStreetMap](https://www.openstreetmap.org/) & Nominatim for global geocoding services.

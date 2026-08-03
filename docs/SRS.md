# Software Requirements Specification (SRS)
## RoadVision: Intelligent Road Damage Detection & Monitoring System

### 1. Introduction
RoadVision is an intelligent road surface monitoring system combining computer vision, monocular depth estimation, PostGIS spatial analytics, and dual-channel data ingestion (Citizen Mobile App + Continuous Government Fleet Monitoring).

### 2. Functional Requirements
- **FR-1**: Image Ingestion & Preprocessing (OpenCV CLAHE contrast enhancement & noise reduction).
- **FR-2**: Object Detection (YOLOv11/v8 classification of Potholes, Longitudinal Cracks, Transverse Cracks, Alligator Cracks, Surface Wear, and Road Edge Failures).
- **FR-3**: 3D Monocular Depth Estimation (MiDaS v3.0 depth estimation for physical width, length, area, depth in cm, and road occupancy %).
- **FR-4**: Severity & Priority Matrix (0–100 score assignment).
- **FR-5**: PostGIS Spatial Deduplication (Merging duplicate captures within a 10m buffer zone via `ST_DWithin`).
- **FR-6**: Role-Based REST APIs (Authentication, Citizen complaint upload/history, Admin repair dispatching, Fleet batch ingestion).
- **FR-7**: Interactive GIS Dashboard (Leaflet map rendering, severity filters, repair status management, and statistics analytics).

### 3. Non-Functional Requirements
- **NFR-1 (Performance)**: AI inference latency under 100ms per image on GPU.
- **NFR-2 (Scalability)**: Asynchronous FastAPI architecture supporting 10,000+ daily fleet vehicle image uploads.
- **NFR-3 (Reliability)**: In-Memory fallback database mechanism ensuring operational continuity during offline testing.
- **NFR-4 (Security)**: JWT authentication and password hashing (bcrypt).

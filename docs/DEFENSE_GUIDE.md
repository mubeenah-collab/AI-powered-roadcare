# RoadVision: Comprehensive Engineering Project Review & Defense Manual

RoadVision is an enterprise-grade AI, Computer Vision, and Smart City MLOps platform designed for automated pavement damage detection and municipal maintenance dispatching.

---

## 🏛 1. Core Problem & System Innovation
- **Traditional Problem**: Municipal pavement inspection relies on manual visual surveys, which are slow, reactive, dangerous for highway workers, and expensive.
- **RoadVision Innovation**:
  - **Dual Data Ingestion**: Combines **Citizen Mobile Reporting** and **Continuous Government Fleet Surveillance** (garbage trucks, public buses).
  - **Zero Human Intervention**: Fleet vehicles automatically capture dashboard camera frames every 5 seconds while driving their daily routes, attaching 4G/5G telematics GPS metadata.

---

## 📍 2. Indian Location Support & Privacy
- **Human-Readable Display**: Converts internal coordinates (`12.926543, 80.143287`) into realistic Indian locations (*"Anna Salai, Teynampet, Chennai, Tamil Nadu"*, *"GST Road, Chromepet, Chennai"*).
- **Internal PostGIS Storage**: Latitude and longitude remain stored internally in PostgreSQL + PostGIS (`GEOMETRY(Point, 4326)`) for sub-10m spatial buffer deduplication (`ST_DWithin`), heatmaps, and GIS mapping.

---

## ⛅ 3. Live Weather Hazard Assessment
- Fetches real-time weather metrics (`temperature`, `humidity`, `visibility`, `wind_speed`, `rain_probability`).
- If heavy rainfall is detected, the AI automatically applies a **+15 Point Priority Score Boost** to accelerate repair dispatch before monsoon rains expand pothole erosion.

---

## 🧠 4. AI & Computer Vision Stack
1. **OpenCV Preprocessing**:
   - **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: Enhances local contrast in shaded pavement regions.
   - **Bilateral Filtering**: Smooths surface asphalt grain while preserving defect edge sharpness.
2. **YOLOv11 Object Detector**:
   - Detects **Potholes**, **Longitudinal Cracks**, **Transverse Cracks**, **Alligator Cracks**, **Surface Damage**, and **Road Edge Failures**.
3. **MiDaS Monocular Depth Estimation**:
   - Infers 3D relative depth map gradients from 2D photos, computing physical defect **width ($m$)**, **length ($m$)**, **surface area ($m^2$)**, **depth ($cm$)**, and **road occupancy $\%$**.

---

## 📊 5. Priority Matrix & Road Health Score (0–100%)
- **Priority Score (0–100)**: Combines defect class risk, road occupancy $\%$, depth ($cm$), AI confidence, and weather rain risk boost.
- **Road Health Score (0–100%)**: Evaluates overall pavement health ($91\% = \text{Good}$, $22\% = \text{Critical}$) to help municipalities budget maintenance per road segment.

---

## 🔄 6. 8-Stage Municipal Repair Lifecycle
```
Reported ➔ AI Detection Completed ➔ Pending Verification ➔ Verified ➔ Assigned ➔ Repair In Progress ➔ Completed ➔ Closed
```
Includes **Before & After Repair Image Comparison** for auditability.

---

## 📱 7. Mobile-First Flutter Application (`flutter_app/`)
- Unified Flutter Mobile Application supporting **Citizen** and **Administrator** role-based authentication.
- Citizen Dashboard: Photo capture, auto location, AI diagnosis, confidence bar visualizer, live weather card, repair timeline.
- Admin Dashboard: Municipal overview stats, active complaints list, 8-stage lifecycle controls, analytics charts, FlutterMap GIS visualization.

---

## 🚀 8. Production Deployment & MLOps Stack
- **FastAPI**: Asynchronous Python backend framework.
- **PostgreSQL + PostGIS**: Enterprise spatial database with GIST spatial indexing.
- **Docker Compose**: Multi-container containerization (API + PostGIS + Redis).
- **GitHub Actions**: Automated CI/CD workflow testing backend integration and building Flutter APK artifacts.

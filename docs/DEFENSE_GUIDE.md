# Project Review & Presentation Defense Guide
## RoadVision: AI-Powered Intelligent Road Damage Detection System

### 1. Indian Location Support & Privacy
- **Why Hidden GPS**: Raw floating-point numbers (`12.926543, 80.143287`) are unintuitive for citizens and city officers. Geocoding converts coordinates into familiar Indian locations (*"Anna Salai, Teynampet, Chennai, Tamil Nadu"*).
- **Internal GIS Role**: Latitude and Longitude are preserved in PostGIS (`GEOMETRY(Point, 4326)`) for 10-meter spatial buffer deduplication (`ST_DWithin`), heatmaps, and spatial clustering.

### 2. Live Weather Risk Integration
- Continuous monsoon rainfall rapidly destabilizes cracked asphalt. Weather service evaluates rain probability ($\%$) and dynamically boosts priority scores by $+15\text{ pts}$ during severe downpours.

### 3. AI Confidence Visualization
- Color-coded indicator bar (`██████████░░ 96.4%`) provides visual certainty feedback to citizens and municipal inspectors:
  - **Green (90–100%)**: High AI Certainty
  - **Orange (70–89%)**: Moderate Certainty
  - **Red (<70%)**: Requires Manual Verification

### 4. Road Health Score (0–100%)
- Moves municipal budgeting from reactive pothole patching to overall pavement health monitoring ($91\% = \text{Good}$, $22\% = \text{Critical}$).

### 5. 8-Stage Repair Lifecycle Workflow
```
Reported ➔ AI Detection ➔ Pending Verification ➔ Verified ➔ Assigned ➔ Repair Started ➔ Completed ➔ Closed
```
Includes Before & After repair photo comparison for auditability.

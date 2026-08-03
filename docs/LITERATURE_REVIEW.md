# Literature Review: Automated Road Damage Detection & Spatial Monitoring

### 1. Traditional Road Inspection Limitations
Traditional pavement evaluation relies on manual visual inspection by human engineers or expensive laser profilometer vehicles. These methods suffer from high labor costs, dangerous highway exposure, low inspection frequency, and delayed maintenance responses.

### 2. Deep Learning for Pavement Defect Classification
Recent advances in single-stage convolutional object detectors (YOLOv5 to YOLOv11) demonstrate state-of-the-art performance on road damage datasets such as **RDD2022 (Road Damage Detection 2022)**. YOLO models achieve real-time frame rates ($>30$ FPS) while detecting complex crack morphologies.

### 3. Monocular Depth Estimation vs LiDAR
While LiDAR provides accurate 3D point clouds, hardware costs prohibit mounting LiDAR units across entire public transit fleets. Monocular depth estimation architectures (e.g., MiDaS, DPT) infer dense relative depth maps from standard 2D camera images, democratizing 3D metric extraction across standard dashcams.

### 4. Spatial Analytics & GIS Deduplication
Citizen-sourcing and continuous fleet monitoring introduce massive duplicate reporting of identical defects. Integrating PostGIS spatial buffer queries (`ST_DWithin`) resolves multi-perspective captures into unified spatial complaint clusters with boosted verification counts.

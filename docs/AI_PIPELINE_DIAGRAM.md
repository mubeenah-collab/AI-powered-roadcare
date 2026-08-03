# RoadVision End-to-End AI Inspection Pipeline

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

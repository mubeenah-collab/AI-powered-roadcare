# RoadVision System Sequence Diagram

```
[ Citizen / Fleet ]       [ Flutter App ]         [ FastAPI API ]         [ AI Core (YOLO+MiDaS) ]      [ PostGIS DB ]
        │                        │                        │                        │                        │
        │── Upload Road Image ──>│                        │                        │                        │
        │   + Auto GPS Sensor    │                        │                        │                        │
        │                        │── POST /predict ──────>│                        │                        │
        │                        │   (Multipart Form)     │                        │                        │
        │                        │                        │── Process Image ──────>│                        │
        │                        │                        │   + Reverse Geocode    │                        │
        │                        │                        │   + Weather API        │                        │
        │                        │                        │                        │── CLAHE & YOLOv11 ────>│
        │                        │                        │                        │   Multi-Class Defect   │
        │                        │                        │                        │── MiDaS Depth ────────>│
        │                        │                        │                        │   Width, Length, Depth │
        │                        │                        │                        │── Severity & Priority ─>│
        │                        │                        │                        │   + Weather Risk Boost │
        │                        │                        │                        │── Road Health Score ──>│
        │                        │                        │<─ Structured Payload ──│                        │
        │                        │                        │                                                 │
        │                        │                        │── Spatial Buffer Query (ST_DWithin 10m) ───────>│
        │                        │                        │<─ Merge / Create Record Result ─────────────────│
        │                        │                        │                                                 │
        │                        │<─ JSON Response ───────│                                                 │
        │<─ Display Inspection ──│   (Human Address,      │                                                 │
        │   Result & Priority    │   Weather & Health)    │                                                 │
```

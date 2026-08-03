# Government Fleet Continuous Road Monitoring Architecture

RoadVision transforms public transit and municipal utility fleets into automated road inspection agents.

## Operational Workflow

```
               [ Government Bus / Garbage Collection Truck ]
                                    │
                                    ▼
                         [ Front Dashboard Camera ]
                                    │
                       (Captures Frame Every 5 Seconds)
                                    │
                                    ▼
                      [ GPS Sensor & 4G/5G Telematics ]
                                    │
                       (Attaches Lat/Lng & Vehicle ID)
                                    │
                                    ▼
                    [ FastAPI High-Throughput Fleet API ]
                        (POST /api/v1/predict-batch)
                                    │
                                    ▼
                      [ RoadVision Core AI Pipeline ]
                      (YOLOv11 Detector + MiDaS Depth)
                                    │
                                    ▼
                   [ Priority & Severity Scoring Engine ]
                                    │
                                    ▼
                [ PostGIS 10m Spatial Buffer Deduplication ]
                (Merges overlapping sightings within 10m)
                                    │
                                    ▼
                     [ PostgreSQL + PostGIS Storage ]
                                    │
                                    ▼
              [ Flutter Mobile Application (Admin Dashboard) ]
```

### Key Innovations:
- **Zero Human Intervention**: Vehicles perform normal daily routes while continuously inspecting road networks.
- **4G/5G Edge Telematics**: Frame batches sent to server via lightweight HTTP POST multipart.
- **Verification Boost**: When multiple buses record the same pothole, PostGIS merges duplicates and boosts priority automatically.

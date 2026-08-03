# 8-Stage Municipal Road Repair Lifecycle

RoadVision manages the complete lifecycle of road defects from initial sighting to final verification.

```
1. Reported               (Citizen upload or Fleet dashcam frame captured)
     │
     ▼
2. AI Detection           (YOLOv11 & MiDaS estimate metrics and priority)
     │
     ▼
3. Pending Verification   (Logged in system awaiting municipal admin review)
     │
     ▼
4. Verified               (Admin verifies damage location and severity)
     │
     ▼
5. Assigned               (Assigned to contractor repair team with priority SLA)
     │
     ▼
6. Repair In Progress     (Maintenance team patching and resurfacing pavement)
     │
     ▼
7. Completed              (Patching complete and submitted by contractor)
     │
     ▼
8. Closed                 (Final inspection closed and archived in PostGIS)
```

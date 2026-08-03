# Use Case Specification & Diagram

```
                             +------------------------+
                             |    RODVISION SYSTEM    |
                             +------------------------+

     +---------------+                                      +------------------+
     |               | ---- (UC-1: Register / Login) -----> |                  |
     |    CITIZEN    | ---- (UC-2: Upload Road Photo) ----> |                  |
     |     USER      | ---- (UC-3: Auto Capture GPS) -----> |                  |
     |               | ---- (UC-4: Track Complaint) ------> |                  |
     +---------------+                                      |                  |
                                                            |   FASTAPI API    |
     +---------------+                                      |   & AI ENGINE    |
     |  GOVERNMENT   | ---- (UC-5: Auto Stream Cam) -----> |                  |
     | FLEET VEHICLE | ---- (UC-6: Submit GPS Frame) ----> |                  |
     +---------------+                                      |                  |
                                                            |                  |
     +---------------+                                      |                  |
     |     ADMIN     | ---- (UC-7: View GIS Map) ---------> |                  |
     |   AUTHORITY   | ---- (UC-8: Filter Severities) ----> |                  |
     |               | ---- (UC-9: Assign Repair Team) ---> |                  |
     |               | ---- (UC-10: View Fleet Analytics) -> |                  |
     +---------------+                                      +------------------+
```

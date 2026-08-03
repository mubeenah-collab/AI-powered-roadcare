import io
import cv2
import uuid
import numpy as np
from PIL import Image
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query
from backend.api.schemas import (
    DamagePredictionSchema,
    LifecycleStatusUpdateSchema,
    SystemAnalyticsSchema
)
from ai.pipeline import pipeline
from database.db import db_manager

router = APIRouter()

def read_image_bytes(file_bytes: bytes) -> np.ndarray:
    try:
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img_np = np.array(pil_img)
        return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

@router.post("/predict", response_model=DamagePredictionSchema)
@router.post("/citizen/upload", response_model=DamagePredictionSchema)
async def predict_road_damage(
    file: UploadFile = File(...),
    latitude: float = Form(12.926543),
    longitude: float = Form(80.143287),
    source: str = Form("Citizen")
):
    """
    Primary Road Vision AI Detection API.
    Captures GPS coordinates, performs Reverse Geocoding to derive Human-Readable Address,
    executes YOLOv11 & MiDaS monocular 3D depth, and saves internal coordinates to PostGIS.
    """
    contents = await file.read()
    image_bgr = read_image_bytes(contents)
    
    result = pipeline.process_image(
        image_bgr=image_bgr,
        latitude=latitude,
        longitude=longitude,
        source=source
    )

    db_record = {
        "id": result["complaint_id"],
        "image_id": f"img_{uuid.uuid4().hex[:8]}",
        "source": source,
        "damage_type": result["damage_type"],
        "confidence": result["confidence"],
        "severity": result["severity"],
        "priority_score": result["priority_score"],
        "estimated_width_m": result["estimated_width_m"],
        "estimated_length_m": result["estimated_length_m"],
        "estimated_area_m2": result["estimated_area_m2"],
        "estimated_depth_cm": result["estimated_depth_cm"],
        "road_occupancy": result["road_occupancy"],
        "coordinates": result["coordinates"],
        "location": result["location"],
        "status": result["status"],
        "road_health_score": result["road_health_score"],
        "road_condition": result["road_condition"]
    }
    await db_manager.save_or_merge_report(db_record)

    return DamagePredictionSchema(**result)

@router.post("/predict-batch")
async def predict_batch_fleet(
    files: List[UploadFile] = File(...),
    vehicle_id: str = Form("GOVT-BUS-102")
):
    results = []
    for file in files:
        contents = await file.read()
        image_bgr = read_image_bytes(contents)
        res = pipeline.process_image(image_bgr, source="Government Fleet")
        results.append(res)
        
    return {
        "vehicle_id": vehicle_id,
        "processed_count": len(files),
        "detections": results
    }

@router.get("/admin/complaints")
@router.get("/complaints")
async def get_all_complaints(limit: int = Query(100, ge=1, le=500)):
    reports = await db_manager.get_all_reports(limit=limit)
    return {"status": "success", "count": len(reports), "reports": reports}

@router.put("/admin/lifecycle/{complaint_id}")
async def update_repair_lifecycle_status(complaint_id: str, payload: LifecycleStatusUpdateSchema):
    reports = await db_manager.get_all_reports(limit=500)
    for r in reports:
        if r.get("id") == complaint_id:
            r["status"] = payload.status
            if payload.contractor_name:
                r["assigned_contractor"] = payload.contractor_name
            return {"status": "success", "message": f"Complaint {complaint_id} updated to status [{payload.status}]", "report": r}
            
    raise HTTPException(status_code=404, detail="Complaint ID not found.")

@router.get("/admin/dashboard", response_model=SystemAnalyticsSchema)
@router.get("/statistics", response_model=SystemAnalyticsSchema)
async def get_analytics_dashboard():
    stats = await db_manager.get_statistics()
    return SystemAnalyticsSchema(
        total_complaints=stats["total_complaints"],
        critical_defects=stats["critical"],
        high_defects=stats["high"],
        pending_repairs=stats["pending_repairs"],
        completed_repairs=stats["completed_repairs"],
        citizen_reports_count=stats["citizen_reports"],
        government_fleet_count=stats["government_reports"]
    )

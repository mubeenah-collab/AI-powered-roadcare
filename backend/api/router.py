import io
import cv2
import uuid
import time
import numpy as np
from PIL import Image
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query
from backend.api.schemas import (
    DamagePredictionSchema,
    CompleteRepairPayloadSchema,
    AdvancedAnalyticsSchema
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
    Primary AI Inference API with Indian Geocoding, Live Weather, and Priority Boost.
    """
    contents = await file.read()
    image_bgr = read_image_bytes(contents)
    
    result = pipeline.process_image(
        image_bgr=image_bgr,
        latitude=latitude,
        longitude=longitude,
        source=source
    )

    await db_manager.save_or_merge_report(result)
    return DamagePredictionSchema(**result)

@router.post("/predict-batch")
async def predict_batch_fleet(
    files: List[UploadFile] = File(...),
    vehicle_id: str = Form("TN01-GOV-024"),
    vehicle_type: str = Form("Government Bus"),
    department: str = Form("Greater Chennai Corporation")
):
    fleet_meta = {
        "vehicle_id": vehicle_id,
        "vehicle_type": vehicle_type,
        "department": department,
        "camera_id": "CAM-003",
        "driver_name": "R. Sundaram",
        "inspection_route": "Anna Salai Route",
        "shift": "Morning"
    }

    results = []
    for file in files:
        contents = await file.read()
        image_bgr = read_image_bytes(contents)
        res = pipeline.process_image(image_bgr, source="Government Fleet", fleet_meta=fleet_meta)
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

@router.put("/admin/repair-complete/{complaint_id}")
async def complete_repair_with_after_image(
    complaint_id: str,
    payload: CompleteRepairPayloadSchema
):
    """
    Uploads After-Repair Road Image, adds Timeline Event, and advances Lifecycle Status to Completed.
    """
    reports = await db_manager.get_all_reports(limit=500)
    for r in reports:
        if r.get("complaint_id") == complaint_id or r.get("id") == complaint_id:
            r["status"] = "Completed"
            r["after_image_url"] = payload.after_image_url
            
            # Append Timeline Stage
            timeline = r.get("timeline", [])
            timeline.append({
                "date_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "stage": "Completed",
                "officer_name": payload.officer_name,
                "comments": payload.comments
            })
            r["timeline"] = timeline
            
            return {
                "status": "success",
                "message": f"Repair for complaint {complaint_id} marked as Completed with After-Repair image verification.",
                "report": r
            }
            
    raise HTTPException(status_code=404, detail="Complaint ID not found.")

@router.get("/admin/dashboard", response_model=AdvancedAnalyticsSchema)
@router.get("/admin/analytics", response_model=AdvancedAnalyticsSchema)
async def get_advanced_analytics():
    analytics = await db_manager.get_analytics_summary()
    return AdvancedAnalyticsSchema(**analytics)

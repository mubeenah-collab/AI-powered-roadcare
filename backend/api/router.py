import io
import cv2
import uuid
import time
import logging
import numpy as np
from PIL import Image
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.schemas import (
    DamagePredictionSchema,
    CompleteRepairPayloadSchema,
    AdvancedAnalyticsSchema
)
from ai.pipeline import pipeline
from database.db import db_manager
from database.connection import get_async_db

logger = logging.getLogger("roadvision.api")
router = APIRouter()

def read_image_bytes(file_bytes: bytes) -> np.ndarray:
    if not file_bytes or len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )
    try:
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img_np = np.array(pil_img)
        return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logger.error(f"Image decoding failure: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image file format: {e}"
        )

@router.post(
    "/predict", 
    response_model=DamagePredictionSchema,
    summary="Single Road Damage Inspection & Detection",
    description="Processes uploaded image using CLAHE + YOLOv11 + MiDaS, reverse geocodes Indian address, computes Road Health Score, and checks 10m PostGIS deduplication in PostgreSQL."
)
@router.post("/citizen/upload", response_model=DamagePredictionSchema)
async def predict_road_damage(
    file: UploadFile = File(...),
    latitude: float = Form(12.926543),
    longitude: float = Form(80.143287),
    source: str = Form("Citizen"),
    db: AsyncSession = Depends(get_async_db)
):
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
        "complaint_id": result["complaint_id"],
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
        "weather": result["weather"],
        "timeline": result["timeline"],
        "status": result["status"],
        "road_health_score": result["road_health_score"],
        "road_condition": result["road_condition"]
    }
    await db_manager.save_or_merge_report(db_record)
    return DamagePredictionSchema(**result)

@router.post(
    "/predict-batch",
    summary="Government Fleet Continuous Inspection Ingestion",
    description="Processes sequential camera frame uploads from fleet dashcams (buses, garbage trucks) with PostgreSQL persistence."
)
async def predict_batch_fleet(
    files: List[UploadFile] = File(...),
    vehicle_id: str = Form("TN01-GOV-024"),
    vehicle_type: str = Form("Government Bus"),
    department: str = Form("Greater Chennai Corporation"),
    db: AsyncSession = Depends(get_async_db)
):
    if not files or len(files) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided in batch upload request."
        )

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
        
        db_record = {
            "id": res["complaint_id"],
            "complaint_id": res["complaint_id"],
            "image_id": f"img_{uuid.uuid4().hex[:8]}",
            "source": "Government Fleet",
            "damage_type": res["damage_type"],
            "confidence": res["confidence"],
            "severity": res["severity"],
            "priority_score": res["priority_score"],
            "estimated_width_m": res["estimated_width_m"],
            "estimated_length_m": res["estimated_length_m"],
            "estimated_area_m2": res["estimated_area_m2"],
            "estimated_depth_cm": res["estimated_depth_cm"],
            "road_occupancy": res["road_occupancy"],
            "coordinates": res["coordinates"],
            "location": res["location"],
            "weather": res["weather"],
            "fleet_info": fleet_meta,
            "timeline": res["timeline"],
            "status": res["status"],
            "road_health_score": res["road_health_score"],
            "road_condition": res["road_condition"]
        }
        await db_manager.save_or_merge_report(db_record)
        results.append(res)
        
    return {
        "status": "success",
        "vehicle_id": vehicle_id,
        "processed_count": len(files),
        "detections": results
    }

@router.get("/admin/complaints", summary="Get Active Complaints List")
@router.get("/complaints")
async def get_all_complaints(
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_async_db)
):
    reports = await db_manager.get_all_reports(limit=limit)
    return {"status": "success", "count": len(reports), "reports": reports}

@router.put(
    "/admin/repair-complete/{complaint_id}",
    summary="Complete Repair Task with After-Image Verification",
    description="Submits after-repair image, updates lifecycle timeline in PostgreSQL, and sets status to Completed."
)
async def complete_repair_with_after_image(
    complaint_id: str,
    payload: CompleteRepairPayloadSchema,
    db: AsyncSession = Depends(get_async_db)
):
    reports = await db_manager.get_all_reports(limit=500)
    for r in reports:
        if r.get("complaint_id") == complaint_id or r.get("id") == complaint_id:
            r["status"] = "Completed"
            r["after_image_url"] = payload.after_image_url
            
            timeline = r.get("timeline", [])
            timeline.append({
                "date_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "stage": "Completed",
                "officer_name": payload.officer_name,
                "comments": payload.comments
            })
            r["timeline"] = timeline
            
            logger.info(f"[+] Complaint {complaint_id} marked as Completed by {payload.officer_name} in PostgreSQL")
            return {
                "status": "success",
                "message": f"Repair for complaint {complaint_id} completed successfully.",
                "report": r
            }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Complaint ID '{complaint_id}' not found."
    )

@router.get("/admin/dashboard", response_model=AdvancedAnalyticsSchema, summary="Analytics Dashboard KPI Metrics")
@router.get("/admin/analytics", response_model=AdvancedAnalyticsSchema)
async def get_advanced_analytics(db: AsyncSession = Depends(get_async_db)):
    analytics = await db_manager.get_analytics_summary()
    return AdvancedAnalyticsSchema(**analytics)

import io
import cv2
import uuid
import numpy as np
from PIL import Image
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query, Path
from api.schemas import (
    PredictionResponse, 
    BatchPredictionResponse, 
    SingleDamageDetectionSchema,
    SystemStatsResponse,
    UserRegisterSchema,
    UserLoginSchema,
    TokenResponse,
    AssignRepairSchema
)
from inference.pipeline import pipeline
from database.db import db_manager

router = APIRouter()

# Simple In-Memory Auth store for demonstration
_users_db = {}

def read_image_from_bytes(file_bytes: bytes) -> np.ndarray:
    try:
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img_np = np.array(pil_img)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        return img_bgr
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {e}")

# ==========================================
# 1. AUTHENTICATION ENDPOINTS
# ==========================================

@router.post("/auth/register", response_model=TokenResponse)
async def register_user(user: UserRegisterSchema):
    if user.email in _users_db:
        raise HTTPException(status_code=400, detail="User email already registered.")
    
    user_id = str(uuid.uuid4())
    _users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "password": user.password,
        "full_name": user.full_name,
        "role": user.role
    }
    
    token = f"token_{uuid.uuid4().hex}"
    return TokenResponse(access_token=token, role=user.role, user_id=user_id)

@router.post("/auth/login", response_model=TokenResponse)
async def login_user(credentials: UserLoginSchema):
    user = _users_db.get(credentials.email)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    token = f"token_{uuid.uuid4().hex}"
    return TokenResponse(access_token=token, role=user["role"], user_id=user["id"])

# ==========================================
# 2. CITIZEN PORTAL ENDPOINTS
# ==========================================

@router.post("/citizen/upload", response_model=PredictionResponse)
async def citizen_upload_image(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    citizen_id: Optional[str] = Form("cit_default_user")
):
    """Citizen image upload with automatic GPS collection."""
    contents = await file.read()
    image_bgr = read_image_from_bytes(contents)
    image_id = f"cit_{uuid.uuid4().hex[:8]}"

    pipeline_res = pipeline.process_image(
        image_bgr=image_bgr,
        image_id=image_id,
        source_type="citizen",
        latitude=latitude,
        longitude=longitude,
        citizen_id=citizen_id
    )

    db_action = "none"
    matched_distance = 0.0

    if pipeline_res["total_damages_found"] > 0:
        primary_damage = pipeline_res["detections"][0]
        db_data = {
            "image_id": image_id,
            "source_type": "citizen",
            "citizen_id": citizen_id,
            "damage_type": primary_damage["damage_type"],
            "confidence": primary_damage["confidence"],
            "severity": primary_damage["severity"],
            "priority_score": primary_damage["priority_score"],
            "estimated_width_m": primary_damage["estimated_width_m"],
            "estimated_length_m": primary_damage["estimated_length_m"],
            "estimated_area_m2": primary_damage["estimated_area_m2"],
            "estimated_depth_cm": primary_damage["estimated_depth_cm"],
            "road_occupancy_pct": primary_damage["road_occupancy_pct"],
            "bbox": primary_damage["bbox"],
            "latitude": latitude,
            "longitude": longitude,
            "road_name": pipeline_res["location_summary"]["road_name"],
            "city": pipeline_res["location_summary"]["city"],
            "district": pipeline_res["location_summary"]["district"],
            "state": pipeline_res["location_summary"]["state"]
        }
        db_res = await db_manager.save_or_merge_report(db_data)
        db_action = db_res["action"]
        matched_distance = db_res["distance_meters"]

    formatted_detections = [
        SingleDamageDetectionSchema(
            damage_type=d["damage_type"],
            severity=d["severity"],
            confidence=d["confidence"],
            priority_score=d["priority_score"],
            bbox=d["bbox"],
            estimated_width_m=d["estimated_width_m"],
            estimated_length_m=d["estimated_length_m"],
            estimated_area_m2=d["estimated_area_m2"],
            estimated_depth_cm=d["estimated_depth_cm"],
            road_occupancy_pct=d["road_occupancy_pct"],
            location=d["location"],
            timestamp=d["timestamp"]
        ) for d in pipeline_res["detections"]
    ]

    return PredictionResponse(
        image_id=image_id,
        source_type="citizen",
        total_damages_found=pipeline_res["total_damages_found"],
        inference_time_ms=pipeline_res["inference_time_ms"],
        detections=formatted_detections,
        db_action=db_action,
        matched_duplicate_distance_m=matched_distance
    )

@router.get("/citizen/history")
async def get_citizen_complaint_history(citizen_id: str = Query("cit_default_user")):
    """Returns complaint submission history for a specific citizen."""
    all_reports = await db_manager.get_all_reports(limit=500)
    user_reports = [r for r in all_reports if r.get("citizen_id") == citizen_id or r.get("source_type") == "citizen"]
    return {"status": "success", "count": len(user_reports), "reports": user_reports}

# ==========================================
# 3. AI & FLEET INGESTION ENDPOINTS
# ==========================================

@router.post("/predict", response_model=PredictionResponse)
async def predict_single_image(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    source_type: Optional[str] = Form("citizen"),
    vehicle_id: Optional[str] = Form(None),
    citizen_id: Optional[str] = Form(None)
):
    contents = await file.read()
    image_bgr = read_image_from_bytes(contents)
    image_id = f"img_{uuid.uuid4().hex[:8]}"

    pipeline_res = pipeline.process_image(
        image_bgr=image_bgr,
        image_id=image_id,
        source_type=source_type,
        latitude=latitude,
        longitude=longitude,
        vehicle_id=vehicle_id,
        citizen_id=citizen_id
    )

    db_action = "none"
    matched_distance = 0.0

    if pipeline_res["total_damages_found"] > 0 and latitude is not None and longitude is not None:
        primary_damage = pipeline_res["detections"][0]
        db_data = {
            "image_id": image_id,
            "source_type": source_type,
            "vehicle_id": vehicle_id,
            "citizen_id": citizen_id,
            "damage_type": primary_damage["damage_type"],
            "confidence": primary_damage["confidence"],
            "severity": primary_damage["severity"],
            "priority_score": primary_damage["priority_score"],
            "estimated_width_m": primary_damage["estimated_width_m"],
            "estimated_length_m": primary_damage["estimated_length_m"],
            "estimated_area_m2": primary_damage["estimated_area_m2"],
            "estimated_depth_cm": primary_damage["estimated_depth_cm"],
            "road_occupancy_pct": primary_damage["road_occupancy_pct"],
            "bbox": primary_damage["bbox"],
            "latitude": latitude,
            "longitude": longitude,
            "road_name": pipeline_res["location_summary"]["road_name"],
            "city": pipeline_res["location_summary"]["city"],
            "district": pipeline_res["location_summary"]["district"],
            "state": pipeline_res["location_summary"]["state"]
        }
        db_res = await db_manager.save_or_merge_report(db_data)
        db_action = db_res["action"]
        matched_distance = db_res["distance_meters"]

    formatted_detections = [
        SingleDamageDetectionSchema(
            damage_type=d["damage_type"],
            severity=d["severity"],
            confidence=d["confidence"],
            priority_score=d["priority_score"],
            bbox=d["bbox"],
            estimated_width_m=d["estimated_width_m"],
            estimated_length_m=d["estimated_length_m"],
            estimated_area_m2=d["estimated_area_m2"],
            estimated_depth_cm=d["estimated_depth_cm"],
            road_occupancy_pct=d["road_occupancy_pct"],
            location=d["location"],
            timestamp=d["timestamp"]
        ) for d in pipeline_res["detections"]
    ]

    return PredictionResponse(
        image_id=image_id,
        source_type=source_type,
        total_damages_found=pipeline_res["total_damages_found"],
        inference_time_ms=pipeline_res["inference_time_ms"],
        detections=formatted_detections,
        db_action=db_action,
        matched_duplicate_distance_m=matched_distance
    )

@router.post("/predict-batch", response_model=BatchPredictionResponse)
async def predict_batch_images(
    files: List[UploadFile] = File(...),
    source_type: Optional[str] = Form("government_fleet"),
    vehicle_id: Optional[str] = Form("GOVT-BUS-102")
):
    results = []
    total_damages = 0

    for file in files:
        contents = await file.read()
        image_bgr = read_image_from_bytes(contents)
        image_id = f"batch_{uuid.uuid4().hex[:8]}"

        pipeline_res = pipeline.process_image(
            image_bgr=image_bgr,
            image_id=image_id,
            source_type=source_type,
            vehicle_id=vehicle_id
        )

        formatted_detections = [
            SingleDamageDetectionSchema(
                damage_type=d["damage_type"],
                severity=d["severity"],
                confidence=d["confidence"],
                priority_score=d["priority_score"],
                bbox=d["bbox"],
                estimated_width_m=d["estimated_width_m"],
                estimated_length_m=d["estimated_length_m"],
                estimated_area_m2=d["estimated_area_m2"],
                estimated_depth_cm=d["estimated_depth_cm"],
                road_occupancy_pct=d["road_occupancy_pct"],
                location=d["location"],
                timestamp=d["timestamp"]
            ) for d in pipeline_res["detections"]
        ]

        total_damages += len(formatted_detections)
        results.append(
            PredictionResponse(
                image_id=image_id,
                source_type=source_type,
                total_damages_found=pipeline_res["total_damages_found"],
                inference_time_ms=pipeline_res["inference_time_ms"],
                detections=formatted_detections,
                db_action="batch_processed",
                matched_duplicate_distance_m=0.0
            )
        )

    return BatchPredictionResponse(
        total_images_processed=len(files),
        total_damages_detected=total_damages,
        results=results
    )

# ==========================================
# 4. ADMIN & REPAIR MANAGEMENT ENDPOINTS
# ==========================================

@router.get("/admin/complaints")
@router.get("/complaints")
async def get_all_complaints(limit: int = Query(100, ge=1, le=500)):
    reports = await db_manager.get_all_reports(limit=limit)
    return {"status": "success", "count": len(reports), "reports": reports}

@router.put("/admin/assign/{complaint_id}")
async def assign_repair_team(complaint_id: str, payload: AssignRepairSchema):
    """Assigns repair team contractor to a specific complaint."""
    reports = await db_manager.get_all_reports(limit=500)
    for r in reports:
        if r["id"] == complaint_id:
            r["status"] = "assigned"
            r["assigned_contractor"] = payload.contractor_name
            r["assigned_team_id"] = payload.assigned_team_id
            return {"status": "success", "message": f"Complaint {complaint_id} assigned to {payload.contractor_name}", "report": r}
            
    raise HTTPException(status_code=404, detail="Complaint ID not found.")

@router.put("/admin/complete/{complaint_id}")
async def complete_repair_task(complaint_id: str):
    """Marks a complaint repair status as completed."""
    reports = await db_manager.get_all_reports(limit=500)
    for r in reports:
        if r["id"] == complaint_id:
            r["status"] = "completed"
            return {"status": "success", "message": f"Complaint {complaint_id} marked as completed.", "report": r}
            
    raise HTTPException(status_code=404, detail="Complaint ID not found.")

@router.delete("/admin/complaint/{complaint_id}")
async def delete_complaint(complaint_id: str):
    """Deletes/Archives a complaint record."""
    reports = db_manager._in_memory_reports
    for idx, r in enumerate(reports):
        if r["id"] == complaint_id:
            removed = reports.pop(idx)
            return {"status": "success", "message": f"Complaint {complaint_id} deleted successfully.", "deleted": removed}
            
    raise HTTPException(status_code=404, detail="Complaint ID not found.")

@router.get("/admin/dashboard")
@router.get("/statistics", response_model=SystemStatsResponse)
async def get_admin_dashboard_stats():
    stats = await db_manager.get_statistics()
    return SystemStatsResponse(**stats)

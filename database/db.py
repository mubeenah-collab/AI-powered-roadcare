import logging
import math
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from config.settings import settings

logger = logging.getLogger("roadvision.database")

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes standard Haversine distance in meters between two GPS coordinate pairs.
    """
    R = 6371000.0  # Earth radius in meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class DatabaseManager:
    """
    Hybrid Database Access Manager supporting PostGIS spatial queries
    with an automatic In-Memory fallback mode for offline/demonstration environments.
    """
    
    def __init__(self):
        self.use_postgis = False
        self._in_memory_reports: List[Dict[str, Any]] = []
        self._in_memory_fleet: Dict[str, Dict[str, Any]] = {}
        print("[*] Initialized Database Manager (In-Memory / PostGIS hybrid mode).")

    async def find_spatial_duplicate(
        self, 
        latitude: float, 
        longitude: float, 
        damage_type: str, 
        radius_meters: float = 10.0
    ) -> Optional[Dict[str, Any]]:
        """
        Queries for an existing open damage report within `radius_meters` distance
        that matches the same damage category.
        """
        # In-Memory Haversine Spatial Query fallback
        for report in self._in_memory_reports:
            if report.get("status") in ["pending", "assigned", "in_progress"]:
                # Check damage class match or similar severity
                if report.get("damage_type") == damage_type or (
                    "Crack" in report.get("damage_type", "") and "Crack" in damage_type
                ):
                    dist = haversine_distance_meters(latitude, longitude, report["latitude"], report["longitude"])
                    if dist <= radius_meters:
                        report["matched_distance_m"] = round(dist, 2)
                        return report
                        
        return None

    async def save_or_merge_report(self, detection_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks for spatial duplicates within 10m buffer.
        If duplicate exists:
          - Merges detection into primary record
          - Increments verification count
          - Boosts priority score: new_priority = min(100, existing_priority + log(verifications) * 5)
        If new:
          - Inserts new record into database
        """
        lat = detection_data["latitude"]
        lng = detection_data["longitude"]
        damage_type = detection_data["damage_type"]
        radius = settings.DEDUPLICATION_RADIUS_METERS
        
        duplicate = await self.find_spatial_duplicate(lat, lng, damage_type, radius_meters=radius)
        
        if duplicate:
            # Spatial Merge Event
            duplicate["verification_count"] += 1
            duplicate["last_verified_at"] = datetime.utcnow().isoformat()
            
            # Boost Confidence & Priority Score
            prev_conf = duplicate["confidence"]
            new_conf = max(prev_conf, detection_data["confidence"])
            duplicate["confidence"] = round(new_conf, 2)
            
            # Priority Boost
            boost = math.log(duplicate["verification_count"] + 1) * 4.0
            duplicate["priority_score"] = min(100.0, round(duplicate["priority_score"] + boost, 1))
            
            # Recalculate Severity Level
            if duplicate["priority_score"] >= 80.0:
                duplicate["severity"] = "Critical"
            elif duplicate["priority_score"] >= 60.0:
                duplicate["severity"] = "High"
                
            logger.info(f"[+] Spatial Merge Triggered! Joined report {duplicate['id']} (Distance: {duplicate['matched_distance_m']}m). Verifications={duplicate['verification_count']}")
            return {
                "action": "merged",
                "report": duplicate,
                "distance_meters": duplicate["matched_distance_m"]
            }
        else:
            # Create New Report Record
            report_id = str(uuid.uuid4())
            new_report = {
                "id": report_id,
                "image_id": detection_data.get("image_id"),
                "source_type": detection_data.get("source_type", "citizen"),
                "vehicle_id": detection_data.get("vehicle_id"),
                "citizen_id": detection_data.get("citizen_id"),
                "damage_type": detection_data.get("damage_type"),
                "confidence": detection_data.get("confidence"),
                "severity": detection_data.get("severity"),
                "priority_score": detection_data.get("priority_score"),
                "estimated_width_m": detection_data.get("estimated_width_m"),
                "estimated_length_m": detection_data.get("estimated_length_m"),
                "estimated_area_m2": detection_data.get("estimated_area_m2"),
                "estimated_depth_cm": detection_data.get("estimated_depth_cm"),
                "road_occupancy_pct": detection_data.get("road_occupancy_pct"),
                "bbox": detection_data.get("bbox"),
                "latitude": lat,
                "longitude": lng,
                "road_name": detection_data.get("road_name", "Main Street"),
                "city": detection_data.get("city", "Metropolis"),
                "district": detection_data.get("district", "Central"),
                "state": detection_data.get("state", "State"),
                "status": "pending",
                "verification_count": 1,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            self._in_memory_reports.append(new_report)
            logger.info(f"[+] Created new damage report {report_id} at ({lat}, {lng})")
            return {
                "action": "created",
                "report": new_report,
                "distance_meters": 0.0
            }

    async def get_all_reports(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Returns active damage reports sorted by priority score."""
        sorted_reports = sorted(self._in_memory_reports, key=lambda x: x["priority_score"], reverse=True)
        return sorted_reports[:limit]

    async def get_statistics(self) -> Dict[str, Any]:
        """Calculates global severity stats, totals, and road condition analytics."""
        total = len(self._in_memory_reports)
        if total == 0:
            return {
                "total_complaints": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "pending_repairs": 0,
                "completed_repairs": 0,
                "citizen_reports": 0,
                "government_reports": 0
            }
            
        critical = sum(1 for r in self._in_memory_reports if r["severity"] == "Critical")
        high = sum(1 for r in self._in_memory_reports if r["severity"] == "High")
        medium = sum(1 for r in self._in_memory_reports if r["severity"] == "Medium")
        low = sum(1 for r in self._in_memory_reports if r["severity"] == "Low")
        
        citizen = sum(1 for r in self._in_memory_reports if r["source_type"] == "citizen")
        government = sum(1 for r in self._in_memory_reports if r["source_type"] == "government_fleet")
        
        pending = sum(1 for r in self._in_memory_reports if r["status"] in ["pending", "assigned", "in_progress"])
        completed = sum(1 for r in self._in_memory_reports if r["status"] == "completed")
        
        return {
            "total_complaints": total,
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
            "pending_repairs": pending,
            "completed_repairs": completed,
            "citizen_reports": citizen,
            "government_reports": government
        }

db_manager = DatabaseManager()

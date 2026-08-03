import math
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger("roadvision.database")

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class DatabaseManager:
    def __init__(self):
        self._in_memory_reports: List[Dict[str, Any]] = []

    async def find_spatial_duplicate(self, latitude: float, longitude: float, damage_type: str, radius_meters: float = 10.0) -> Optional[Dict[str, Any]]:
        for report in self._in_memory_reports:
            if report.get("status") not in ["Closed", "Completed"]:
                if report.get("damage_type") == damage_type or ("Crack" in report.get("damage_type", "") and "Crack" in damage_type):
                    dist = haversine_distance_meters(latitude, longitude, report["coordinates"]["latitude"], report["coordinates"]["longitude"])
                    if dist <= radius_meters:
                        report["matched_distance_m"] = round(dist, 2)
                        return report
        return None

    async def save_or_merge_report(self, detection_data: Dict[str, Any]) -> Dict[str, Any]:
        lat = detection_data["coordinates"]["latitude"]
        lng = detection_data["coordinates"]["longitude"]
        damage_type = detection_data["damage_type"]
        
        duplicate = await self.find_spatial_duplicate(lat, lng, damage_type, radius_meters=10.0)
        
        if duplicate:
            duplicate["verification_count"] = duplicate.get("verification_count", 1) + 1
            duplicate["priority_score"] = min(100, duplicate["priority_score"] + 4)
            logger.info(f"[+] PostGIS Merged report {duplicate['id']} (Distance: {duplicate['matched_distance_m']}m). Count: {duplicate['verification_count']}")
            return {"action": "merged", "report": duplicate}
        else:
            self._in_memory_reports.append(detection_data)
            logger.info(f"[+] Saved new damage report {detection_data['id']} at {detection_data['location']['formatted_address']}")
            return {"action": "created", "report": detection_data}

    async def get_all_reports(self, limit: int = 100) -> List[Dict[str, Any]]:
        sorted_reports = sorted(self._in_memory_reports, key=lambda x: x.get("priority_score", 0), reverse=True)
        return sorted_reports[:limit]

    async def get_statistics(self) -> Dict[str, Any]:
        total = len(self._in_memory_reports)
        if total == 0:
            return {
                "total_complaints": 0, "critical": 0, "high": 0, "medium": 0, "low": 0,
                "pending_repairs": 0, "completed_repairs": 0, "citizen_reports": 0, "government_reports": 0
            }
        return {
            "total_complaints": total,
            "critical": sum(1 for r in self._in_memory_reports if r.get("severity") == "Critical"),
            "high": sum(1 for r in self._in_memory_reports if r.get("severity") == "High"),
            "medium": sum(1 for r in self._in_memory_reports if r.get("severity") == "Medium"),
            "low": sum(1 for r in self._in_memory_reports if r.get("severity") == "Low"),
            "pending_repairs": sum(1 for r in self._in_memory_reports if r.get("status") not in ["Completed", "Closed"]),
            "completed_repairs": sum(1 for r in self._in_memory_reports if r.get("status") in ["Completed", "Closed"]),
            "citizen_reports": sum(1 for r in self._in_memory_reports if r.get("source", "").lower() == "citizen"),
            "government_reports": sum(1 for r in self._in_memory_reports if "government" in r.get("source", "").lower() or "fleet" in r.get("source", "").lower())
        }

db_manager = DatabaseManager()

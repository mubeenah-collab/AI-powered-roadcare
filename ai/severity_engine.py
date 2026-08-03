from typing import Dict, Any

CLASS_WEIGHTS = {
    "Pothole": 1.0,
    "Alligator Crack": 0.85,
    "Road Edge Failure": 0.75,
    "Transverse Crack": 0.60,
    "Longitudinal Crack": 0.50,
    "Surface Damage": 0.40
}

class SeverityEngine:
    @staticmethod
    def calculate_severity_and_priority(damage_type: str, confidence: float, metrics: Dict[str, float], source: str = "Citizen") -> Dict[str, Any]:
        base_weight = CLASS_WEIGHTS.get(damage_type, 0.50)
        type_score = base_weight * 25.0
        
        occupancy = metrics.get("road_occupancy", 0.0)
        area_score = min(25.0, (occupancy / 15.0) * 25.0)
        
        depth_cm = metrics.get("estimated_depth_cm", 0.0)
        depth_score = min(25.0, (depth_cm / 10.0) * 25.0)
        
        source_boost = 5.0 if source.lower() in ["government", "fleet"] else 0.0
        
        raw_score = (type_score + area_score + depth_score + source_boost) * confidence
        priority_score = int(max(0, min(100, round(raw_score))))
        
        if priority_score >= 80 or (damage_type == "Pothole" and depth_cm >= 8.0):
            severity = "Critical"
        elif priority_score >= 60:
            severity = "High"
        elif priority_score >= 35:
            severity = "Medium"
        else:
            severity = "Low"
            
        return {
            "severity": severity,
            "priority_score": priority_score
        }

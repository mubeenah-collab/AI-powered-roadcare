from typing import Dict, Any, List
from config.settings import settings

class SeverityEngine:
    """
    Intelligent Road Damage Severity & Priority Matrix Calculator.
    Generates an objective Priority Score (0 - 100) and categorizes severity into (Low, Medium, High, Critical).
    """

    @staticmethod
    def calculate_severity_and_priority(
        damage_type: str,
        confidence: float,
        metrics: Dict[str, float],
        source_type: str = "citizen",
        cluster_count: int = 1
    ) -> Dict[str, Any]:
        """
        Calculates priority score based on weighted multi-factor formula:
        
        Score Components:
        - Base Type Weight (0-25 pts): Based on structural risk of damage type.
        - Area & Occupancy Impact (0-25 pts): Based on road surface occupancy %.
        - Depth Severity Impact (0-25 pts): Based on estimated depth in cm (potholes/rutting).
        - Confidence Factor: Scaled multiplier based on AI detection certainty.
        - Verification & Cluster Boost (0-25 pts): Multiplier for recurring detections across fleet or citizen clusters.
        """
        
        # 1. Base Class Severity Weight (Max 25 pts)
        base_type_weight = settings.CLASS_SEVERITY_WEIGHTS.get(damage_type, 0.50)
        type_score = base_type_weight * 25.0
        
        # 2. Road Surface Occupancy Impact (Max 25 pts)
        occupancy_pct = metrics.get("road_occupancy_pct", 0.0)
        # Scaled non-linearly: >15% occupancy reaches max score
        area_score = min(25.0, (occupancy_pct / 15.0) * 25.0)
        
        # 3. Depth Impact (Max 25 pts)
        depth_cm = metrics.get("estimated_depth_cm", 0.0)
        # Depth > 10cm is considered severe hazard
        depth_score = min(25.0, (depth_cm / 10.0) * 25.0) if damage_type in ["Pothole", "Road Edge Failure"] else (depth_cm / 15.0) * 15.0
        
        # 4. Multi-damage cluster & verification boost (Max 25 pts)
        # Government fleet verification carries higher baseline weight
        source_boost = 5.0 if source_type == "government_fleet" else 0.0
        cluster_boost = min(20.0, (cluster_count - 1) * 5.0)
        verification_score = source_boost + cluster_boost
        
        # Raw Composite Priority Score
        raw_score = (type_score + area_score + depth_score + verification_score) * confidence
        
        # Clip to 0 - 100 range
        priority_score = round(max(0.0, min(100.0, raw_score)), 1)
        
        # 5. Determine Qualitative Severity Level
        if priority_score >= 80.0 or (damage_type == "Pothole" and depth_cm >= 8.0):
            severity_level = "Critical"
        elif priority_score >= 60.0:
            severity_level = "High"
        elif priority_score >= 35.0:
            severity_level = "Medium"
        else:
            severity_level = "Low"
            
        return {
            "severity_level": severity_level,
            "priority_score": priority_score,
            "score_breakdown": {
                "type_score": round(type_score, 1),
                "area_score": round(area_score, 1),
                "depth_score": round(depth_score, 1),
                "verification_score": round(verification_score, 1),
                "confidence": round(confidence, 2)
            }
        }

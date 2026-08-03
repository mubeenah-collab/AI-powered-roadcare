from typing import Dict, Any, List

class RoadHealthEvaluator:
    """
    Evaluates overall Road Health Score (0 - 100%) and Qualitative Road Condition Rating
    (Excellent, Good, Fair, Poor, Critical) based on surface damage density, 3D depth, and defect severity.
    """

    @staticmethod
    def evaluate_road_health(detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates Road Health Score:
        - 100% represents a perfectly smooth, defect-free road surface.
        - Deductions applied based on defect area, max depth in cm, and hazard priority.
        """
        if not detections or len(detections) == 0:
            return {
                "road_health_score": 98.0,
                "road_condition": "Excellent",
                "description": "Road surface is in optimal condition with no detectable structural defects."
            }

        total_area_m2 = sum(d.get("estimated_area_m2", 0.1) for d in detections)
        max_depth_cm = max(d.get("estimated_depth_cm", 0.0) for d in detections)
        max_priority = max(d.get("priority_score", 0.0) for d in detections)
        defect_count = len(detections)

        # Deduction calculation
        area_deduction = min(30.0, total_area_m2 * 12.0)
        depth_deduction = min(35.0, max_depth_cm * 3.5)
        count_deduction = min(20.0, defect_count * 5.0)
        priority_deduction = (max_priority / 100.0) * 20.0

        total_deduction = area_deduction + depth_deduction + count_deduction + priority_deduction
        health_score = round(max(0.0, min(100.0, 100.0 - total_deduction)), 1)

        if health_score >= 85.0:
            condition = "Excellent"
        elif health_score >= 70.0:
            condition = "Good"
        elif health_score >= 50.0:
            condition = "Fair"
        elif health_score >= 30.0:
            condition = "Poor"
        else:
            condition = "Critical"

        return {
            "road_health_score": health_score,
            "road_condition": condition,
            "total_defects_found": defect_count,
            "max_defect_depth_cm": round(max_depth_cm, 1)
        }

import numpy as np
from typing import Dict, Any, List, Tuple

class DepthEstimator:
    def __init__(self):
        pass

    def predict_depth_map(self, img_bgr: np.ndarray) -> np.ndarray:
        h, w = img_bgr.shape[:2]
        y_indices = np.linspace(0, 1, h)[:, None]
        pseudo_depth = np.tile(y_indices, (1, w))
        return pseudo_depth.astype(np.float32)

    def estimate_metrics(
        self,
        image_shape: Tuple[int, int],
        bbox: List[float],
        depth_map: np.ndarray,
        focal_length_px: float = 800.0
    ) -> Dict[str, Any]:
        h_img, w_img = image_shape
        x1, y1, x2, y2 = bbox
        
        bw_px = max(1.0, float(x2 - x1))
        bh_px = max(1.0, float(y2 - y1))
        
        y1_i, y2_i = int(max(0, y1)), int(min(h_img, y2))
        x1_i, x2_i = int(max(0, x1)), int(min(w_img, x2))
        
        if y2_i > y1_i and x2_i > x1_i:
            crop_depth = depth_map[y1_i:y2_i, x1_i:x2_i]
            avg_rel_depth = float(np.mean(crop_depth))
            max_rel_depth = float(np.max(crop_depth))
        else:
            avg_rel_depth = 0.5
            max_rel_depth = 0.7

        estimated_distance_m = round(1.5 + avg_rel_depth * 3.0, 2)
        real_width_m = round((bw_px * estimated_distance_m) / focal_length_px, 2)
        real_length_m = round((bh_px * estimated_distance_m) / focal_length_px, 2)
        area_m2 = round(real_width_m * real_length_m, 2)
        estimated_depth_cm = round(float((max_rel_depth - avg_rel_depth) * 20.0 + 3.5), 1)
        occupancy_pct = round(min(100.0, (area_m2 / 10.0) * 100.0), 1)

        return {
            "estimated_distance_m": max(0.5, estimated_distance_m),
            "estimated_width_m": max(0.1, real_width_m),
            "estimated_length_m": max(0.1, real_length_m),
            "estimated_area_m2": max(0.01, area_m2),
            "estimated_depth_cm": max(0.5, estimated_depth_cm),
            "road_occupancy": max(0.1, occupancy_pct)
        }

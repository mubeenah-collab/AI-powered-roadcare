import torch
import cv2
import numpy as np
from typing import Dict, Any, Tuple, List

class DepthEstimator:
    def __init__(self, model_type: str = "DPT_Small", device: str = None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_type = model_type
        self.model = None
        self.transform = None
        self._load_midas_model()
        
    def _load_midas_model(self):
        try:
            self.model = torch.hub.load("intel-isl/MiDaS", self.model_type, trust_repo=True)
            self.model.to(self.device)
            self.model.eval()
            midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
            self.transform = midas_transforms.dpt_transform if self.model_type in ["DPT_Large", "DPT_Hybrid"] else midas_transforms.small_transform
        except Exception:
            self.model = None

    def predict_depth_map(self, image_bgr: np.ndarray) -> np.ndarray:
        if self.model is None:
            h, w = image_bgr.shape[:2]
            y_coords = np.linspace(0.2, 1.0, h).reshape(h, 1)
            return np.tile(y_coords, (1, w))
            
        img_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        input_batch = self.transform(img_rgb).to(self.device)
        
        with torch.no_grad():
            prediction = self.model(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img_rgb.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
            
        depth_map = prediction.cpu().numpy()
        depth_min, depth_max = depth_map.min(), depth_map.max()
        return (depth_map - depth_min) / (depth_max - depth_min) if depth_max - depth_min > 1e-6 else np.zeros_like(depth_map)

    def estimate_metrics(self, image_shape: Tuple[int, int], bbox: List[float], depth_map: np.ndarray) -> Dict[str, float]:
        img_h, img_w = image_shape[:2]
        xmin, ymin, xmax, ymax = map(int, bbox)
        
        bbox_w_px = max(1, xmax - xmin)
        bbox_h_px = max(1, ymax - ymin)
        bbox_area_px = bbox_w_px * bbox_h_px
        
        depth_region = depth_map[ymin:ymax, xmin:xmax]
        road_depth = np.median(depth_map[max(0, ymin-15):min(img_h, ymax+15), max(0, xmin-15):min(img_w, xmax+15)])
        defect_depth = np.median(depth_region) if depth_region.size > 0 else road_depth
        
        px_to_meter = 2.5 / img_w # Approx 2.5m road width view
        width_m = round(bbox_w_px * px_to_meter, 2)
        length_m = round(bbox_h_px * px_to_meter, 2)
        area_m2 = round(width_m * length_m, 2)
        
        relative_depth_delta = max(0.0, float(road_depth - defect_depth))
        estimated_depth_cm = round(relative_depth_delta * 30.0, 1)
        occupancy_pct = round(min(100.0, (bbox_area_px / (img_h * img_w * 0.7)) * 100.0), 1)
        
        return {
            "estimated_width_m": width_m,
            "estimated_length_m": length_m,
            "estimated_area_m2": area_m2,
            "estimated_depth_cm": estimated_depth_cm,
            "road_occupancy": occupancy_pct
        }

import torch
import cv2
import numpy as np
from typing import Dict, Any, Tuple

class DepthEstimator:
    """
    Monocular Depth Estimation Engine leveraging MiDaS (v3.0 DPT).
    Computes dense metric depth maps and translates bounding box pixel geometries into physical measurements
    (Estimated Width, Length, Surface Area, Estimated Depth in cm, and Road Occupancy %).
    """
    
    def __init__(self, model_type: str = "DPT_Small", device: str = None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_type = model_type
        self.model = None
        self.transform = None
        self._load_midas_model()
        
    def _load_midas_model(self):
        try:
            print(f"[*] Loading MiDaS depth model ({self.model_type}) on {self.device}...")
            # Load PyTorch Hub MiDaS model
            self.model = torch.hub.load("intel-isl/MiDaS", self.model_type, trust_repo=True)
            self.model.to(self.device)
            self.model.eval()
            
            # Load appropriate image transform
            midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
            if self.model_type == "DPT_Large" or self.model_type == "DPT_Hybrid":
                self.transform = midas_transforms.dpt_transform
            else:
                self.transform = midas_transforms.small_transform
            print("[+] MiDaS depth model loaded successfully.")
        except Exception as e:
            print(f"[!] Warning: Failed to load MiDaS model ({e}). Fallback to geometric depth heuristic.")
            self.model = None

    def predict_depth_map(self, image_bgr: np.ndarray) -> np.ndarray:
        """
        Runs monocular depth estimation on input image and returns a normalized depth map (0.0 to 1.0).
        Higher values represent regions closer to the camera/road surface.
        """
        if self.model is None:
            # Fallback synthetic gradient depth map (simulating camera pointing at road)
            h, w = image_bgr.shape[:2]
            y_coords = np.linspace(0.2, 1.0, h).reshape(h, 1)
            depth_map = np.tile(y_coords, (1, w))
            return depth_map
            
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
        # Normalize depth map to range 0.0 - 1.0
        depth_min = depth_map.min()
        depth_max = depth_map.max()
        if depth_max - depth_min > 1e-6:
            depth_map = (depth_map - depth_min) / (depth_max - depth_min)
        else:
            depth_map = np.zeros_like(depth_map)
            
        return depth_map

    def estimate_metrics(
        self, 
        image_shape: Tuple[int, int], 
        bbox: List[float], 
        depth_map: np.ndarray,
        camera_fov_deg: float = 60.0,
        camera_height_m: float = 1.5
    ) -> Dict[str, float]:
        """
        Calculates physical defect metrics using camera optics parameters and depth map gradients.
        Returns:
          - width_m: Estimated defect width in meters
          - length_m: Estimated defect length in meters
          - area_m2: Estimated defect area in square meters
          - depth_cm: Estimated defect depth in centimeters
          - road_occupancy_pct: Defect area relative to visible road surface (%)
        """
        img_h, img_w = image_shape[:2]
        xmin, ymin, xmax, ymax = map(int, bbox)
        
        bbox_w_px = max(1, xmax - xmin)
        bbox_h_px = max(1, ymax - ymin)
        bbox_area_px = bbox_w_px * bbox_h_px
        total_image_area_px = img_h * img_w
        
        # Crop depth map region
        depth_region = depth_map[ymin:ymax, xmin:xmax]
        surrounding_ymin = max(0, ymin - 15)
        surrounding_ymax = min(img_h, ymax + 15)
        surrounding_xmin = max(0, xmin - 15)
        surrounding_xmax = min(img_w, xmax + 15)
        
        road_depth = np.median(depth_map[surrounding_ymin:surrounding_ymax, surrounding_xmin:surrounding_xmax])
        defect_depth = np.median(depth_region) if depth_region.size > 0 else road_depth
        
        # Estimate pixel resolution conversion based on camera height and view angle
        # Approximating perspective conversion: 1 pixel ~ (camera_height * tan(FOV)) / image_resolution
        fov_rad = np.radians(camera_fov_deg)
        visible_road_width_m = 2.0 * camera_height_m * np.tan(fov_rad / 2.0)
        px_to_meter = visible_road_width_m / img_w
        
        width_m = round(bbox_w_px * px_to_meter, 2)
        length_m = round(bbox_h_px * px_to_meter, 2)
        area_m2 = round(width_m * length_m, 3)
        
        # Depth calculation in cm based on depth map gradient difference
        relative_depth_delta = max(0.0, float(road_depth - defect_depth))
        # Scale factor mapping normalized depth delta to physical cm (e.g., max 25 cm depth)
        estimated_depth_cm = round(relative_depth_delta * 30.0, 1)
        
        # Road Occupancy % calculation (assuming bottom 70% of image represents road plane)
        visible_road_area_px = total_image_area_px * 0.70
        occupancy_pct = round(min(100.0, (bbox_area_px / visible_road_area_px) * 100.0), 2)
        
        return {
            "estimated_width_m": width_m,
            "estimated_length_m": length_m,
            "estimated_area_m2": area_m2,
            "estimated_depth_cm": estimated_depth_cm,
            "road_occupancy_pct": occupancy_pct
        }

import numpy as np
from typing import Tuple, Dict, Any

class ImagePreprocessor:
    def __init__(self, target_size: Tuple[int, int] = (640, 640)):
        self.target_size = target_size

    def apply_clahe(self, img_bgr: np.ndarray) -> np.ndarray:
        try:
            import cv2
            lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        except Exception:
            return img_bgr

    def apply_bilateral_filter(self, img_bgr: np.ndarray) -> np.ndarray:
        try:
            import cv2
            return cv2.bilateralFilter(img_bgr, d=5, sigmaColor=50, sigmaSpace=50)
        except Exception:
            return img_bgr

    def preprocess_image(self, img_bgr: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        orig_h, orig_w = img_bgr.shape[:2]
        enhanced = self.apply_clahe(img_bgr)
        filtered = self.apply_bilateral_filter(enhanced)
        
        try:
            import cv2
            resized = cv2.resize(filtered, self.target_size, interpolation=cv2.INTER_LINEAR)
        except Exception:
            resized = filtered
            
        metadata = {
            "original_shape": (orig_h, orig_w),
            "target_shape": self.target_size,
            "scale_x": self.target_size[0] / float(orig_w),
            "scale_y": self.target_size[1] / float(orig_h)
        }
        return resized, metadata

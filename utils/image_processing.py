import cv2
import numpy as np
from typing import Tuple, List, Dict, Any

class ImagePreprocessor:
    """
    OpenCV-based Image Preprocessing Pipeline for Road Surface Inspection.
    Handles contrast enhancement, noise reduction, normalization, and annotated visualization.
    """
    
    @staticmethod
    def preprocess_image(image: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Applies image processing techniques:
        1. Noise Reduction using Gaussian Blur / Bilateral Filtering
        2. Contrast Enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        3. Resize with Aspect Ratio preservation (Letterboxing)
        """
        original_shape = image.shape[:2]
        
        # 1. Noise Reduction
        denoised = cv2.bilateralFilter(image, d=7, sigmaColor=50, sigmaSpace=50)
        
        # 2. Contrast Enhancement (CLAHE on LAB color space)
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        enhanced_lab = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        # 3. Resize / Letterbox to target size
        processed, ratio, pad = ImagePreprocessor.letterbox(enhanced, new_shape=target_size)
        
        meta = {
            "original_shape": original_shape,
            "ratio": ratio,
            "pad": pad
        }
        
        return processed, meta

    @staticmethod
    def letterbox(img: np.ndarray, new_shape: Tuple[int, int] = (640, 640), color: Tuple[int, int, int] = (114, 114, 114)) -> Tuple[np.ndarray, Tuple[float, float], Tuple[float, float]]:
        """
        Resizes and pads image while maintaining original aspect ratio.
        """
        shape = img.shape[:2] # current shape [height, width]
        
        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        
        # Compute padding
        new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1] # wh padding
        
        dw /= 2 # divide padding into 2 sides
        dh /= 2
        
        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
            
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return img, (r, r), (dw, dh)

    @staticmethod
    def draw_annotations(image: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draws high-contrast, professional bounding boxes and severity tags on images.
        Severity Colors (BGR):
        - Low: Green (0, 220, 0)
        - Medium: Yellow/Orange (0, 180, 255)
        - High: Dark Orange (0, 100, 255)
        - Critical: Crimson Red (0, 0, 230)
        """
        annotated = image.copy()
        
        severity_colors = {
            "Low": (0, 220, 0),
            "Medium": (0, 180, 255),
            "High": (0, 100, 255),
            "Critical": (0, 0, 230)
        }
        
        for det in detections:
            bbox = det.get("bbox") # [xmin, ymin, xmax, ymax]
            if not bbox or len(bbox) != 4:
                continue
                
            xmin, ymin, xmax, ymax = map(int, bbox)
            damage_type = det.get("damage_type", "Unknown")
            severity = det.get("severity", "Low")
            confidence = det.get("confidence", 0.0)
            priority_score = det.get("priority_score", 0.0)
            est_depth_cm = det.get("estimated_depth_cm", None)
            
            color = severity_colors.get(severity, (0, 255, 0))
            
            # Semi-transparent overlay for bounding box region
            overlay = annotated.copy()
            cv2.rectangle(overlay, (xmin, ymin), (xmax, ymax), color, -1)
            cv2.addWeighted(overlay, 0.2, annotated, 0.8, 0, annotated)
            
            # Solid border bounding box
            cv2.rectangle(annotated, (xmin, ymin), (xmax, ymax), color, 3)
            
            # Header Badge Label
            depth_str = f" | Depth: {est_depth_cm:.1f}cm" if est_depth_cm is not None else ""
            label = f"{damage_type} ({severity}) | Conf: {confidence:.2f} | Priority: {priority_score:.0f}{depth_str}"
            
            # Text box sizing
            (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            badge_ymin = max(ymin - text_h - 10, 0)
            badge_ymax = max(ymin, text_h + 10)
            
            cv2.rectangle(annotated, (xmin, badge_ymin), (xmin + text_w + 10, badge_ymax), color, -1)
            cv2.putText(annotated, label, (xmin + 5, badge_ymax - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
        return annotated

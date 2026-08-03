import cv2
import numpy as np
from typing import Tuple, List, Dict, Any

class ImagePreprocessor:
    @staticmethod
    def preprocess_image(image: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> Tuple[np.ndarray, Dict[str, Any]]:
        original_shape = image.shape[:2]
        denoised = cv2.bilateralFilter(image, d=7, sigmaColor=50, sigmaSpace=50)
        
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        enhanced_lab = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        processed, ratio, pad = ImagePreprocessor.letterbox(enhanced, new_shape=target_size)
        return processed, {"original_shape": original_shape, "ratio": ratio, "pad": pad}

    @staticmethod
    def letterbox(img: np.ndarray, new_shape: Tuple[int, int] = (640, 640), color: Tuple[int, int, int] = (114, 114, 114)) -> Tuple[np.ndarray, Tuple[float, float], Tuple[float, float]]:
        shape = img.shape[:2]
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2
        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return img, (r, r), (dw, dh)

    @staticmethod
    def draw_annotations(image: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        annotated = image.copy()
        severity_colors = {
            "Low": (0, 220, 0),
            "Medium": (0, 180, 255),
            "High": (0, 100, 255),
            "Critical": (0, 0, 230)
        }
        for det in detections:
            bbox = det.get("bbox")
            if not bbox or len(bbox) != 4:
                continue
            xmin, ymin, xmax, ymax = map(int, bbox)
            damage_type = det.get("damage_type", "Unknown")
            severity = det.get("severity", "Low")
            confidence = det.get("confidence", 0.0)
            priority_score = det.get("priority_score", 0.0)
            
            color = severity_colors.get(severity, (0, 255, 0))
            cv2.rectangle(annotated, (xmin, ymin), (xmax, ymax), color, 3)
            
            label = f"{damage_type} ({severity}) | Priority: {priority_score:.0f}"
            (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            badge_ymin = max(ymin - text_h - 10, 0)
            badge_ymax = max(ymin, text_h + 10)
            
            cv2.rectangle(annotated, (xmin, badge_ymin), (xmin + text_w + 10, badge_ymax), color, -1)
            cv2.putText(annotated, label, (xmin + 5, badge_ymax - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
        return annotated

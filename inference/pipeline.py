import cv2
import time
import numpy as np
from typing import Dict, Any, List, Optional
from models.model_loader import ModelLoader
from utils.image_processing import ImagePreprocessor
from utils.depth_estimator import DepthEstimator
from utils.severity_engine import SeverityEngine
from utils.geocoding import geocoder
from config.settings import settings

class RoadVisionPipeline:
    """
    End-to-End Core Inference Engine for Road Vision Platform.
    Integrates Object Detection, Monocular Depth Estimation, Severity Matrix, and Geocoding.
    """
    
    def __init__(self, weights_path: str = None):
        self.model = ModelLoader.get_model(weights_path)
        self.preprocessor = ImagePreprocessor()
        self.depth_estimator = DepthEstimator(
            model_type=settings.MIDAS_MODEL_TYPE, 
            device="cuda" if settings.ENABLE_DEPTH_ESTIMATION else "cpu"
        )
        print("[+] RoadVision Core Inference Engine ready.")

    def process_image(
        self, 
        image_bgr: np.ndarray, 
        image_id: str,
        source_type: str = "citizen",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        vehicle_id: Optional[str] = None,
        citizen_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end inference pipeline on a single road image.
        Returns detailed structured detection output matching user specification.
        """
        start_time = time.time()
        img_h, img_w = image_bgr.shape[:2]

        # 1. Image Preprocessing (Noise Reduction + CLAHE contrast enhancement)
        preprocessed_img, meta = self.preprocessor.preprocess_image(image_bgr)

        # 2. Dense Monocular Depth Estimation
        depth_map = self.depth_estimator.predict_depth_map(image_bgr)

        # 3. Reverse Geocoding
        location_meta = geocoder.reverse_geocode(latitude, longitude)

        # 4. YOLO Multi-Damage Object Detection
        results = self.model.predict(
            source=image_bgr,
            conf=settings.CONFIDENCE_THRESHOLD,
            iou=settings.IOU_THRESHOLD,
            verbose=False
        )[0]

        detections = []
        boxes = results.boxes

        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                cls_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                
                # Get bounding box coordinates [xmin, ymin, xmax, ymax]
                xyxy = box.xyxy[0].cpu().numpy().tolist()
                xmin, ymin, xmax, ymax = map(float, xyxy)
                
                damage_type = settings.CLASS_MAPPING.get(cls_id, f"Defect_Type_{cls_id}")
                
                # 5. Monocular 3D Metric Calculations
                metrics = self.depth_estimator.estimate_metrics(
                    image_shape=(img_h, img_w),
                    bbox=[xmin, ymin, xmax, ymax],
                    depth_map=depth_map
                )

                # 6. Multi-Factor Severity & Priority Scoring
                severity_res = SeverityEngine.calculate_severity_and_priority(
                    damage_type=damage_type,
                    confidence=confidence,
                    metrics=metrics,
                    source_type=source_type,
                    cluster_count=len(boxes)
                )

                detection_entry = {
                    "damage_type": damage_type,
                    "confidence": round(confidence, 4),
                    "severity": severity_res["severity_level"],
                    "priority_score": severity_res["priority_score"],
                    "score_breakdown": severity_res["score_breakdown"],
                    "bbox": [round(xmin, 1), round(ymin, 1), round(xmax, 1), round(ymax, 1)],
                    "estimated_width_m": metrics["estimated_width_m"],
                    "estimated_length_m": metrics["estimated_length_m"],
                    "estimated_area_m2": metrics["estimated_area_m2"],
                    "estimated_depth_cm": metrics["estimated_depth_cm"],
                    "road_occupancy_pct": metrics["road_occupancy_pct"],
                    "latitude": latitude,
                    "longitude": longitude,
                    "location": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "road_name": location_meta["road_name"],
                        "city": location_meta["city"],
                        "district": location_meta["district"],
                        "state": location_meta["state"]
                    },
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                detections.append(detection_entry)

        # 7. Render Annotated Visualization Image
        annotated_img = self.preprocessor.draw_annotations(image_bgr, detections)
        inference_time_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "image_id": image_id,
            "source_type": source_type,
            "vehicle_id": vehicle_id,
            "citizen_id": citizen_id,
            "total_damages_found": len(detections),
            "inference_time_ms": inference_time_ms,
            "detections": detections,
            "annotated_image": annotated_img,
            "location_summary": location_meta
        }

pipeline = RoadVisionPipeline()

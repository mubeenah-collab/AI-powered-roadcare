import cv2
import json
import numpy as np
from ai.pipeline import pipeline

def create_synthetic_road_image() -> np.ndarray:
    h, w = 640, 640
    asphalt = np.full((h, w, 3), (70, 70, 75), dtype=np.uint8)
    noise = np.random.randint(-15, 15, (h, w, 3), dtype=np.int16)
    asphalt = np.clip(asphalt.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    cv2.line(asphalt, (w // 2, 0), (w // 2, h), (0, 215, 255), 10)
    cv2.ellipse(asphalt, (250, 400), (60, 40), 15, 0, 360, (25, 25, 30), -1)
    return asphalt

def run_test():
    print("=" * 60)
    print("   RoadVision AI Pipeline Integration Test")
    print("=" * 60)

    img = create_synthetic_road_image()
    sample_lat, sample_lng = 37.7749, -122.4194
    print(f"[*] Running inference with sample coordinates ({sample_lat}, {sample_lng})...")
    
    result = pipeline.process_image(
        image_bgr=img,
        latitude=sample_lat,
        longitude=sample_lng,
        source="Citizen"
    )

    print("\n[+] Structured Pipeline Output JSON (Matching Specification):")
    print(json.dumps(result, indent=2))
    print("=" * 60)

if __name__ == "__main__":
    run_test()

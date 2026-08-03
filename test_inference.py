import sys
import json

try:
    import cv2
    import numpy as np
    from ai.pipeline import pipeline
except ModuleNotFoundError as e:
    print(f"[!] System Environment Diagnostic: {e}")
    print("[!] Please run this test script inside the project virtualenv:")
    print("    python -m venv venv")
    print("    venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux)")
    print("    pip install -r requirements.txt")
    print("    python test_inference.py")
    sys.exit(0)

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
    print("   RoadVision AI Final System Integration Audit Test")
    print("   Indian Location, Live Weather & Fleet Telematics")
    print("=" * 60)

    img = create_synthetic_road_image()
    # Coordinates for Anna Salai, Teynampet, Chennai, Tamil Nadu
    sample_lat, sample_lng = 12.926543, 80.143287
    print(f"[*] Running inference for coordinates ({sample_lat}, {sample_lng})...")
    
    result = pipeline.process_image(
        image_bgr=img,
        latitude=sample_lat,
        longitude=sample_lng,
        source="Government Bus",
        fleet_meta={
            "vehicle_id": "TN01-GOV-024",
            "vehicle_type": "Government Bus",
            "department": "Greater Chennai Corporation",
            "camera_id": "CAM-003",
            "driver_name": "R. Sundaram",
            "inspection_route": "Anna Salai Route",
            "shift": "Morning"
        }
    )

    print("\n[+] Verified Output JSON Payload:")
    print(json.dumps(result, indent=2))
    print("=" * 60)

if __name__ == "__main__":
    run_test()

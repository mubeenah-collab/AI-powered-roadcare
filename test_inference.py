import cv2
import json
import numpy as np
from inference.pipeline import pipeline

def create_synthetic_road_image() -> np.ndarray:
    """Generates a synthetic asphalt road surface image with simulated defects for testing."""
    h, w = 640, 640
    # Dark grey asphalt texture
    asphalt = np.full((h, w, 3), (70, 70, 75), dtype=np.uint8)
    
    # Add random asphalt noise
    noise = np.random.randint(-15, 15, (h, w, 3), dtype=np.int16)
    asphalt = np.clip(asphalt.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Draw yellow lane divider line
    cv2.line(asphalt, (w // 2, 0), (w // 2, h), (0, 215, 255), 10)
    
    # Draw simulated pothole (dark irregular oval)
    cv2.ellipse(asphalt, (250, 400), (60, 40), 15, 0, 360, (25, 25, 30), -1)
    cv2.ellipse(asphalt, (250, 400), (65, 45), 15, 0, 360, (40, 40, 45), 3)
    
    # Draw simulated longitudinal crack
    pts = np.array([[450, 150], [455, 220], [448, 300], [460, 380]], np.int32)
    cv2.polylines(asphalt, [pts], False, (20, 20, 20), 4)
    
    return asphalt

def run_test():
    print("=" * 60)
    print("   RoadVision Core Pipeline Integration Test")
    print("=" * 60)

    # 1. Create sample synthetic road image
    img = create_synthetic_road_image()
    
    # 2. Run Inference Pipeline with sample GPS (e.g. San Francisco downtown coordinates)
    sample_lat, sample_lng = 37.7749, -122.4194
    print(f"[*] Running inference with sample coordinates ({sample_lat}, {sample_lng})...")
    
    res = pipeline.process_image(
        image_bgr=img,
        image_id="test_sample_001",
        source_type="government_fleet",
        latitude=sample_lat,
        longitude=sample_lng,
        vehicle_id="MUNI-BUS-42"
    )

    # 3. Print JSON Output
    printable_res = {
        "image_id": res["image_id"],
        "source_type": res["source_type"],
        "vehicle_id": res["vehicle_id"],
        "total_damages_found": res["total_damages_found"],
        "inference_time_ms": res["inference_time_ms"],
        "location": res["location_summary"],
        "detections": res["detections"]
    }
    
    print("\n[+] Structured Pipeline Output JSON:")
    print(json.dumps(printable_res, indent=2))

    # 4. Save Annotated Output Image
    annotated = res["annotated_image"]
    output_filename = "output_annotated.jpg"
    cv2.imwrite(output_filename, annotated)
    print(f"\n[+] Saved annotated result image to: {output_filename}")
    print("=" * 60)

if __name__ == "__main__":
    run_test()

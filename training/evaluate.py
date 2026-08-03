import torch
import argparse
from ultralytics import YOLO
from pathlib import Path

def evaluate_roadvision_model(weights_path: str = "models/best.pt", data_yaml: str = "dataset/rdd2022.yaml"):
    """
    Evaluates trained YOLO model on validation/test datasets.
    Prints Precision, Recall, mAP@50, and mAP@50-95 metrics per class.
    """
    if not Path(weights_path).exists():
        print(f"[!] Warning: Model weights '{weights_path}' not found. Falling back to 'yolov8n.pt'")
        weights_path = "yolov8n.pt"

    print("=" * 60)
    print(f"      RoadVision Model Evaluation Suite")
    print(f" Weights: {weights_path} | Dataset: {data_yaml}")
    print("=" * 60)

    model = YOLO(weights_path)
    metrics = model.val(data=data_yaml, split='val', imgsz=640, batch=16, conf=0.25, iou=0.5)

    print("\n" + "=" * 60)
    print("                EVALUATION RESULTS SUMMARY")
    print("=" * 60)
    print(f" Mean Precision (P)    : {metrics.box.mp:.4f}")
    print(f" Mean Recall (R)       : {metrics.box.mr:.4f}")
    print(f" mAP @ 0.50            : {metrics.box.map50:.4f}")
    print(f" mAP @ 0.50:0.95       : {metrics.box.map:.4f}")
    print("=" * 60)

    # Print Class Breakdown
    print("\nPer-Class Performance Breakdown:")
    print(f"{'Class Name':<22} | {'Precision':<10} | {'Recall':<10} | {'mAP50':<10} | {'mAP50-95':<10}")
    print("-" * 72)
    
    names = metrics.names
    for idx, class_name in names.items():
        if idx < len(metrics.box.p):
            p = metrics.box.p[idx]
            r = metrics.box.r[idx]
            ap50 = metrics.box.ap50[idx]
            ap = metrics.box.ap[idx]
            print(f"{class_name:<22} | {p:<10.4f} | {r:<10.4f} | {ap50:<10.4f} | {ap:<10.4f}")

    print("=" * 72)
    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate RoadVision YOLO Detector")
    parser.add_argument("--weights", type=str, default="models/best.pt", help="Path to weights file")
    parser.add_argument("--data", type=str, default="dataset/rdd2022.yaml", help="Path to rdd2022.yaml")
    args = parser.parse_args()

    evaluate_roadvision_model(args.weights, args.data)

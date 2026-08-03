import os
import torch
import argparse
from ultralytics import YOLO
from pathlib import Path

def train_roadvision_yolo(
    data_yaml: str = "dataset/rdd2022.yaml",
    model_version: str = "yolov8n.pt",
    epochs: int = 100,
    imgsz: int = 640,
    batch_size: int = 16,
    device: str = None
):
    """
    Complete Training Pipeline for RoadVision YOLO Detector.
    Configures Albumentations data augmentation, learning rate scheduling, and GPU acceleration.
    """
    if device is None:
        device = "0" if torch.cuda.is_available() else "cpu"
        
    print("=" * 60)
    print(f"       RoadVision YOLO Training Pipeline Launch")
    print(f" Device: {device.upper()} | PyTorch Version: {torch.__version__}")
    print(f" Configuration YAML: {data_yaml}")
    print(f" Epochs: {epochs} | Image Size: {imgsz} | Batch Size: {batch_size}")
    print("=" * 60)

    # Initialize pretrained model backbone
    model = YOLO(model_version)

    # Production Hyperparameter Recommendations for Road Damage Detection
    hyperparameters = {
        'data': data_yaml,
        'epochs': epochs,
        'imgsz': imgsz,
        'batch': batch_size,
        'device': device,
        'workers': 4,
        'patience': 15,           # Early stopping patience
        'save': True,
        'exist_ok': True,
        'pretrained': True,
        'optimizer': 'AdamW',
        'lr0': 0.001,             # Initial learning rate
        'lrf': 0.01,              # Final OneCycleLR factor
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'warmup_momentum': 0.8,
        
        # Advanced Data Augmentations tailored for Road Surface Textures
        'hsv_h': 0.015,           # Image HSV-Hue augmentation
        'hsv_s': 0.7,             # Image HSV-Saturation augmentation
        'hsv_v': 0.4,             # Image HSV-Value augmentation
        'degrees': 10.0,          # Image rotation (+/- deg)
        'translate': 0.1,         # Image translation (+/- fraction)
        'scale': 0.5,             # Image scale (+/- gain)
        'shear': 2.0,             # Image shear (+/- deg)
        'perspective': 0.0005,    # Image perspective (+/- fraction)
        'flipud': 0.0,            # Vertical flip (Disabled: road damage orientation matters)
        'fliplr': 0.5,            # Horizontal flip probability
        'mosaic': 1.0,            # Mosaic augmentation (combines 4 images)
        'mixup': 0.15,            # Mixup augmentation
        'copy_paste': 0.10,       # Segment Copy-Paste augmentation
        
        'project': 'runs/train',
        'name': 'roadvision_exp',
    }

    print("[*] Starting YOLO training loop...")
    results = model.train(**hyperparameters)
    print("[+] Training completed successfully!")

    # Copy best model weights to models/best.pt
    best_weights = Path(results.save_dir) / "weights" / "best.pt"
    target_weights = Path("models/best.pt")
    target_weights.parent.mkdir(parents=True, exist_ok=True)

    if best_weights.exists():
        import shutil
        shutil.copy(str(best_weights), str(target_weights))
        print(f"[+] Exported optimal trained model to: {target_weights.resolve()}")
    else:
        print("[!] Warning: best.pt not found in run results directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train RoadVision YOLO Object Detector")
    parser.add_argument("--data", type=str, default="dataset/rdd2022.yaml", help="Path to rdd2022.yaml")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Pretrained model checkpoint (yolov8n.pt / yolov11n.pt)")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Target image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    args = parser.parse_args()

    train_roadvision_yolo(args.data, args.model, args.epochs, args.imgsz, args.batch)

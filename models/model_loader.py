import os
import torch
from ultralytics import YOLO
from config.settings import settings

class ModelLoader:
    """
    Singleton Model Loader for YOLO object detector.
    Automatically handles GPU allocation, model weight resolution, and dynamic downloading.
    """
    _instance = None
    _model = None

    @classmethod
    def get_model(cls, weights_path: str = None) -> YOLO:
        if cls._model is not None:
            return cls._model

        device = "cuda" if torch.cuda.is_available() else "cpu"
        target_path = weights_path or settings.YOLO_MODEL_PATH
        
        print(f"[*] Initializing YOLO object detector on device [{device.upper()}]...")
        
        if not os.path.exists(target_path):
            print(f"[!] Custom weights '{target_path}' not found. Downloading baseline YOLO model ('yolov8n.pt')...")
            target_path = "yolov8n.pt"
            
        cls._model = YOLO(target_path)
        print(f"[+] YOLO Detector initialized from: {target_path}")
        return cls._model

model_loader = ModelLoader()

import os
import torch
from ultralytics import YOLO

class ModelLoader:
    _instance = None
    _model = None

    @classmethod
    def get_model(cls, weights_path: str = "models/best.pt") -> YOLO:
        if cls._model is not None:
            return cls._model

        device = "cuda" if torch.cuda.is_available() else "cpu"
        target_path = weights_path if os.path.exists(weights_path) else "yolov8n.pt"
            
        cls._model = YOLO(target_path)
        return cls._model

model_loader = ModelLoader()

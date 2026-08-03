import os
import xml.etree.ElementTree as ET
import shutil
import random
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

# RDD2022 to Standardized Class Mapping
RDD_CLASS_MAP = {
    "D00": 0,  # Longitudinal Crack
    "D10": 1,  # Transverse Crack
    "D20": 2,  # Alligator Crack
    "D40": 3,  # Pothole
    "D44": 4,  # Surface Wear / Bleeding
    "D50": 5   # Road Edge Failure / Rutting
}

CLASS_NAMES = [
    "Longitudinal Crack",
    "Transverse Crack",
    "Alligator Crack",
    "Pothole",
    "Surface Wear",
    "Road Edge Failure"
]

def convert_bbox_to_yolo(size: Tuple[int, int], box: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """
    Converts Pascal VOC box (xmin, ymin, xmax, ymax) to YOLO normalized format (x_center, y_center, width, height).
    """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    
    xmin, ymin, xmax, ymax = box
    x_center = (xmin + xmax) / 2.0 - 1
    y_center = (ymin + ymax) / 2.0 - 1
    w = xmax - xmin
    h = ymax - ymin
    
    x_center = max(0.0, min(1.0, x_center * dw))
    y_center = max(0.0, min(1.0, y_center * dh))
    w = max(0.0, min(1.0, w * dw))
    h = max(0.0, min(1.0, h * dh))
    
    return (x_center, y_center, w, h)

def parse_voc_xml(xml_path: str) -> Tuple[Tuple[int, int], List[Tuple[int, Tuple[float, float, float, float]]]]:
    """
    Parses a Pascal VOC XML file and extracts image dimensions and mapped YOLO annotations.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size_elem = root.find('size')
    if size_elem is None:
        return (0, 0), []
        
    width = int(size_elem.find('width').text)
    height = int(size_elem.find('height').text)
    
    annotations = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        if name in RDD_CLASS_MAP:
            class_id = RDD_CLASS_MAP[name]
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)
            
            yolo_box = convert_bbox_to_yolo((width, height), (xmin, ymin, xmax, ymax))
            annotations.append((class_id, yolo_box))
            
    return (width, height), annotations

def prepare_rdd2022_dataset(raw_dataset_dir: str, output_dir: str, train_ratio: float = 0.8, val_ratio: float = 0.1):
    """
    Converts raw RDD2022 VOC XML dataset into structured YOLO format directory with train/val/test splits.
    """
    print(f"[*] Processing RDD2022 dataset from: {raw_dataset_dir}")
    
    output_path = Path(output_dir)
    images_dir = output_path / "images"
    labels_dir = output_path / "labels"
    
    for split in ["train", "val", "test"]:
        (images_dir / split).mkdir(parents=True, exist_ok=True)
        (labels_dir / split).mkdir(parents=True, exist_ok=True)
        
    xml_files = list(Path(raw_dataset_dir).rglob("*.xml"))
    print(f"[*] Found {len(xml_files)} annotation files.")
    
    random.seed(42)
    random.shuffle(xml_files)
    
    total = len(xml_files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    counts = {"train": 0, "val": 0, "test": 0}
    
    for idx, xml_file in enumerate(xml_files):
        if idx < train_end:
            split = "train"
        elif idx < val_end:
            split = "val"
        else:
            split = "test"
            
        img_file = xml_file.with_suffix(".jpg")
        if not img_file.exists():
            img_file = xml_file.with_suffix(".png")
        if not img_file.exists():
            continue
            
        (img_w, img_h), annotations = parse_voc_xml(str(xml_file))
        if not annotations or img_w == 0 or img_h == 0:
            continue
            
        # Copy image file
        dst_img_path = images_dir / split / img_file.name
        shutil.copy(str(img_file), str(dst_img_path))
        
        # Write YOLO label TXT file
        txt_name = xml_file.stem + ".txt"
        dst_label_path = labels_dir / split / txt_name
        
        with open(dst_label_path, "w") as f:
            for class_id, (xc, yc, w, h) in annotations:
                f.write(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
                
        counts[split] += 1
        
    print(f"[+] Dataset Split Completed: Train={counts['train']}, Val={counts['val']}, Test={counts['test']}")
    
    # Generate rdd2022.yaml config file
    yaml_content = {
        'path': str(output_path.resolve()),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': {i: name for i, name in enumerate(CLASS_NAMES)}
    }
    
    yaml_path = output_path / "rdd2022.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False)
        
    print(f"[+] Generated YOLO configuration file: {yaml_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RDD2022 VOC XML to YOLO Converter")
    parser.add_argument("--input", type=str, default="data/raw_rdd2022", help="Path to raw dataset folder")
    parser.add_argument("--output", type=str, default="dataset", help="Output YOLO dataset folder")
    args = parser.parse_args()
    
    prepare_rdd2022_dataset(args.input, args.output)

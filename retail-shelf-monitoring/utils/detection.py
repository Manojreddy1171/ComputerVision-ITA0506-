# ============================================================
# Module 2 & 3: Product Detection and Recognition
# ============================================================
# This module wraps the Ultralytics YOLO model.
# It handles:
#   - Loading the model (custom best.pt or fallback YOLOv8n)
#   - Running inference on a preprocessed image
#   - Drawing bounding boxes & confidence labels
#   - Returning structured detection results
# ============================================================

import os
from pathlib import Path
import cv2
import numpy as np
from ultralytics import YOLO

# ─── Model Paths (Robust Pathlib resolution) ─────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CUSTOM_MODEL_PATH = PROJECT_ROOT / "models" / "best.pt"
FALLBACK_ROOT_PATH = PROJECT_ROOT / "yolov8n.pt"
FALLBACK_MODELS_PATH = PROJECT_ROOT / "models" / "yolov8n.pt"

# Standard retail classes expected in capstone training
DEFAULT_RETAIL_CLASSES = ["Coke", "Pepsi", "Sprite"]
# Relevant retail categories when operating in COCO Demo mode
DEMO_RETAIL_CLASSES = ["bottle", "cup", "can"]

# ─── Colour palette for bounding boxes ──────────────────────
PALETTE = [
    (52,  168, 83),   # green
    (66,  133, 244),  # blue
    (251, 188,   4),  # yellow
    (234,  67,  53),  # red
    (154,  52, 168),  # purple
    (0,   172, 193),  # cyan
    (255, 112,  67),  # orange
    (38,  166, 154),  # teal
    (121,  85, 72 ),  # brown
    (103, 58,  183),  # deep purple
]


def get_color(class_id: int) -> tuple:
    """Return a consistent BGR colour for the given class index."""
    return PALETTE[class_id % len(PALETTE)]


# ─── Model Loader ────────────────────────────────────────────

def load_model() -> YOLO:
    """
    Load the YOLO model.
      - If models/best.pt exists → load custom trained model (_source = 'custom')
      - Otherwise                → load YOLOv8n (pretrained COCO) as fallback (_source = 'demo')
    The model is loaded once and cached by Streamlit @st.cache_resource.
    """
    if CUSTOM_MODEL_PATH.exists():
        model = YOLO(str(CUSTOM_MODEL_PATH))
        model._source = "custom"
        model._source_name = "Custom Retail Model (models/best.pt)"
    elif FALLBACK_ROOT_PATH.exists():
        model = YOLO(str(FALLBACK_ROOT_PATH))
        model._source = "demo"
        model._source_name = "Demo Pretrained Model (yolov8n.pt COCO)"
    elif FALLBACK_MODELS_PATH.exists():
        model = YOLO(str(FALLBACK_MODELS_PATH))
        model._source = "demo"
        model._source_name = "Demo Pretrained Model (models/yolov8n.pt COCO)"
    else:
        # Fallback will trigger ultralytics download if file not found locally
        model = YOLO("yolov8n.pt")
        model._source = "demo"
        model._source_name = "Demo Pretrained Model (yolov8n.pt COCO)"

    return model


def get_expected_classes(model: YOLO) -> list[str]:
    """
    Return the list of expected product classes for condition tracking.
    
    - Custom Retail Mode (models/best.pt):
      Returns the trained custom classes (e.g. ['Coke', 'Pepsi', 'Sprite'] from model.names
      or data/dataset.yaml). If a brand like Sprite has 0 detections, it is accurately
      flagged as Out of Stock.
      
    - Demo Mode (yolov8n.pt COCO fallback):
      Returns standard COCO retail categories (e.g. ['bottle', 'cup']) so that non-retail
      classes (like train, zebra, airplane) are not flooded as 'Out of Stock', while still
      demonstrating stock availability logic (e.g., bottle Available, cup Out of Stock).
    """
    source = getattr(model, "_source", "demo")
    
    if source == "custom" and hasattr(model, "names") and model.names:
        return list(model.names.values())
    
    # In Demo Mode, track retail-relevant COCO items
    if source == "demo":
        return ["bottle", "cup"]
            
    return DEFAULT_RETAIL_CLASSES



# ─── Inference ───────────────────────────────────────────────

def run_detection(model: YOLO, img_bgr: np.ndarray, conf_threshold: float = 0.30) -> list[dict]:
    """
    Run YOLO inference on the BGR image.

    Returns a list of detection dictionaries, each with:
        {
            "class_id"   : int,
            "class_name" : str,
            "confidence" : float,   # 0.0 – 1.0
            "bbox"       : (x1, y1, x2, y2)  # pixel coords
        }
    """
    if img_bgr is None:
        return []

    results = model.predict(
        source=img_bgr,
        conf=conf_threshold,
        verbose=False
    )

    detections = []
    if results and len(results) > 0 and results[0].boxes is not None:
        boxes = results[0].boxes
        names = model.names  # dict {id: name}
        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, coords)
            detections.append({
                "class_id"   : class_id,
                "class_name" : names.get(class_id, f"Class {class_id}"),
                "confidence" : round(confidence, 4),
                "bbox"       : (x1, y1, x2, y2),
            })

    return detections


# ─── Annotated Image ─────────────────────────────────────────

def draw_detections(img_bgr: np.ndarray, detections: list[dict]) -> np.ndarray:
    """
    Draw bounding boxes and confidence labels on a copy of the
    image. Returns the annotated BGR image.
    """
    if img_bgr is None:
        return np.zeros((100, 100, 3), dtype=np.uint8)
        
    annotated = img_bgr.copy()

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        cid = det["class_id"]
        label = f"{det['class_name']} {det['confidence']*100:.0f}%"
        color = get_color(cid)

        # Bounding box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

        # Label background
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        label_y = max(y1 - 10, th + 6)
        cv2.rectangle(
            annotated,
            (x1, label_y - th - 6),
            (x1 + tw + 8, label_y + 2),
            color,
            -1
        )
        # Label text
        cv2.putText(
            annotated, label,
            (x1 + 4, label_y - 2),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (255, 255, 255), 1, cv2.LINE_AA
        )

    return annotated


# ─── Aggregation helpers ─────────────────────────────────────

def aggregate_detections(detections: list[dict]) -> dict:
    """
    Aggregate per-detection results into per-class summaries.

    Returns:
        {
            "ClassName": {
                "count"      : int,
                "avg_conf"   : float,  # average confidence 0-1
                "class_id"   : int,
            },
            ...
        }
    """
    summary = {}
    for det in detections:
        name = det["class_name"]
        if name not in summary:
            summary[name] = {
                "count"    : 0,
                "conf_sum" : 0.0,
                "class_id" : det["class_id"],
            }
        summary[name]["count"] += 1
        summary[name]["conf_sum"] += det["confidence"]

    result = {}
    for name, data in summary.items():
        count = data["count"]
        result[name] = {
            "count"    : count,
            "avg_conf" : round(data["conf_sum"] / count, 4) if count > 0 else 0.0,
            "class_id" : data["class_id"],
        }
    return result


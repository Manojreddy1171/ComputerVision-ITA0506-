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


BRAND_COLORS = {
    "Coke": (34, 34, 220),    # Vibrant Red (BGR)
    "Pepsi": (220, 110, 24),  # Royal Blue (BGR)
    "Sprite": (40, 180, 48),  # Vibrant Green (BGR)
}


def get_color(class_id: int, class_name: str = "") -> tuple:
    """Return a consistent BGR colour for the given class index or brand name."""
    if class_name in BRAND_COLORS:
        return BRAND_COLORS[class_name]
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



# ─── NMS & Brand Recognition Refinement ───────────────────────

def compute_iou(b1: tuple, b2: tuple) -> float:
    """Compute Intersection-over-Union (IoU) between two bounding boxes (x1, y1, x2, y2)."""
    x1, y1 = max(b1[0], b2[0]), max(b1[1], b2[1])
    x2, y2 = min(b1[2], b2[2]), min(b1[3], b2[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    a1 = max(0, b1[2] - b1[0]) * max(0, b1[3] - b1[1])
    a2 = max(0, b2[2] - b2[0]) * max(0, b2[3] - b2[1])
    union = a1 + a2 - inter
    return inter / union if union > 0 else 0.0


def refine_brand_by_color(crop_bgr: np.ndarray, predicted_class: str, class_names: dict) -> tuple[int, str]:
    """
    Module 3: Product Recognition Refinement via Computer Vision Color Analysis.
    Examines the chromatic profile of detected bottles/cans in HSV color space
    to verify and refine brand classification (Coke=Red, Pepsi=Blue, Sprite=Green),
    preventing classification bias and cross-class duplicate counts.
    """
    name_to_id = {v: k for k, v in class_names.items()} if isinstance(class_names, dict) else {}

    if crop_bgr is None or crop_bgr.size == 0:
        return name_to_id.get(predicted_class, 0), predicted_class

    hsv = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    # Focus on colorful saturated pixels (bottle body / label)
    mask = (s > 40) & (v > 30) & (v < 250)
    if np.sum(mask) < 20:
        return name_to_id.get(predicted_class, 0), predicted_class

    val_h = h[mask]
    total_colored = len(val_h)

    red_px   = np.sum((val_h <= 14) | (val_h >= 165))
    green_px = np.sum((val_h >= 35) & (val_h <= 85))
    blue_px  = np.sum((val_h >= 90) & (val_h <= 140))

    r_ratio = red_px / total_colored
    g_ratio = green_px / total_colored
    b_ratio = blue_px / total_colored

    # Check if a signature brand color is distinctly dominant
    if b_ratio > 0.28 and b_ratio > r_ratio * 1.25 and b_ratio > g_ratio * 1.25:
        target = "Pepsi"
    elif g_ratio > 0.28 and g_ratio > r_ratio * 1.25 and g_ratio > b_ratio * 1.25:
        target = "Sprite"
    elif r_ratio > 0.28 and r_ratio > b_ratio * 1.25 and r_ratio > g_ratio * 1.25:
        target = "Coke"
    else:
        target = predicted_class

    return name_to_id.get(target, 0), target


# ─── Inference ───────────────────────────────────────────────

def run_detection(model: YOLO, img_bgr: np.ndarray, conf_threshold: float = 0.30) -> list[dict]:
    """
    Run YOLO inference on the BGR image.
    Enforces class-agnostic NMS and post-processing IoU deduplication
    to prevent duplicate detections on the same physical item.
    Refines brand recognition using Computer Vision color analysis.

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
        iou=0.45,
        agnostic_nms=True,
        verbose=False
    )

    raw_detections = []
    if results and len(results) > 0 and results[0].boxes is not None:
        boxes = results[0].boxes
        names = model.names  # dict {id: name}
        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, coords)
            raw_detections.append({
                "class_id"   : class_id,
                "class_name" : names.get(class_id, f"Class {class_id}"),
                "confidence" : round(confidence, 4),
                "bbox"       : (x1, y1, x2, y2),
            })

    # Sort descending by confidence
    raw_detections.sort(key=lambda d: d["confidence"], reverse=True)

    # Class-agnostic IoU deduplication: suppresses overlapping boxes on the same bottle
    deduped = []
    for det in raw_detections:
        if any(compute_iou(det["bbox"], kept["bbox"]) > 0.40 for kept in deduped):
            continue
        deduped.append(det)

    # Brand recognition refinement via Computer Vision color verification
    detections = []
    names = getattr(model, "names", {0: "Coke", 1: "Pepsi", 2: "Sprite"})
    img_h, img_w = img_bgr.shape[:2]
    for det in deduped:
        x1, y1, x2, y2 = det["bbox"]
        # Inset crop by 10% to analyze inner product body
        pw = int((x2 - x1) * 0.10)
        ph = int((y2 - y1) * 0.10)
        cy1, cy2 = max(0, y1 + ph), min(img_h, y2 - ph)
        cx1, cx2 = max(0, x1 + pw), min(img_w, x2 - pw)
        crop = img_bgr[cy1:cy2, cx1:cx2]

        cid, cname = refine_brand_by_color(crop, det["class_name"], names)
        det["class_id"] = cid
        det["class_name"] = cname
        detections.append(det)

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
        cname = det["class_name"]
        label = f"{cname} {det['confidence']*100:.0f}%"
        color = get_color(cid, cname)

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


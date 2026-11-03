# ============================================================
# Module 1: Shelf Image Acquisition & Preprocessing Utilities
# ============================================================
# This module handles loading, validating, and preprocessing
# shelf images using OpenCV before feeding them into the
# YOLO detection pipeline.
# ============================================================

import cv2
import numpy as np
from PIL import Image
import os

# ─── Configuration ───────────────────────────────────────────
MAX_IMAGE_WIDTH  = 1280   # Maximum allowed width (pixels)
MAX_IMAGE_HEIGHT = 1280   # Maximum allowed height (pixels)
ALLOWED_FORMATS  = {"jpg", "jpeg", "png"}


def validate_image_format(filename: str) -> bool:
    """Return True if the file extension is in ALLOWED_FORMATS."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].strip().lower()
    return ext in ALLOWED_FORMATS


def load_image_from_bytes(file_bytes: bytes) -> np.ndarray:
    """
    Convert raw file bytes (from Streamlit uploader) into an
    OpenCV BGR image array. Raises ValueError on empty or corrupt data.
    """
    if not file_bytes:
        raise ValueError("Uploaded image file is empty (0 bytes).")
    
    nparr = np.frombuffer(file_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img_bgr is None:
        raise ValueError("Failed to decode image. The file may be corrupted or in an unsupported format.")
    
    return img_bgr


def resize_if_needed(img_bgr: np.ndarray, max_w: int = MAX_IMAGE_WIDTH, max_h: int = MAX_IMAGE_HEIGHT) -> np.ndarray:
    """
    Resize the image proportionally so that neither dimension
    exceeds max_w / max_h. Smaller images are returned unchanged.
    """
    if img_bgr is None:
        raise ValueError("Cannot resize None image.")
        
    h, w = img_bgr.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)
    if scale < 1.0:
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        img_bgr = cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img_bgr


def preprocess_image(img_bgr: np.ndarray) -> np.ndarray:
    """
    Apply standard OpenCV preprocessing steps:
      1. Mild Gaussian blur (3x3) to reduce sensor noise
      2. CLAHE (Contrast Limited Adaptive Histogram Equalisation) on the
         L-channel (improves contrast in unevenly lit retail shelves)
    Returns the preprocessed BGR image (same dtype, same shape).
    """
    if img_bgr is None:
        raise ValueError("Cannot preprocess None image.")
        
    # --- Step 1: Mild noise reduction -------------------------
    blurred = cv2.GaussianBlur(img_bgr, (3, 3), 0)

    # --- Step 2: Adaptive contrast enhancement ----------------
    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)
    lab_eq = cv2.merge([l_eq, a, b])
    enhanced = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

    return enhanced


def bgr_to_rgb_pil(img_bgr: np.ndarray) -> Image.Image:
    """Convert an OpenCV BGR array to a PIL RGB Image for display."""
    if img_bgr is None:
        raise ValueError("Cannot convert None image to PIL.")
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)


def get_image_info(img_bgr: np.ndarray, filename: str, file_size_bytes: int = None) -> dict:
    """
    Return a dictionary with basic image metadata.
    Used by Module 1 (Shelf Image Acquisition) to show users
    information about their uploaded image.
    """
    if img_bgr is None:
        raise ValueError("Cannot get info from None image.")
        
    h, w, c = img_bgr.shape
    size_kb = round(file_size_bytes / 1024, 1) if file_size_bytes else round((w * h * c) / 1024, 1)
    
    return {
        "filename" : os.path.basename(filename),
        "width"    : w,
        "height"   : h,
        "channels" : c,
        "size_kb"  : size_kb,
    }


def full_pipeline(file_bytes: bytes, filename: str):
    """
    Convenience function that runs the complete Module 1 pipeline:
      load → resize → preprocess
    Returns (preprocessed_bgr, image_info_dict).
    """
    img_bgr = load_image_from_bytes(file_bytes)
    img_bgr = resize_if_needed(img_bgr)
    processed = preprocess_image(img_bgr)
    info = get_image_info(processed, filename, file_size_bytes=len(file_bytes))
    return processed, info


# ============================================================
#  YOLO Model Training Script
#  Intelligent Retail Shelf Monitoring System
# ============================================================
#  Run this script (or the equivalent Colab notebook) to train
#  a custom YOLOv8 model on your retail product dataset.
#
#  Usage:
#      python train_model.py
#
#  After training, best.pt is automatically verified and copied
#  to the models/ folder in the project root.
# ============================================================

from pathlib import Path
import shutil
import sys
from ultralytics import YOLO

# ─── Robust Path Configuration ───────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_YAML    = PROJECT_ROOT / "data" / "dataset.yaml"
MODELS_DIR   = PROJECT_ROOT / "models"
DEST_BEST_PT = MODELS_DIR / "best.pt"

# Base model to fine-tune.
# yolov8n = nano (fastest, ideal for student capstone).
# Alternative: yolo11n.pt
BASE_MODEL   = PROJECT_ROOT / "yolov8n.pt" if (PROJECT_ROOT / "yolov8n.pt").exists() else "yolov8n.pt"

# Training hyper-parameters
EPOCHS       = 50        # Recommended 50 to 100 for solid mAP
IMAGE_SIZE   = 640       # Standard YOLO resolution
BATCH_SIZE   = 16        # Reduce to 8 if training on low-memory GPU or CPU
RUNS_DIR     = PROJECT_ROOT / "runs" / "detect"
EXPERIMENT   = "retail_shelf"


def train():
    """Fine-tune YOLO model on custom retail shelf dataset."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_YAML.exists():
        print(f"[ERROR] Dataset configuration not found at: {DATA_YAML}")
        print("Please verify data/dataset.yaml before launching training.")
        sys.exit(1)

    print(f"[INFO] Dataset YAML : {DATA_YAML}")
    print(f"[INFO] Base Model   : {BASE_MODEL}")
    print(f"[INFO] Epochs       : {EPOCHS}")
    print(f"[INFO] Image Size   : {IMAGE_SIZE}x{IMAGE_SIZE}")
    print(f"[INFO] Starting training pipeline...")

    model = YOLO(str(BASE_MODEL))

    results = model.train(
        data     = str(DATA_YAML),
        epochs   = EPOCHS,
        imgsz    = IMAGE_SIZE,
        batch    = BATCH_SIZE,
        project  = str(RUNS_DIR),
        name     = EXPERIMENT,
        exist_ok = True,      # overwrite existing experiment run
        patience = 15,        # early stopping patience
        workers  = 2,         # safer on Windows to avoid multiprocessing deadlocks
        verbose  = True,
    )

    trained_best_pt = RUNS_DIR / EXPERIMENT / "weights" / "best.pt"
    if trained_best_pt.exists():
        shutil.copy2(trained_best_pt, DEST_BEST_PT)
        print(f"\n[✅] Training complete!")
        print(f"     Trained weights saved at : {trained_best_pt}")
        print(f"     Copied automatically to  : {DEST_BEST_PT}")
        print(f"\n     You can now launch the web app with:")
        print(f"     streamlit run app.py")
    else:
        print(f"[WARNING] Expected best weights at {trained_best_pt} was not found.")

    return results


def validate():
    """Evaluate trained model on the validation split."""
    target_weights = DEST_BEST_PT if DEST_BEST_PT.exists() else (RUNS_DIR / EXPERIMENT / "weights" / "best.pt")
    if not target_weights.exists():
        print("[INFO] No trained model weights found yet to validate.")
        return

    print(f"\n[INFO] Validating model performance: {target_weights}")
    model   = YOLO(str(target_weights))
    metrics = model.val(data=str(DATA_YAML), imgsz=IMAGE_SIZE, verbose=True)

    print("\n─── Validation Performance Metrics ────────────")
    print(f"  mAP @ 0.50       : {metrics.box.map50:.4f}")
    print(f"  mAP @ 0.50:0.95  : {metrics.box.map:.4f}")
    print(f"  Mean Precision   : {metrics.box.mp:.4f}")
    print(f"  Mean Recall      : {metrics.box.mr:.4f}")
    print("───────────────────────────────────────────────")


if __name__ == "__main__":
    train()
    validate()


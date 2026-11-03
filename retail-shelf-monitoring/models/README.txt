Place your trained YOLOv8 model here as  best.pt

How to get best.pt
==================

Option A – Train your own model
---------------------------------
1. Prepare your dataset (see data/dataset.yaml for folder structure).
2. Annotate images with Roboflow or LabelImg in YOLOv8 format.
3. Run:  python train_model.py
4. Copy  runs/detect/retail_shelf/weights/best.pt  into this folder.

Option B – Use a Roboflow pretrained model
-------------------------------------------
1. Visit https://universe.roboflow.com and search for a retail / beverage dataset.
2. Download the model weights (best.pt).
3. Place the file here.

Option C – Demo mode (no training needed)
------------------------------------------
If best.pt is absent the app automatically falls back to the pretrained
YOLOv8n (COCO) model, which detects 80 common object classes.
This is useful for live demonstrations without a custom-trained model.

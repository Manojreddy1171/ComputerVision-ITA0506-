# 🛒 Intelligent Retail Shelf Monitoring and Product Availability Detection System

> **Computer Vision Capstone Project — ITA 0506**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-blueviolet?style=flat)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-Headless-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)

---

## 🌐 Web Application

The application runs locally with Streamlit. The previously listed public
Streamlit URL is currently unavailable, so a working public deployment cannot
be verified.

* **GitHub Repository:** [Manojreddy1171/ComputerVision-ITA0506-](https://github.com/Manojreddy1171/ComputerVision-ITA0506-)
* **Run locally:** Follow the Local Installation & Setup instructions below.

---

## 📖 Project Overview

This project is an end-to-end Computer Vision system that automates the monitoring of retail beverage shelves. Using deep-learning object detection (YOLOv8) and OpenCV image processing, the system identifies on-shelf products (`Coke`, `Pepsi`, `Sprite`), quantifies available stock, and generates real-time inventory alerts to prevent stockouts.

The application answers three operational questions for retail managers:
1. **What products are currently placed on the shelf?**
2. **How many items of each product class are available?**
3. **Which products require immediate replenishment?**

---

## 📦 Five Mandatory Modules

| # | Module | Implementation Description |
|:---:|:---|:---|
| **01** | **Shelf Image Acquisition** | Upload validation (JPG/PNG), dynamic resizing (max 1280px), noise reduction (Gaussian blur 3x3), and CLAHE adaptive contrast equalisation via OpenCV. |
| **02** | **Product Segmentation / Detection** | Ultralytics YOLOv8 inference identifying bounding boxes ($x_1, y_1, x_2, y_2$), confidence scores, and class labels. |
| **03** | **Product Recognition** | Multi-class product classification categorising detected items into target brand classes (`Coke`, `Pepsi`, `Sprite`). |
| **04** | **Shelf Condition Analysis** | Heuristic inventory status classification: **Available** ($\ge 5$ items), **Low Stock** ($1-4$ items), and **Out of Stock** ($0$ items). |
| **05** | **Retail Monitoring Dashboard** | Executive analytics interface featuring SaaS KPI metric cards, interactive Plotly availability bar charts, and restock alert tables. |

---

## 🛠️ Technology Stack

* **Language:** Python 3.10+
* **Framework:** Streamlit (Modern Web UI & Session State Navigation)
* **Computer Vision:** OpenCV (`opencv-python-headless`)
* **Deep Learning:** Ultralytics YOLOv8 (`models/best.pt`)
* **Visualisation:** Plotly Graph Objects & Pillow
* **Data Processing:** Pandas, NumPy, PyYAML

---

## 📁 Repository Structure

```
intelligent-retail-shelf-monitoring/
│
├── .streamlit/
│   └── config.toml               # Streamlit theme & headless server config
│
├── assets/
│   └── styles.css                # Premium modern AI SaaS CSS styling
│
├── data/
│   ├── dataset.yaml              # YOLOv8 dataset configuration
│   └── sample_images/            # High-resolution test shelf images
│
├── models/
│   ├── best.pt                   # Trained custom YOLOv8 model (~6.2 MB)
│   └── README.txt                # Model documentation and class dictionary
│
├── pages/
│   ├── home.py                   # Split-hero landing page & workflow pipeline
│   ├── shelf_analysis.py         # 6-step AI shelf analysis pipeline
│   ├── dashboard.py              # SaaS retail analytics & inventory tables
│   └── about.py                  # Academic specifications & architecture
│
├── utils/
│   ├── image_processing.py       # Module 1: OpenCV acquisition & CLAHE
│   ├── detection.py              # Modules 2 & 3: YOLO detection & recognition
│   └── shelf_analysis.py         # Module 4: Stock condition & replenishment logic
│
├── app.py                        # Main application orchestrator & safe router
├── requirements.txt              # Cloud-deployment optimized dependencies
├── train_model.py                # Local training & validation script
├── train_colab.ipynb             # Google Colab cloud training notebook
├── .gitignore                    # Git tracking rules
└── README.md                     # Capstone documentation
```

---

## 💻 Local Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Manojreddy1171/ComputerVision-ITA0506-.git
cd ComputerVision-ITA0506-
cd retail-shelf-monitoring
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## ☁️ Deployment: Streamlit Community Cloud

This project is designed for **Streamlit Community Cloud** with `opencv-python-headless` and platform-agnostic `pathlib` references.

### Deployment Steps:
1. Push the [ComputerVision-ITA0506- repository](https://github.com/Manojreddy1171/ComputerVision-ITA0506-) to GitHub.
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click **"New app"**.
4. Select repository `Manojreddy1171/ComputerVision-ITA0506-`.
5. Set **Branch:** `main` and **Main file path:** `retail-shelf-monitoring/app.py`.
6. Choose an available app subdomain.
7. Click **"Deploy"**.

---

## 🏋️ Model Training & Dataset

The custom YOLOv8 detection model is trained to recognize 3 primary beverage classes:
* `Class 0`: **Coke**
* `Class 1`: **Pepsi**
* `Class 2`: **Sprite**

### Training on Google Colab (Free GPU)
1. Open [`train_colab.ipynb`](train_colab.ipynb) in Google Colab.
2. Select runtime: **T4 GPU**.
3. Run the notebook cells to train YOLOv8 for 50 epochs.
4. Download the generated `runs/detect/retail_shelf/weights/best.pt` and place it in the `models/` directory.

---

## 📊 Business Rules & Stock Thresholds

Stock levels are classified according to configurable threshold values in `utils/shelf_analysis.py`:

| Status | Condition | Action Required | Badge |
|:---|:---|:---|:---:|
| **Available** | $\text{Count} \ge 5$ | Adequate inventory. No action needed. | `● Available` |
| **Low Stock** | $1 \le \text{Count} \le 4$ | Reorder recommended to prevent stockout. | `▲ Low Stock` |
| **Out of Stock** | $\text{Count} = 0$ | Depleted. Immediate shelf restock needed. | `■ Out of Stock` |

---

## 👨‍💻 Capstone Information

* **Subject:** Computer Vision — Capstone Project (ITA 0506)
* **Domain:** Smart Retail / AI Automation / Inventory Monitoring
* **Target Classes:** Coke, Pepsi, Sprite
* **License:** Academic Use Only

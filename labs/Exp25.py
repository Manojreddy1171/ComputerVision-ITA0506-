import cv2
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from resources.display_utils import show_small
import numpy as np
from tkinter import Tk, filedialog

Tk().withdraw()
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)

if not file_path:
    print("No image selected!")
    exit()

img = cv2.imread(file_path)
if img is None:
    print("Error: Unable to load image!")
    exit()

height, width = img.shape[:2]
mask = np.zeros_like(img)
mask[:height // 2, :width // 2] = 255
result = cv2.bitwise_and(img, mask)

show_small("Original Image", img)
show_small("Bitwise AND Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

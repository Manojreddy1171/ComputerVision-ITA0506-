import cv2
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from resources.display_utils import show_small
from tkinter import Tk, filedialog

# Hide Tkinter window
Tk().withdraw()

# Select image
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)

# Check if image selected
if not file_path:
    print("No image selected!")
    exit()

# Read image
img = cv2.imread(file_path)

if img is None:
    print("Error: Unable to load image!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Histogram Equalization
equalized = cv2.equalizeHist(gray)

# Display images
show_small("Original Grayscale Image", gray)
show_small("Histogram Equalized Image", equalized)

cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from resources.display_utils import show_small
from tkinter import Tk, filedialog

Tk().withdraw()
file_path1 = filedialog.askopenfilename(
    title="Select First Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path1:
    print("No first image selected!")
    exit()

file_path2 = filedialog.askopenfilename(
    title="Select Second Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path2:
    print("No second image selected!")
    exit()

img1 = cv2.imread(file_path1)
img2 = cv2.imread(file_path2)
if img1 is None or img2 is None:
    print("Error: Unable to load images!")
    exit()

if img1.shape != img2.shape:
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

subtracted = cv2.absdiff(img1, img2)

show_small("Image 1", img1)
show_small("Image 2", img2)
show_small("Image Subtraction", subtracted)
cv2.waitKey(0)
cv2.destroyAllWindows()

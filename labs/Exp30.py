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
    title="Select Background Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path1:
    print("No background image selected!")
    exit()

file_path2 = filedialog.askopenfilename(
    title="Select Current Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path2:
    print("No current image selected!")
    exit()

background = cv2.imread(file_path1)
current = cv2.imread(file_path2)
if background is None or current is None:
    print("Error: Unable to load images!")
    exit()

if background.shape != current.shape:
    current = cv2.resize(current, (background.shape[1], background.shape[0]))

fgmask = cv2.absdiff(background, current)
fgmask = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)
_, fgmask = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)

show_small("Background Image", background)
show_small("Current Image", current)
show_small("Background Subtraction Mask", fgmask)
cv2.waitKey(0)
cv2.destroyAllWindows()

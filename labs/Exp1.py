import cv2
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from resources.display_utils import show_small

img = cv2.imread(str(ROOT.parent / "images" / "flower.jpg"))

if img is None:
    print("Image not found!")
else:
    # Show original image
    show_small("Original Image", img)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display grayscale image
    show_small("Gray Image", gray)

    # Save grayscale image
    cv2.imwrite("gray_flower.jpg", gray)

    print("Image converted successfully!")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

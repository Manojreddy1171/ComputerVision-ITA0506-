import cv2
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from resources.display_utils import show_small

# Read the image
img = cv2.imread("flower.jpg")

# Check whether the image is loaded
if img is None:
    print("Image not found!")
else:
    # Display the original image
    show_small("Original Image", img)

    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(img, (15, 15), 0)

    # Display the blurred image
    show_small("Gaussian Blur Image", blur)

    # Save the blurred image
    cv2.imwrite("flower.jpg", blur)

    print("Gaussian Blur applied successfully!")
    print("Blurred image saved as flower.jpg")

    # Wait until a key is pressed
    cv2.waitKey(0)

    # Close all windows
    cv2.destroyAllWindows()

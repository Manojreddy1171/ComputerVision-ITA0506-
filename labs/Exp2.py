import cv2
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from resources.display_utils import show_small

input_path = PROJECT_ROOT / "images" / "flower.jpg"
output_path = PROJECT_ROOT / "images" / "flower_blurred.jpg"
img = cv2.imread(str(input_path))

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
    if not cv2.imwrite(str(output_path), blur):
        raise OSError(f"Unable to save blurred image: {output_path}")

    print("Gaussian Blur applied successfully!")
    print(f"Blurred image saved as {output_path}")

    # Wait until a key is pressed
    cv2.waitKey(0)

    # Close all windows
    cv2.destroyAllWindows()

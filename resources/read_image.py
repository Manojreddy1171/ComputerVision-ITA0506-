from pathlib import Path

import cv2

image_path = Path(__file__).with_name("image.jpg")
img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

if img is None:
    print(f"Could not load the image: {image_path}")
    print("Place image.jpg in the same folder as this script.")
else:
    print("Image loaded successfully")
    print("Image size:", img.shape)
    cv2.imshow("My Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import cv2
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

noise = np.random.normal(0, 25, img.shape).astype(np.uint8)
noisy = cv2.add(img, noise)

cv2.imshow("Original Image", img)
cv2.imshow("Gaussian Noise Image", noisy)
cv2.waitKey(0)
cv2.destroyAllWindows()

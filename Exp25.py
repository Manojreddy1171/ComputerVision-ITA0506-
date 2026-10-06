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

height, width = img.shape[:2]
mask = np.zeros_like(img)
mask[:height // 2, :width // 2] = 255
result = cv2.bitwise_and(img, mask)

cv2.imshow("Original Image", img)
cv2.imshow("Bitwise AND Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

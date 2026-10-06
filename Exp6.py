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

kernel = np.ones((5, 5), np.uint8)
eroded = cv2.erode(img, kernel, iterations=1)

cv2.imshow("Original Image", img)
cv2.imshow("Eroded Image", eroded)
cv2.waitKey(0)
cv2.destroyAllWindows()

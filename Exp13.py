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

rows, cols = img.shape[:2]
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
matrix = cv2.getAffineTransform(pts1, pts2)
result = cv2.warpAffine(img, matrix, (cols, rows))

cv2.imshow("Original Image", img)
cv2.imshow("Affine Transformation", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

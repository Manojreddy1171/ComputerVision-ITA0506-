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
trans_mat = np.float32([[1, 0, 50], [0, 1, 30]])
translated = cv2.warpAffine(img, trans_mat, (cols, rows))

cv2.imshow("Original Image", img)
cv2.imshow("Translated Image", translated)
cv2.waitKey(0)
cv2.destroyAllWindows()

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

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 50, 50])
upper = np.array([255, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("Original Image", img)
cv2.imshow("Color Mask", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
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

rotated = cv2.rotate(img, cv2.ROTATE_180)

cv2.imshow("Original Image", img)
cv2.imshow("180 Degree Rotated Image", rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()

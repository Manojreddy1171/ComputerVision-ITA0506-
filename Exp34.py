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

flipped = cv2.flip(img, 1)

cv2.imshow("Original Image", img)
cv2.imshow("Flipped Image", flipped)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
from tkinter import Tk, filedialog

Tk().withdraw()
file_path1 = filedialog.askopenfilename(
    title="Select First Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path1:
    print("No first image selected!")
    exit()

file_path2 = filedialog.askopenfilename(
    title="Select Second Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path2:
    print("No second image selected!")
    exit()

img1 = cv2.imread(file_path1)
img2 = cv2.imread(file_path2)
if img1 is None or img2 is None:
    print("Error: Unable to load one or both images!")
    exit()

if img1.shape != img2.shape:
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

blended = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)
cv2.imshow("Blended Image", blended)
cv2.waitKey(0)
cv2.destroyAllWindows()

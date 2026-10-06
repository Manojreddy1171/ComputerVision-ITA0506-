import cv2
from tkinter import Tk, filedialog

Tk().withdraw()
file_path1 = filedialog.askopenfilename(
    title="Select Background Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path1:
    print("No background image selected!")
    exit()

file_path2 = filedialog.askopenfilename(
    title="Select Current Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path2:
    print("No current image selected!")
    exit()

background = cv2.imread(file_path1)
current = cv2.imread(file_path2)
if background is None or current is None:
    print("Error: Unable to load images!")
    exit()

if background.shape != current.shape:
    current = cv2.resize(current, (background.shape[1], background.shape[0]))

fgmask = cv2.absdiff(background, current)
fgmask = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)
_, fgmask = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)

cv2.imshow("Background Image", background)
cv2.imshow("Current Image", current)
cv2.imshow("Background Subtraction Mask", fgmask)
cv2.waitKey(0)
cv2.destroyAllWindows()

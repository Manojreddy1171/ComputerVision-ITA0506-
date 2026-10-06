import cv2
from tkinter import Tk, filedialog

Tk().withdraw()
file_path = filedialog.askopenfilename(
    title="Select a Main Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not file_path:
    print("No main image selected!")
    exit()

template_path = filedialog.askopenfilename(
    title="Select a Template Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)
if not template_path:
    print("No template image selected!")
    exit()

img = cv2.imread(file_path)
template = cv2.imread(template_path)
if img is None or template is None:
    print("Error: Unable to load images!")
    exit()

result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
_, _, _, max_loc = cv2.minMaxLoc(result)

h, w = template.shape[:2]
cv2.rectangle(img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)

cv2.imshow("Main Image", img)
cv2.imshow("Template Match", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

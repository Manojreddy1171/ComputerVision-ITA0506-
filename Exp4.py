import cv2
from tkinter import Tk, filedialog

# Hide Tkinter window
Tk().withdraw()

# Select image
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)

# Check if image selected
if not file_path:
    print("No image selected!")
    exit()

# Read image
img = cv2.imread(file_path)

if img is None:
    print("Error: Unable to load image!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Histogram Equalization
equalized = cv2.equalizeHist(gray)

# Display images
cv2.imshow("Original Grayscale Image", gray)
cv2.imshow("Histogram Equalized Image", equalized)

cv2.waitKey(0)
cv2.destroyAllWindows()
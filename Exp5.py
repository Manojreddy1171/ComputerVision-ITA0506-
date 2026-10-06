import cv2
from tkinter import Tk, filedialog
from matplotlib import pyplot as plt

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

# Display original image
cv2.imshow("Original Image", img)

# Plot histogram for B, G, R channels
colors = ('b', 'g', 'r')

plt.figure("Color Histogram")

for i, color in enumerate(colors):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(hist, color=color)
    plt.xlim([0, 256])

plt.title("Histogram of Color Image")
plt.xlabel("Pixel Intensity")
plt.ylabel("Number of Pixels")

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
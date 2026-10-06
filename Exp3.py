import cv2
from tkinter import Tk, filedialog

# Hide the Tkinter window
Tk().withdraw()

# Open a file dialog to choose an image
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)

# Check if a file was selected
if not file_path:
    print("No image selected!")
    exit()

# Read the image
img = cv2.imread(file_path)

# Check if the image was loaded
if img is None:
    print("Error: Unable to load the image!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny Edge Detection
edges = cv2.Canny(gray, 100, 200)

# Display images
cv2.imshow("Original Image", img)
cv2.imshow("Canny Edge Detection", edges)

# Wait until a key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
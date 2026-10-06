import cv2

# Read the image
img = cv2.imread("flower.jpg")

# Check whether the image is loaded
if img is None:
    print("Image not found!")
else:
    # Display the original image
    cv2.imshow("Original Image", img)

    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(img, (15, 15), 0)

    # Display the blurred image
    cv2.imshow("Gaussian Blur Image", blur)

    # Save the blurred image
    cv2.imwrite("flower.jpg", blur)

    print("Gaussian Blur applied successfully!")
    print("Blurred image saved as flower.jpg")

    # Wait until a key is pressed
    cv2.waitKey(0)

    # Close all windows
    cv2.destroyAllWindows()
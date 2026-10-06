import cv2

img = cv2.imread("flower.jpg")

if img is None:
    print("Image not found!")
else:
    # Show original image
    cv2.imshow("Original Image", img)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display grayscale image
    cv2.imshow("Gray Image", gray)

    # Save grayscale image
    cv2.imwrite("gray_flower.jpg", gray)

    print("Image converted successfully!")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
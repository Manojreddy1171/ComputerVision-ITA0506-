import cv2
from tkinter import Tk, filedialog

Tk().withdraw()
video_path = filedialog.askopenfilename(
    title="Select a Video",
    filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
)

if not video_path:
    print("No video selected!")
    exit()

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Unable to open video!")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Video - Normal Speed", frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

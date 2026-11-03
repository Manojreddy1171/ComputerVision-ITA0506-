import cv2
import pytesseract
from pathlib import Path

video_path = Path(__file__).resolve().parent.parent / "vedio41.mp4"
video = cv2.VideoCapture(str(video_path))
if not video.isOpened():
    raise FileNotFoundError(f"Video not found: {video_path}")
print("Extracting text from video...")
print("Press Q to stop.")
while True:
    ret, frame = video.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    if text.strip():
        print("Extracted Text:")
        print(text)
    cv2.imshow("Text Extraction from Video", frame)
    if cv2.waitKey(30) & 0xFF == ord("q"):
        break
video.release()
cv2.destroyAllWindows()
print("Text extraction completed.")
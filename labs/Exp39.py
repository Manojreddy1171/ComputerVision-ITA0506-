import cv2
from pathlib import Path

video_path = Path(__file__).resolve().parent.parent / "vedio40.mp4"
video = cv2.VideoCapture(str(video_path))
if not video.isOpened():
    raise FileNotFoundError(f"Video not found: {video_path}")

print("Applying median blur to video...")
print("Press Q to stop.")
try:
    while True:
        ret, frame = video.read()
        if not ret:
            break
        denoised = cv2.medianBlur(frame, 5)
        cv2.imshow("Original Video", frame)
        cv2.imshow("Median Filter Denoised Video", denoised)
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
finally:
    video.release()
    cv2.destroyAllWindows()

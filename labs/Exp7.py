import cv2
from pathlib import Path

video_path = Path(__file__).resolve().parent.parent / "vedio40.mp4"
video = cv2.VideoCapture(str(video_path))
if not video.isOpened():
    raise FileNotFoundError(f"Video not found or unable to open: {video_path}")

fps = video.get(cv2.CAP_PROP_FPS)
video.release()
if fps <= 0:
    fps = 30

print(f"Using video: {video_path}")
print("Press Q to stop.")
stop_requested = False
try:
    for title, speed in (
        ("Normal Speed", 1.0),
        ("Slow Motion", 0.5),
        ("Fast Motion", 2.0),
    ):
        if stop_requested:
            break
        video = cv2.VideoCapture(str(video_path))
        if not video.isOpened():
            raise OSError(f"Unable to reopen video: {video_path}")
        try:
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                cv2.imshow(title, frame)
                delay = max(1, int(1000 / (fps * speed)))
                if cv2.waitKey(delay) & 0xFF == ord("q"):
                    stop_requested = True
                    break
        finally:
            video.release()
            cv2.destroyWindow(title)
finally:
    cv2.destroyAllWindows()

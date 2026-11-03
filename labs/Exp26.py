import cv2
from pathlib import Path

root = Path(__file__).resolve().parent.parent
video_path = root / "vedio40.mp4"
output_path = root / "reverse_vedio40.mp4"

video = cv2.VideoCapture(str(video_path))
if not video.isOpened():
    raise FileNotFoundError(f"Video not found or unable to open: {video_path}")

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 25

frames = []
try:
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)
finally:
    video.release()

if not frames:
    raise ValueError(f"No frames could be read from video: {video_path}")

frames.reverse()
output = cv2.VideoWriter(
    str(output_path),
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height),
)
if not output.isOpened():
    raise OSError(f"Unable to create output video: {output_path}")

try:
    for frame in frames:
        output.write(frame)
finally:
    output.release()

print(f"Reverse video created successfully: {output_path}")
try:
    for frame in frames:
        cv2.imshow("Experiment 26 - Reverse Video", frame)
        if cv2.waitKey(max(1, int(1000 / fps))) & 0xFF == 27:
            break
finally:
    cv2.destroyAllWindows()

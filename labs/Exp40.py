import os
import shutil
import cv2
import pytesseract
from pathlib import Path


def configure_tesseract():
    configured_path = os.environ.get("TESSERACT_CMD")
    if configured_path:
        if not Path(configured_path).is_file():
            raise FileNotFoundError(
                f"TESSERACT_CMD does not point to a file: {configured_path}"
            )
        pytesseract.pytesseract.tesseract_cmd = configured_path
        return

    candidates = []
    if os.name == "nt":
        candidates.extend(
            [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
        )

    executable = next(
        (path for path in candidates if path and Path(path).is_file()),
        None,
    ) or shutil.which("tesseract")
    if executable is None:
        raise RuntimeError(
            "Tesseract OCR is required but was not found. Install it with "
            "`choco install tesseract -y` from an Administrator terminal, "
            "then restart the terminal. If it is installed elsewhere, set "
            "TESSERACT_CMD to the full path of tesseract.exe."
        )

    pytesseract.pytesseract.tesseract_cmd = executable


configure_tesseract()

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
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
IMG = cv2.imread(str(ROOT / 'images' / 'exp1_animal.jpg'))
IMG2 = cv2.imread(str(ROOT / 'images' / 'exp2_animal.jpg'))
IMG3 = cv2.imread(str(ROOT / 'images' / 'exp3_animal.jpg'))
BG = cv2.imread(str(ROOT / 'images' / 'exp4_animal.jpg'))

if IMG is None or IMG2 is None or IMG3 is None or BG is None:
    raise FileNotFoundError('One or more sample images are missing in the images/ folder.')


def save(exp_no, frame):
    out_path = ROOT / f'Exp{exp_no}output.png'
    ok = cv2.imwrite(str(out_path), frame)
    if not ok:
        raise RuntimeError(f'Failed to write {out_path}')
    print(f'saved {out_path.name}')


def ensure_size(a, b):
    if a.shape != b.shape:
        return cv2.resize(a, (b.shape[1], b.shape[0]))
    return a

# 1
save(1, cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY))

# 2
save(2, cv2.GaussianBlur(IMG, (15, 15), 0))

# 3
save(3, cv2.Canny(cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY), 100, 200))

# 4
gray = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
save(4, cv2.equalizeHist(gray))

# 5
hist_b = cv2.calcHist([IMG], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([IMG], [1], None, [256], [0, 256])
hist_r = cv2.calcHist([IMG], [2], None, [256], [0, 256])
canvas = np.full((300, 512, 3), 255, dtype=np.uint8)
for hist, color in [(hist_b, (255, 0, 0)), (hist_g, (0, 255, 0)), (hist_r, (0, 0, 255))]:
    values = np.squeeze(hist)
    max_val = max(1, float(values.max()))
    pts = []
    for x, value in enumerate(values):
        y = int(250 - (value / max_val) * 180)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        cv2.line(canvas, pts[i], pts[i + 1], color, 1)
save(5, canvas)

# 6
kernel = np.ones((5, 5), np.uint8)
save(6, cv2.erode(IMG, kernel, iterations=1))

# 7
video_path = ROOT / 'temp_video.mp4'
writer = cv2.VideoWriter(str(video_path), cv2.VideoWriter_fourcc(*'mp4v'), 12.0, (IMG.shape[1], IMG.shape[0]))
for i in range(10):
    frame = IMG.copy()
    cv2.putText(frame, f'Frame {i + 1}', (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    writer.write(frame)
writer.release()
cap = cv2.VideoCapture(str(video_path))
_, frame = cap.read()
cap.release()
save(7, frame)

# 8
save(8, cv2.dilate(IMG, kernel, iterations=1))

# 9
big = cv2.resize(IMG, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
small = cv2.resize(IMG, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
big = cv2.resize(big, (IMG.shape[1], IMG.shape[0]))
small = cv2.resize(small, (IMG.shape[1], IMG.shape[0]))
combined = np.hstack([IMG, big, small])
save(9, combined)

# 10/11/12
save(10, cv2.rotate(IMG, cv2.ROTATE_90_CLOCKWISE))
save(11, cv2.rotate(IMG, cv2.ROTATE_180))
save(12, cv2.rotate(IMG, cv2.ROTATE_90_COUNTERCLOCKWISE))

# 13 affine
rows, cols = IMG.shape[:2]
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
M = cv2.getAffineTransform(pts1, pts2)
save(13, cv2.warpAffine(IMG, M, (cols, rows)))

# 14 perspective
pts1 = np.float32([[50, 50], [300, 50], [50, 300], [300, 300]])
pts2 = np.float32([[0, 0], [300, 0], [100, 300], [300, 300]])
M = cv2.getPerspectiveTransform(pts1, pts2)
save(14, cv2.warpPerspective(IMG, M, (cols, rows)))

# 15 Harris corners
gray_f = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY).astype(np.float32)
corners = cv2.cornerHarris(gray_f, 2, 3, 0.04)
corners = cv2.dilate(corners, None)
corner_img = IMG.copy()
corner_img[corners > 0.01 * corners.max()] = [0, 0, 255]
save(15, corner_img)

# 16 threshold
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
save(16, thresh)

# 17 adaptive threshold
adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
save(17, adaptive)

# 18
save(18, cv2.medianBlur(IMG, 5))

# 19
save(19, cv2.bilateralFilter(IMG, 9, 75, 75))

# 20
sobel_x = cv2.convertScaleAbs(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3))
sobel_y = cv2.convertScaleAbs(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3))
sobel_combined = cv2.bitwise_or(sobel_x, sobel_y)
save(20, sobel_combined)

# 21
lap = cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_64F))
save(21, lap)

# 22
save(22, cv2.morphologyEx(IMG, cv2.MORPH_OPEN, kernel))

# 23
save(23, cv2.morphologyEx(IMG, cv2.MORPH_CLOSE, kernel))

# 24
img_b = ensure_size(IMG2, IMG)
save(24, cv2.absdiff(IMG, img_b))

# 25
h, w = IMG.shape[:2]
mask = np.zeros_like(IMG)
mask[:h // 2, :w // 2] = 255
save(25, cv2.bitwise_and(IMG, mask))

# 26
save(26, cv2.cvtColor(IMG, cv2.COLOR_BGR2HSV))

# 27
hsv = cv2.cvtColor(IMG, cv2.COLOR_BGR2HSV)
lower = np.array([0, 50, 50])
upper = np.array([255, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
save(27, cv2.bitwise_and(IMG, IMG, mask=mask))

# 28
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour_img = IMG.copy()
cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
save(28, contour_img)

# 29
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
box_img = IMG.copy()
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(box_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
save(29, box_img)

# 30
bg_img = ensure_size(BG, IMG)
diff = cv2.absdiff(bg_img, IMG)
gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray_diff, 25, 255, cv2.THRESH_BINARY)
save(30, mask)

# 31
template = IMG[50:250, 100:270]
result = cv2.matchTemplate(IMG, template, cv2.TM_CCOEFF_NORMED)
_, _, _, max_loc = cv2.minMaxLoc(result)
h_t, w_t = template.shape[:2]
box_img = IMG.copy()
cv2.rectangle(box_img, max_loc, (max_loc[0] + w_t, max_loc[1] + h_t), (0, 255, 0), 2)
save(31, box_img)

# 32
save(32, IMG[100:400, 150:500])

# 33
rows, cols = IMG.shape[:2]
M = np.float32([[1, 0, 50], [0, 1, 30]])
save(33, cv2.warpAffine(IMG, M, (cols, rows)))

# 34
save(34, cv2.flip(IMG, 1))

# 35
save(35, cv2.convertScaleAbs(IMG, alpha=1.5, beta=30))

# 36
low = cv2.pyrDown(IMG)
high = cv2.pyrUp(low)
low = cv2.resize(low, (IMG.shape[1], IMG.shape[0]))
high = cv2.resize(high, (IMG.shape[1], IMG.shape[0]))
pyramid = np.hstack([IMG, low, high])
save(36, pyramid)

# 37
kernel_sharp = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
save(37, cv2.filter2D(IMG, -1, kernel_sharp))

# 38
noise = np.random.normal(0, 25, IMG.shape).astype(np.uint8)
save(38, cv2.add(IMG, noise))

# 39
save(39, cv2.medianBlur(IMG, 5))

# 40
img_b2 = ensure_size(IMG3, IMG)
save(40, cv2.addWeighted(IMG, 0.5, img_b2, 0.5, 0))

video_path.unlink(missing_ok=True)
print('All experiment outputs generated successfully.')

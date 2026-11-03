import cv2

DISPLAY_W = 700
DISPLAY_H = 520
WINDOW_X = 40
WINDOW_Y = 60
X_STEP = 760
Y_STEP = 560
_window_index = 0

def show_small(title, image):
    global _window_index
    if image is None:
        return

    h, w = image.shape[:2]
    scale = min(DISPLAY_W / w, DISPLAY_H / h) if w and h else 1.0
    if scale < 1.0:
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, image.shape[1], image.shape[0])
    x = WINDOW_X + (_window_index % 3) * X_STEP
    y = WINDOW_Y + (_window_index // 3) * Y_STEP
    cv2.moveWindow(title, x, y)
    cv2.imshow(title, image)
    _window_index += 1

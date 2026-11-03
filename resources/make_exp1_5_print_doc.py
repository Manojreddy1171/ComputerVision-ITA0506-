from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / 'Exp1_to_Exp5_Print_Clean.pdf'


def resize_to_fit(path, max_w, max_h):
    with Image.open(path) as img:
        width, height = img.size
        scale = min(max_w / width, max_h / height)
        return max(1, int(width * scale)), max(1, int(height * scale))


def add_experiment_row(c, exp_no, left_x, right_x, top_y):
    label_y = top_y + 48 * mm
    img_w = 55 * mm
    img_h = 42 * mm

    input_path = ROOT / f'Exp{exp_no}input.jpg'
    output_path = ROOT / f'Exp{exp_no}output.png'
    if not input_path.exists():
        input_path = ROOT / 'images' / f'exp{exp_no}_animal.jpg'

    c.setFont('Helvetica-Bold', 10)
    c.drawString(left_x, label_y, f'Exp {exp_no} - Input')
    c.drawString(right_x, label_y, f'Exp {exp_no} - Output')

    input_w, input_h = resize_to_fit(input_path, img_w, img_h)
    output_w, output_h = resize_to_fit(output_path, img_w, img_h)

    img_y1 = top_y
    img_y2 = top_y
    c.drawImage(str(input_path), left_x, img_y1, width=input_w, height=input_h)
    c.drawImage(str(output_path), right_x, img_y2, width=output_w, height=output_h)


def add_page(c, experiments, page_no):
    c.setTitle(f'CV Lab Print - Page {page_no}')
    c.setFont('Helvetica-Bold', 16)
    c.drawString(55 * mm, 286 * mm, 'Computer Vision Lab Experiments 1 to 5')

    if page_no == 1:
        rows = [(1, 25 * mm, 108 * mm, 185 * mm), (2, 25 * mm, 108 * mm, 105 * mm), (3, 25 * mm, 108 * mm, 25 * mm)]
    else:
        rows = [(4, 25 * mm, 108 * mm, 185 * mm), (5, 25 * mm, 108 * mm, 105 * mm)]

    for exp_no, left_x, right_x, top_y in rows:
        add_experiment_row(c, exp_no, left_x, right_x, top_y)


for i in range(1, 6):
    src = ROOT / 'images' / f'exp{i}_animal.jpg'
    dst = ROOT / f'Exp{i}input.jpg'
    if src.exists() and not dst.exists():
        dst.write_bytes(src.read_bytes())

c = canvas.Canvas(str(OUT_PDF), pagesize=A4)
add_page(c, [1, 2, 3], 1)
c.showPage()
add_page(c, [4, 5], 2)
c.save()
print(f'Created: {OUT_PDF}')

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / 'Exp1_to_Exp5_Print.pdf'


def resize_to_fit(path, max_w, max_h):
    with Image.open(path) as img:
        width, height = img.size
        scale = min(max_w / width, max_h / height)
        new_w = max(1, int(width * scale))
        new_h = max(1, int(height * scale))
        return new_w, new_h


def add_experiment_page(c, experiments, page_no):
    c.setTitle(f'Exp1-5 Printout - Page {page_no}')
    c.setFont('Helvetica-Bold', 16)
    c.drawString(20 * mm, 285 * mm, 'Computer Vision Lab - Experiments 1 to 5')
    y_cursor = 250 * mm
    x_left = 25 * mm
    x_right = 120 * mm
    img_w = 55 * mm
    img_h = 42 * mm

    for idx, exp_no in enumerate(experiments, 1):
        if y_cursor < 60 * mm:
            c.showPage()
            y_cursor = 250 * mm
        c.setFont('Helvetica-Bold', 11)
        c.drawString(x_left, y_cursor + 2 * mm, f'Exp {exp_no} - Input')
        c.drawString(x_right, y_cursor + 2 * mm, f'Exp {exp_no} - Output')

        input_path = ROOT / f'Exp{exp_no}input.jpg'
        output_path = ROOT / f'Exp{exp_no}output.png'
        if not input_path.exists():
            input_path = ROOT / f'images' / f'exp{exp_no}_animal.jpg'
        if not output_path.exists():
            output_path = ROOT / f'Exp{exp_no}output.png'

        input_w, input_h = resize_to_fit(input_path, img_w, img_h)
        output_w, output_h = resize_to_fit(output_path, img_w, img_h)
        c.drawImage(str(input_path), x_left, y_cursor - input_h, width=input_w, height=input_h)
        c.drawImage(str(output_path), x_right, y_cursor - output_h, width=output_w, height=output_h)

        y_cursor -= 78 * mm


# Create input copies for the 5 experiments if needed
for i in range(1, 6):
    src = ROOT / 'images' / f'exp{i}_animal.jpg'
    dst = ROOT / f'Exp{i}input.jpg'
    if src.exists() and not dst.exists():
        dst.write_bytes(src.read_bytes())

# Build PDF
c = canvas.Canvas(str(OUT_PDF), pagesize=A4)
add_experiment_page(c, [1, 2, 3], 1)
add_experiment_page(c, [4, 5], 2)
c.save()
print(f'Created: {OUT_PDF}')

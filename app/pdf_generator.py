from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
import io
import datetime

PARTICIPATION_TEMPLATE_PATH = "templates/participation-template.png"
FINANCE_CHAMPION_TEMPLATE_PATH = "templates/finance-champion-template.png"
FINANCE_1ST_TEMPLATE_PATH = "templates/finance-first-runner-template.png"
FINANCE_2ND_TEMPLATE_PATH = "templates/finance-second-runner-template.png"
SOCIETY_CHAMPION_TEMPLATE_PATH = "templates/society-champion-template.png"
SOCIETY_1ST_TEMPLATE_PATH = "templates/society-first-runner-template.png"
SOCIETY_2ND_TEMPLATE_PATH = "templates/society-second-runner-template.png"
SOCIETY_OPA_TEMPLATE_PATH = "templates/society-opa-template.png"
FONT_PATH = "fonts/Roboto-Regular.ttf"

def generate_certificate(name: str, cert_no: str, cert_type: str) -> bytes:

    if cert_type == "participant":
        TEMPLATE_PATH = PARTICIPATION_TEMPLATE_PATH
    elif cert_type == "finance-champion":
        TEMPLATE_PATH = FINANCE_CHAMPION_TEMPLATE_PATH
    elif cert_type == "finance-first":
        TEMPLATE_PATH = FINANCE_1ST_TEMPLATE_PATH
    elif cert_type == "finance-second":
        TEMPLATE_PATH = FINANCE_2ND_TEMPLATE_PATH
    elif cert_type == "society-champion":
        TEMPLATE_PATH = SOCIETY_CHAMPION_TEMPLATE_PATH
    elif cert_type == "society-first":
        TEMPLATE_PATH = SOCIETY_1ST_TEMPLATE_PATH
    elif cert_type == "society-second":
        TEMPLATE_PATH = SOCIETY_2ND_TEMPLATE_PATH
    elif cert_type == "society-opa":
        TEMPLATE_PATH = SOCIETY_OPA_TEMPLATE_PATH
    else:
        TEMPLATE_PATH = PARTICIPATION_TEMPLATE_PATH

    # 1. Load template
    img = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 2. Load font
    name_font = ImageFont.truetype(FONT_PATH, 45)
    cert_font = ImageFont.truetype(FONT_PATH, 21)

    # 3. Place Name (center)
    name_w, name_h = draw.textbbox((0, 0), name, font=name_font)[2:]
    img_width, img_height = img.size
    draw.text(((img_width - name_w) / 2, img_height * 0.55), name, fill="black", font=name_font)

    # 4. Place certificate number
    draw.text((img_width * 0.19, img_height * 0.85), f"{cert_no}", fill="gray", font=cert_font)

    # 5. Convert template to image buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # ---- CREATE PDF ----
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    c.drawImage(ImageReader(img_buffer), 0, 0, width=width, height=height)
    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "depliant-fermeture-poche-falaise-chambois.pdf"
HERO_IMAGE = ROOT / "assets" / "cimetiere-polonais-urville-wiki.jpeg"
LOGO = ROOT / "assets" / "1_pancerna_gen_Maczka.gif"

BLUE_950 = colors.HexColor("#071733")
BLUE_900 = colors.HexColor("#102a56")
BLUE_700 = colors.HexColor("#174a8b")
RED_700 = colors.HexColor("#bb1f2d")
RED_600 = colors.HexColor("#d52b3a")
SURFACE = colors.HexColor("#f7f9fc")
LINE = colors.HexColor("#d8deea")
MUTED = colors.HexColor("#5c677d")
WHITE = colors.white


def draw_wrapped(c, text, x, y, width, style):
    paragraph = Paragraph(text, style)
    _, height = paragraph.wrap(width, 1000)
    paragraph.drawOn(c, x, y - height)
    return y - height


def fit_image_cover(c, image_path, x, y, w, h):
    c.saveState()
    path = c.beginPath()
    path.roundRect(x, y, w, h, 4 * mm)
    c.clipPath(path, stroke=0, fill=0)
    c.drawImage(str(image_path), x, y, w, h, preserveAspectRatio=True, anchor="c", mask="auto")
    c.restoreState()


def pill(c, text, x, y, bg, fg=WHITE, pad_x=4 * mm, pad_y=2.5 * mm, font_size=9):
    width = stringWidth(text, "Helvetica-Bold", font_size) + 2 * pad_x
    height = font_size + 2 * pad_y
    c.setFillColor(bg)
    c.roundRect(x, y - height, width, height, 3 * mm, stroke=0, fill=1)
    c.setFillColor(fg)
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(x + pad_x, y - height + pad_y + 1, text)
    return width


def draw_qr(c, data, x, y, size):
    code = qr.QrCodeWidget(data)
    bounds = code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    drawing.add(code)
    renderPDF.draw(drawing, c, x, y)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4)
    w, h = A4
    margin = 13 * mm
    panel_h = h / 3

    # Background and fold guides.
    c.setFillColor(WHITE)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    c.setStrokeColor(colors.HexColor("#b8c0cf"))
    c.setDash(2, 4)
    for y in (panel_h, panel_h * 2):
        c.line(8 * mm, y, w - 8 * mm, y)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        c.drawRightString(w - 9 * mm, y + 2 * mm, "ligne de pliage")
    c.setDash()

    styles = {
        "kicker": ParagraphStyle(
            "kicker",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=RED_600,
            uppercase=True,
            spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=27,
            textColor=BLUE_950,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=BLUE_950,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=9.4,
            leading=12.7,
            textColor=colors.HexColor("#303a4a"),
        ),
        "small": ParagraphStyle(
            "small",
            fontName="Helvetica",
            fontSize=8.3,
            leading=11,
            textColor=MUTED,
        ),
        "tiny": ParagraphStyle(
            "tiny",
            fontName="Helvetica",
            fontSize=7.25,
            leading=9.15,
            textColor=MUTED,
        ),
        "white": ParagraphStyle(
            "white",
            fontName="Helvetica",
            fontSize=9.3,
            leading=12.4,
            textColor=colors.HexColor("#eaf1fb"),
        ),
    }

    # Panel 1 - essential ceremony information.
    y_top = h - margin
    if LOGO.exists():
        c.drawImage(str(LOGO), margin, y_top - 17 * mm, 11 * mm, 15 * mm, preserveAspectRatio=True, mask="auto")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLUE_950)
    c.drawString(margin + 15 * mm, y_top - 6 * mm, "ANS1DBP")
    c.setFont("Helvetica", 7.7)
    c.setFillColor(MUTED)
    c.drawString(margin + 15 * mm, y_top - 11 * mm, "Association Nationale du Souvenir de la 1ère Division Blindée Polonaise")

    fit_image_cover(c, HERO_IMAGE, w - margin - 62 * mm, panel_h * 2 + 14 * mm, 62 * mm, 54 * mm)
    x = margin
    y = y_top - 24 * mm
    y = draw_wrapped(c, "CÉRÉMONIE OFFICIELLE", x, y, 112 * mm, styles["kicker"])
    y -= 2 * mm
    y = draw_wrapped(c, "Fermeture de la Poche de Falaise-Chambois", x, y, 110 * mm, styles["h1"])
    y -= 5 * mm
    pill(c, "DIMANCHE 23 AOÛT 2026", x, y, BLUE_900)
    pill(c, "9 H 30", x + 55 * mm, y, RED_700)
    y -= 16 * mm
    text = (
        "L’Association Nationale du Souvenir de la 1ère Division Blindée Polonaise vous invite "
        "à une cérémonie commémorative publique, ouverte à tous, au cimetière militaire polonais d’Urville."
    )
    y = draw_wrapped(c, text, x, y, 110 * mm, styles["body"])
    y -= 3 * mm
    text = (
        "<b>Lieu :</b> cimetière militaire polonais d’Urville, aussi appelé cimetière d’Urville-Langannerie "
        "en raison de son accès par Grainville-Langannerie depuis la N158."
    )
    draw_wrapped(c, text, x, y, 110 * mm, styles["small"])

    # Panel 2 - program.
    y2_top = panel_h * 2 - margin
    c.setFillColor(SURFACE)
    c.rect(0, panel_h, w, panel_h, stroke=0, fill=1)
    x = margin
    y = y2_top
    y = draw_wrapped(c, "PROGRAMME DE LA CÉRÉMONIE", x, y, w - 2 * margin, styles["kicker"])
    y -= 1 * mm
    y = draw_wrapped(c, "Déroulé de la matinée", x, y, w - 2 * margin, styles["h2"])
    y -= 7 * mm

    def schedule_block(time, title, subtitle, items, x, y, width, height):
        c.setFillColor(WHITE)
        c.roundRect(x, y - height, width, height, 3 * mm, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.roundRect(x, y - height, width, height, 3 * mm, stroke=1, fill=0)
        c.setFillColor(BLUE_900)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(x + 6 * mm, y - 12 * mm, time)
        tx = x + 6 * mm
        ty = y - 21 * mm
        ty = draw_wrapped(c, f"<b>{title}</b>", tx, ty, width - 12 * mm, styles["body"])
        if subtitle:
            ty -= 1 * mm
            ty = draw_wrapped(c, subtitle, tx, ty, width - 12 * mm, styles["tiny"])
        ty -= 2 * mm
        item_text = "<br/>".join([f"- {item}" for item in items])
        draw_wrapped(c, item_text, tx, ty, width - 12 * mm, styles["tiny"])

    gap = 7 * mm
    card_w = (w - 2 * margin - gap) / 2
    card_h = 57 * mm
    card_y = y

    schedule_block(
        "9 h 30",
        "Cimetière militaire polonais",
        "Urville, accès par Grainville-Langannerie",
        [
            "Accueil des participants et placement des porte-drapeaux.",
            "Cérémonie religieuse.",
            "Cérémonie du Souvenir de la 1ère Division Blindée Polonaise.",
            "Allumage de la Flamme.",
            "Dépôts de gerbes autorisées pendant la cérémonie officielle.",
            "Sonnerie « Aux Morts » et hymnes nationaux.",
        ],
        x,
        card_y,
        card_w,
        card_h,
    )
    schedule_block(
        "11 h 30",
        "Potigny",
        "Commune surnommée la « petite Varsovie ».",
        [
            "Cérémonie à Potigny, à laquelle l’association participera également.",
            "Dépôts de gerbes au monument polonais.",
            "Suivi du verre de l’amitié offert par la municipalité.",
        ],
        x + card_w + gap,
        card_y,
        card_w,
        card_h,
    )

    # Panel 3 - website and contact/action.
    c.setFillColor(BLUE_950)
    c.rect(0, 0, w, panel_h, stroke=0, fill=1)
    x = margin
    y = panel_h - margin
    c.setFillColor(RED_600)
    c.rect(x, y - 4 * mm, 28 * mm, 1.2 * mm, stroke=0, fill=1)
    y -= 9 * mm
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x, y, "Informations en ligne")
    y -= 8 * mm
    web = "https://www.ans1dbp.fr/fermeture-poche-falaise-chambois.html"
    body = (
        "Sur la page de l’événement, vous pouvez signaler votre présence, retrouver les informations pratiques "
        "et poser vos questions à notre ChatBOT IA au sujet de l’association ou de la cérémonie."
    )
    y = draw_wrapped(c, body, x, y, 118 * mm, styles["white"])
    y -= 5 * mm
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x, y, "Page événement")
    y -= 5 * mm
    c.setFont("Helvetica", 8.3)
    c.setFillColor(colors.HexColor("#eaf1fb"))
    c.drawString(x, y, web)
    y -= 9 * mm
    c.setFillColor(RED_700)
    c.roundRect(x, y - 12 * mm, 54 * mm, 12 * mm, 3 * mm, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x + 27 * mm, y - 8 * mm, "Signaler ma présence")
    c.setFillColor(colors.HexColor("#eaf1fb"))
    c.setFont("Helvetica", 8)
    c.drawString(x + 62 * mm, y - 8 * mm, "Formulaire : https://forms.gle/h2bZywtfPHpB6cF68")

    qr_size = 43 * mm
    qr_x = w - margin - qr_size
    qr_y = 14 * mm
    c.setFillColor(WHITE)
    c.roundRect(qr_x - 4 * mm, qr_y - 4 * mm, qr_size + 8 * mm, qr_size + 14 * mm, 4 * mm, stroke=0, fill=1)
    draw_qr(c, web, qr_x, qr_y + 6 * mm, qr_size)
    c.setFillColor(BLUE_950)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(qr_x + qr_size / 2, qr_y, "Scanner la page")

    c.setFillColor(colors.HexColor("#eaf1fb"))
    c.setFont("Helvetica", 7.4)
    c.drawString(margin, 8 * mm, "ANS1DBP - Association Nationale du Souvenir de la 1ère Division Blindée Polonaise")

    c.save()
    print(OUT)


if __name__ == "__main__":
    main()

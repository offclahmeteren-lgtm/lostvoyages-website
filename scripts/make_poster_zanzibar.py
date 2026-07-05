"""
Lost Voyages — Zanzibar Tur Afisi (A4, tek sayfa, tarihsiz)
Marka: Navy #0F1923 · Gold #D4A017 · Teal #2ABFBF · Montserrat + ReklameScript
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import io, os

W, H = A4

FONTS = '/Users/ahmeterenvci/lostvoyages-website/fonts/'
pdfmetrics.registerFont(TTFont('MR',   FONTS + 'Montserrat-Regular.ttf'))
pdfmetrics.registerFont(TTFont('MB',   FONTS + 'Montserrat-Bold.ttf'))
pdfmetrics.registerFont(TTFont('MSB',  FONTS + 'Montserrat-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('ML',   FONTS + 'Montserrat-Light.ttf'))

NAVY  = HexColor('#0F1923')
GOLD  = HexColor('#D4A017')
GOLD2 = HexColor('#E8B82A')
TEAL  = HexColor('#2ABFBF')
WHITE = HexColor('#E8E6E1')
DIM   = HexColor('#8A8880')

IMG = '/Users/ahmeterenvci/lostvoyages-website/images/gallery/'
OUT = os.path.expanduser('~/Desktop/zanzibar-afis.pdf')

def load(path, mw=1200, q=78):
    try:
        p = PILImage.open(path).convert('RGB')
        w, h = p.size
        if w > mw: p = p.resize((mw, int(h * mw / w)), PILImage.LANCZOS)
        buf = io.BytesIO()
        p.save(buf, 'JPEG', quality=q, optimize=True)
        buf.seek(0)
        return ImageReader(buf)
    except: return None

def t(c, s, x, y, fn='MR', fs=10, col=WHITE, align='l'):
    c.setFont(fn, fs)
    c.setFillColor(col)
    if align == 'c': c.drawCentredString(x, y, s)
    elif align == 'r': c.drawRightString(x, y, s)
    else: c.drawString(x, y, s)

def hline(c, x1, y, x2, col=None, lw=0.5):
    c.setStrokeColor(col or Color(1, 1, 1, alpha=0.15))
    c.setLineWidth(lw)
    c.line(x1, y, x2, y)

def poster(c):
    # ── Tam sayfa fotoğraf ────────────────────────────────────────────────
    r = load(IMG + 'zb-2.jpg')
    if r:
        c.drawImage(r, 0, 0, W, H, preserveAspectRatio=False)

    # Üstten navy gradient
    steps = 18
    for i in range(steps):
        a = 0.03 + i * 0.028
        sh = H * 0.072
        c.setFillColor(Color(0.059, 0.098, 0.137, alpha=a))
        c.rect(0, H - (i+1)*sh, W, sh + 1, fill=1, stroke=0)

    # Alttan navy gradient — daha güçlü
    for i in range(22):
        a = 0.04 + i * 0.038
        sh = H * 0.058
        c.setFillColor(Color(0.059, 0.098, 0.137, alpha=a))
        c.rect(0, 0, W, (i+1)*sh + 1, fill=1, stroke=0)

    # ── Nav çizgisi + Logo ───────────────────────────────────────────────
    c.setFillColor(Color(0.059, 0.098, 0.137, alpha=0.72))
    c.rect(0, H - 56, W, 56, fill=1, stroke=0)
    hline(c, 0, H - 56, W, col=Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.4), lw=1)

    # ReklameScript logo — tam web sitesiyle aynı
    t(c, 'Lost Voyages', W/2, H - 34, 'MB', 22, GOLD, 'c')
    t(c, 'lostvoyages.com', W/2, H - 47, 'ML', 7, Color(1,1,1,alpha=0.45), 'c')

    # ── Orta alan: Ana başlık ─────────────────────────────────────────────
    title_y = H * 0.525

    # "ZANZIBAR" — Reklame Script, büyük
    t(c, 'Zanzibar', W/2, title_y + 14, 'MB', 82, WHITE, 'c')

    # Gold alt çizgi
    lw = 88
    hline(c, W/2 - lw, title_y - 4, W/2 + lw,
          col=Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.85), lw=1.8)

    # Tagline — Montserrat Light
    t(c, 'H İ N T   O K Y A N U S U\'N U N   İ N C İ S İ', W/2, title_y - 22,
      'ML', 9.5, Color(1,1,1,alpha=0.78), 'c')

    # ── Meta rozetler ─────────────────────────────────────────────────────
    meta_y = title_y - 54
    metas = ['5 Gece / 6 Gün', 'Maks. 20 Kişi', '4 Yıldızlı Otel', 'Stone Town · Jozani · Paje']

    c.setFont('MSB', 8)
    widths = [c.stringWidth(m, 'MSB', 8) + 22 for m in metas]
    total_w = sum(widths) + (len(metas) - 1) * 8
    px = W/2 - total_w/2

    for m, mw in zip(metas, widths):
        # pill arka plan
        c.setFillColor(Color(NAVY.red, NAVY.green, NAVY.blue, alpha=0.75))
        c.roundRect(px, meta_y - 1, mw, 18, 4, fill=1, stroke=0)
        c.setStrokeColor(Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.5))
        c.setLineWidth(0.6)
        c.roundRect(px, meta_y - 1, mw, 18, 4, fill=0, stroke=1)
        t(c, m, px + mw/2, meta_y + 5, 'MSB', 8, WHITE, 'c')
        px += mw + 8

    # ── Alt panel ─────────────────────────────────────────────────────────
    panel_h = 158

    # Navy panel
    c.setFillColor(Color(NAVY.red, NAVY.green, NAVY.blue, alpha=0.93))
    c.rect(0, 0, W, panel_h, fill=1, stroke=0)

    # Gold üst çizgi
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(0, panel_h, W, panel_h)

    # Teal Gold iç çizgi
    c.setStrokeColor(Color(TEAL.red, TEAL.green, TEAL.blue, alpha=0.3))
    c.setLineWidth(0.5)
    c.line(0, panel_h - 1, W, panel_h - 1)

    # Sol sütun — öne çıkanlar
    pad = 32
    hy = panel_h - 20
    t(c, 'ÖNE ÇIKANLAR', pad, hy, 'MB', 8, GOLD)
    hy -= 16
    highlights = [
        'Stone Town — UNESCO Dünya Mirası',
        'Safari Blue — Yunuslar, Mercan, Sandbar',
        'Jozani Ormanı — Kızıl Colobus Maymunları',
        'Baharat Bahçesi & Zanzibar Mutfağı',
        'Nakupenda Sandbar — Açık Okyanus Güneşbatımı',
    ]
    for line in highlights:
        c.setFillColor(TEAL)
        c.circle(pad + 5, hy + 4, 2.5, fill=1, stroke=0)
        t(c, line, pad + 14, hy, 'MR', 8.5, WHITE)
        hy -= 15

    # Dikey ayraç
    hline(c, W * 0.58, 14, W * 0.58, col=Color(1,1,1,alpha=0.1), lw=0.5)
    # Yukarıdan aşağıya dikey çizgi
    c.setStrokeColor(Color(1,1,1,alpha=0.1))
    c.setLineWidth(0.5)
    c.line(W * 0.58, 14, W * 0.58, panel_h - 14)

    # Sağ sütun — iletişim + fiyat
    rx = W * 0.61
    t(c, 'BİLGİ & REZERVASYON', rx, panel_h - 20, 'MB', 8, GOLD)

    t(c, 'lostvoyages.com', rx, panel_h - 40, 'MSB', 11, WHITE)
    t(c, 'WhatsApp  +90 545 170 69 27', rx, panel_h - 57, 'MR', 9, DIM)
    t(c, '@ahmeterenvci', rx, panel_h - 72, 'MR', 9, DIM)

    hline(c, rx, panel_h - 82, W - 24, col=Color(1,1,1,alpha=0.1))

    # Fiyat
    t(c, '1.995 €', rx, panel_h - 102, 'MB', 22, GOLD)
    t(c, 'kişi başı (uçak hariç)', rx, panel_h - 117, 'ML', 8.5, DIM)
    t(c, 'Kapora ile yerinizi garantileyin', rx, panel_h - 132, 'ML', 8, DIM)

def main():
    cv = canvas.Canvas(OUT, pagesize=A4)
    cv.setTitle('Lost Voyages — Zanzibar Tur Afişi')
    cv.setAuthor('Lost Voyages | Ahmet Eren')
    poster(cv)
    cv.save()
    print(f'OK: {OUT}  ({os.path.getsize(OUT)//1024} KB)')

if __name__ == '__main__':
    main()

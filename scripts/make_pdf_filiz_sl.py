"""
Lost Voyages — Sri Lanka Özel Tur Planlama Dokümanı
3 sayfa · LV marka: krem, navy, gold, Reklame Script PIL, Montserrat
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageEnhance
import io, os

W, H   = A4
OUTPUT = os.path.expanduser("~/Desktop/filiz-alguney-srilanka.pdf")
FONTS  = "/Users/ahmeterenvci/lostvoyages-website/fonts"
GALR   = "/Users/ahmeterenvci/lostvoyages-website/images/gallery"

for name, file in [
    ("M-Light",    "Montserrat-Light"),
    ("M-Regular",  "Montserrat-Regular"),
    ("M-SemiBold", "Montserrat-SemiBold"),
    ("M-Bold",     "Montserrat-Bold"),
]:
    pdfmetrics.registerFont(TTFont(name, f"{FONTS}/{file}.ttf"))

REKLAME = f"{FONTS}/ReklameScript-Medium.otf"

CREAM  = HexColor("#FAF8F4")
NAVY   = HexColor("#1B1730")
GOLD   = HexColor("#C8940E")
WARM   = HexColor("#F2EFE8")
BORDER = HexColor("#E2DDD4")
MUTED  = HexColor("#8A8070")
WHITE  = white
GREEN  = HexColor("#2A7A50")
TEAL   = HexColor("#1A8080")
RED_M  = HexColor("#A03030")

LM = 1.5*cm; RM = W - 1.5*cm; CW = RM - LM

# ── Yardımcı fonksiyonlar ────────────────────────────────────────────────────
def R(c, x, y, w, h, fill=None, stroke=None, r=0, sw=0.5):
    c.saveState(); c.setLineWidth(sw)
    if fill:   c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke)
    kw = dict(fill=1 if fill else 0, stroke=1 if stroke else 0)
    (c.roundRect(x,y,w,h,r,**kw) if r else c.rect(x,y,w,h,**kw))
    c.restoreState()

def T(c, text, x, y, font="M-Regular", size=10, color=NAVY, align="left", max_w=None):
    c.saveState(); c.setFont(font, size); c.setFillColor(color)
    lh = size * 1.35
    if max_w:
        words = str(text).split(); lines, cur = [], ""
        for w_ in words:
            t_ = (cur+" "+w_).strip()
            if c.stringWidth(t_, font, size) <= max_w: cur = t_
            else:
                if cur: lines.append(cur)
                cur = w_
        if cur: lines.append(cur)
        for i, ln in enumerate(lines):
            ly = y - i*lh
            if   align=="center": c.drawCentredString(x, ly, ln)
            elif align=="right":  c.drawRightString(x, ly, ln)
            else:                 c.drawString(x, ly, ln)
        c.restoreState()
        return len(lines)*lh
    else:
        if   align=="center": c.drawCentredString(x, y, str(text))
        elif align=="right":  c.drawRightString(x, y, str(text))
        else:                 c.drawString(x, y, str(text))
        c.restoreState()
        return lh

def L(c, x1, y1, x2, y2, color=BORDER, w=0.5):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(w)
    c.line(x1,y1,x2,y2); c.restoreState()

def img_box(c, path, x, y, w, h, q=88):
    try:
        im = PILImage.open(path).convert("RGB")
        pw, ph = int(w*3), int(h*3)
        s = max(pw/im.width, ph/im.height)
        nw, nh = int(im.width*s), int(im.height*s)
        im = im.resize((nw,nh), PILImage.LANCZOS)
        l_=(nw-pw)//2; t_=(nh-ph)//2
        im = im.crop((l_,t_,l_+pw,t_+ph))
        im = ImageEnhance.Sharpness(im).enhance(1.1)
        buf = io.BytesIO(); im.save(buf,"JPEG",quality=q); buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, w, h)
    except Exception as e: print(f"[img] {path}: {e}")

def reklame(c, text, cx, cy, size, rgba=(200,148,14,255), align="center"):
    px = int(size*3.5)
    try:    fnt = ImageFont.truetype(REKLAME, px)
    except: fnt = ImageFont.load_default()
    dummy = PILImage.new("RGBA",(1,1)); dd = ImageDraw.Draw(dummy)
    bb = dd.textbbox((0,0), text, font=fnt)
    pw, ph = bb[2]-bb[0]+24, bb[3]-bb[1]+24
    im = PILImage.new("RGBA",(pw,ph),(0,0,0,0))
    ImageDraw.Draw(im).text((12-bb[0], 12-bb[1]), text, font=fnt, fill=rgba)
    buf = io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
    ptw, pth = pw/3.5, ph/3.5
    if   align=="center": c.drawImage(ImageReader(buf), cx-ptw/2, cy-pth, ptw, pth, mask="auto")
    elif align=="right":  c.drawImage(ImageReader(buf), cx-ptw,   cy-pth, ptw, pth, mask="auto")
    else:                 c.drawImage(ImageReader(buf), cx,       cy-pth, ptw, pth, mask="auto")
    return ptw, pth

def make_gradient(pw, ph):
    im = PILImage.new("RGBA",(pw,ph),(0,0,0,0))
    draw = ImageDraw.Draw(im)
    for row in range(ph):
        frac = row/ph
        a = int(frac**1.5 * 0.82 * 255)
        draw.line([(0,row),(pw,row)], fill=(26,23,46,a))
    buf = io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
    return ImageReader(buf)

def footer(c):
    R(c, 0, 0, W, 1*cm, fill=NAVY)
    T(c, "lostvoyages.com  ·  iletisim@lostvoyages.com  ·  +90 545 170 69 27",
      W/2, 3.5*mm, "M-Regular", 6.5, HexColor("#c0b8a0"), "center")

cv = canvas.Canvas(OUTPUT, pagesize=A4)

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 1 — KAPAK
# ══════════════════════════════════════════════════════════════════════════════
R(cv, 0, 0, W, H, fill=CREAM)

HERO_H = H * 0.58
IY = H - HERO_H

img_box(cv, f"{GALR}/sl-new-3.jpg", 0, IY, W, HERO_H, q=90)
cv.drawImage(make_gradient(int(W*1.5), int(HERO_H*1.5)), 0, IY, W, HERO_H, mask="auto")

R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)
reklame(cv, "Lost Voyages", W/2, H-7*mm, 13, rgba=(200,148,14,255), align="center")

reklame(cv, "Sri Lanka", W/2, IY+6.2*cm, 52, rgba=(255,255,255,255), align="center")

T(cv, "Özel Wellness Turu",
  W/2, IY+3.6*cm, "M-SemiBold", 13, HexColor("#E8D898"), "center")

T(cv, "C O L O M B O   ·   M İ R İ S S A   ·   H İ R İ K E T İ Y A   ·   S A F A R İ",
  W/2, IY+2.6*cm, "M-Light", 9, HexColor("#c8c0a8"), "center")

T(cv, "Şubat — Mart  2027   ·   6 Gece / 7 Gün",
  W/2, IY+1.6*cm, "M-Regular", 8.5, HexColor("#E8D898"), "center")

R(cv, 0, IY-5*mm, W, 5*mm, fill=GOLD)

# ── Bilgi alanı ──────────────────────────────────────────────────────────────
INFO_TOP = IY - 5*mm
LCW = CW * 0.42
RCX = LM + LCW + 0.6*cm
RCW = CW - LCW - 0.6*cm
LCX = LM + LCW/2

cy = INFO_TOP - 0.6*cm
T(cv, "6 GECE / 7 GÜN", LCX, cy, "M-Bold", 7, GOLD, "center")
cy -= 13
_, prh = reklame(cv, "6 Gece", LCX, cy, 34, rgba=(26,23,48,255), align="center")
cy -= prh + 2
T(cv, "Colombo · Mirissa · Hiriketiya · Safari", LCX, cy, "M-Light", 7.5, MUTED, "center")
cy -= 14
L(cv, LM+0.2*cm, cy, LM+LCW-0.2*cm, cy, BORDER, 0.5)
cy -= 10

infos = [
    ("Sezon:",  "Şubat–Mart 2027 · kuru & güneşli"),
    ("Safari:", "Yala veya Udawalawe — seçimlik"),
    ("Yemek:",  "Açık büfe kahvaltı & akşam yemeği"),
]
for lbl, val in infos:
    T(cv, lbl, LM+0.2*cm, cy, "M-Regular", 7.5, MUTED)
    T(cv, val,  LM+0.2*cm+1.2*cm, cy, "M-SemiBold", 7.5, NAVY, max_w=LCW-1.4*cm)
    cy -= 13
cy_left_end = cy

badges = [
    ("Gün 1",   "Colombo — Şehir Turu"),
    ("Gün 2–3", "Mirissa — Sahil & Balina Turu"),
    ("Gün 4–5", "Hiriketiya — Koy & Wellness"),
    ("Gün 6",   "Safari — Yala veya Udawalawe"),
    ("Gün 7",   "Dönüş — Colombo Havalimanı"),
]
by = INFO_TOP - 0.2*cm
for lbl, val in badges:
    R(cv, RCX, by-0.62*cm, RCW, 0.60*cm, fill=WHITE, stroke=BORDER, r=3)
    T(cv, lbl.upper(), RCX+0.25*cm, by-0.38*cm, "M-Bold", 6.5, GOLD)
    T(cv, val, RCX+RCW-0.25*cm, by-0.38*cm, "M-SemiBold", 8, NAVY, "right")
    by -= 0.66*cm
cy_right_end = by

# Fotoğraf şeridi
STRIP_GAP = 0.35*cm
FOOTER_H  = 1*cm
content_end = min(cy_left_end, cy_right_end)
STRIP_H = min(content_end - STRIP_GAP - FOOTER_H - 0.3*cm, 2.0*cm*2+1.5)
row_h = (STRIP_H - 1.5) / 2
strip_y = content_end - STRIP_GAP - STRIP_H

row1 = [f"{GALR}/sl-new-{i}.jpg" for i in [3,5,8,10,14,16]]
row2 = [f"{GALR}/sl-new-{i}.jpg" for i in [1,4,6,9,11,15]]
gw = W/6
for i, p in enumerate(row2): img_box(cv, p, i*gw, strip_y, gw-1.5, row_h, q=85)
for i, p in enumerate(row1): img_box(cv, p, i*gw, strip_y+row_h+1.5, gw-1.5, row_h, q=85)
R(cv, 0, strip_y+STRIP_H, W, 2, fill=GOLD)

footer(cv); cv.showPage()

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 2 — GÜN GÜN PROGRAM
# ══════════════════════════════════════════════════════════════════════════════
R(cv, 0, 0, W, H, fill=CREAM)
R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)

cy = H - 1.3*cm
_, sh = reklame(cv, "Tur Programı", W/2, cy, 22, rgba=(26,23,48,255), align="center")
cy -= sh + 0.15*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

DAYS = [
    (1, "Colombo — Şehir Keşfi", [
        ("Varış",   "İstanbul → Sri Lanka",          "Havalimanı karşılama · Granbell Colombo"),
        ("Öğleden S.", "Tapınak & Şehir Turu",       "Gangaramaya Tapınağı · Galle Face · Pettah"),
        ("Akşam",   "Serbest Akşam",                 "Otel · açık büfe akşam yemeği"),
    ]),
    (2, "Mirissa — Sahil & Deniz", [
        ("Sabah",   "Sahil Treni (2.5 saat)",        "Colombo Fort → Galle · okyanus manzarası"),
        ("Öğle",    "Galle Fort Gezisi",             "UNESCO · Portekiz & Hollanda kale şehri"),
        ("Akşam",   "Mirissa Varış",                 "Mandara Resort veya Paradise Beach Club"),
    ]),
    (3, "Mirissa — Plaj Günü", [
        ("Sabah",   "Serbest Zaman",                 "Mirissa plajı, Coconut Hill, sörf"),
        ("Öğleden S.", "Mavi Balina Turu (EKSTRA)",  "Aralık–Nisan sezonu · +~100 USD"),
        ("Akşam",   "Serbest Akşam",                  "Otel · açık büfe akşam yemeği"),
    ]),
    (4, "Hiriketiya — Koy Keşfi", [
        ("Sabah",   "Mirissa → Hiriketiya (20 dk)",  "Check-in · Seven Turtles veya Hotel Ferola"),
        ("Öğle",    "Koy Keşfi & Serbest",           "At nalı koyu · sörf · yerel kafeler"),
        ("Akşam",   "Serbest Akşam",                  "Otel · açık büfe akşam yemeği"),
    ]),
    (5, "Hiriketiya — Serbest Gün", [
        ("Sabah",   "Açık Hava Aktivitesi",          "Sörf, yüzme veya güneş doğumu yürüyüşü"),
        ("Öğle",    "Serbest Zaman",                 "Sörf, yüzme, dinlenme"),
        ("Akşam",   "Serbest Akşam",                  "Otel · açık büfe akşam yemeği"),
    ]),
    (6, "Safari Günü", [
        ("Sabah",   "Hiriketiya → Safari (2–3 saat)","Yala veya Udawalawe — seçimlik"),
        ("Öğle",    "Safari",                        "Fil, leopar (Yala) · fil sürüsü (Udawalawe)"),
        ("Gece",    "Safari Oteli",                  "Oakray Yala / Chaarya Resorts (Yala seç.)"),
    ]),
    (7, "Dönüş", [
        ("Sabah",   "Kahvaltı & Check-out",          "Son sabah vakti"),
        ("Gündüz",  "Colombo Transferi (~4–5 saat)", "Havalimanı · İstanbul uçuşu"),
    ]),
]

BAR      = 0.68*cm
RH_SUB   = 1.05*cm
RH_NOSUB = 0.74*cm
GAP_DAY  = 0.28*cm
HALF     = (CW - 0.4*cm) / 2
col_assign = [0, 0, 0, 1, 1, 1, 1]
col_x = [LM, LM + HALF + 0.4*cm]
col_y = [cy, cy]

for idx, (num, title, items) in enumerate(DAYS):
    col = col_assign[idx]
    cx  = col_x[col]
    y   = col_y[col]

    R(cv, cx, y-BAR, HALF, BAR, fill=NAVY, r=3)
    T(cv, f"GÜN {num}", cx+0.25*cm, y-0.44*cm, "M-Bold", 7.5, GOLD)
    T(cv, title, cx+HALF-0.2*cm, y-0.44*cm, "M-SemiBold", 7, WHITE, "right",
      max_w=HALF-2.2*cm)

    used = BAR
    for i2, (time_lbl, lbl, sub) in enumerate(items):
        rh = RH_SUB if sub else RH_NOSUB
        row_y = y - used
        bg2 = WARM if i2 % 2 == 0 else WHITE
        R(cv, cx, row_y-rh, HALF, rh, fill=bg2, stroke=BORDER)
        T(cv, time_lbl, cx+0.2*cm, row_y-0.24*cm, "M-Bold", 6, GOLD)
        T(cv, lbl, cx+0.2*cm, row_y-0.47*cm, "M-SemiBold", 8, NAVY, max_w=HALF-0.4*cm)
        if sub:
            T(cv, sub, cx+0.2*cm, row_y-0.74*cm, "M-Light", 7, MUTED, max_w=HALF-0.4*cm)
        used += rh

    col_y[col] -= (used + GAP_DAY)

# Alt bilgi kutusu
BOTTOM_Y = min(col_y) - 0.15*cm
bby = 1*cm + 0.2*cm
BOX_H = BOTTOM_Y - 0.3*cm - bby
if BOX_H >= 1.8*cm:
    R(cv, LM, bby, CW, BOX_H, fill=HexColor("#FDF9F0"), stroke=GOLD, r=5, sw=1)
    R(cv, LM, bby, 5, BOX_H, fill=GOLD)
    highlights = [
        ("Sahil Treni",    "Colombo → Galle · 2.5 saat okyanus manzarası"),
        ("Balina Turu",    "Ekstra · ~100 USD · Aralık–Nisan zirvesi"),
        ("Hiriketiya Koyu","At nalı koy · sörf · wellness atmosferi"),
        ("Safari",         "Yala veya Udawalawe — seçimlik"),
    ]
    item_w = CW / len(highlights)
    iy = bby + BOX_H/2 + 0.2*cm
    for si, (sname, sdesc) in enumerate(highlights):
        sx = LM + si*item_w + item_w/2
        T(cv, sname, sx, iy, "M-Bold", 8.5, NAVY, "center")
        T(cv, sdesc, sx, iy-0.33*cm, "M-Light", 7, MUTED, "center", max_w=item_w-0.3*cm)

footer(cv); cv.showPage()

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 3 — SAFARI KARŞILAŞTIRMASI + OTELLER + KAPSAM
# ══════════════════════════════════════════════════════════════════════════════
R(cv, 0, 0, W, H, fill=CREAM)
R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)

cy = H - 1.3*cm
_, sh = reklame(cv, "Detaylar & Kapsam", W/2, cy, 22, rgba=(26,23,48,255), align="center")
cy -= sh + 0.15*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.5*cm

# ── Safari karşılaştırması ───────────────────────────────────────────────────
reklame(cv, "Safari Seçeneği", LM+CW/2, cy, 14, rgba=(26,23,48,255), align="center")
cy -= 0.75*cm

HALF = (CW - 0.4*cm) / 2
RX2  = LM + HALF + 0.4*cm

SAFARI_BOX_H = 3.6*cm

# Yala
R(cv, LM, cy-SAFARI_BOX_H, HALF, SAFARI_BOX_H, fill=WHITE, stroke=BORDER, r=5)
R(cv, LM, cy-SAFARI_BOX_H, 5, SAFARI_BOX_H, fill=GOLD, r=0)
T(cv, "YALA ULUSAL PARKI",     LM+0.3*cm, cy-0.30*cm, "M-Bold",  9, NAVY)
T(cv, "Sri Lanka'nın 1 numaralı parkı", LM+0.3*cm, cy-0.62*cm, "M-Light", 8, MUTED)
yala_pts = [
    "Leopar yoğunluğu en yüksek (garanti değil)",
    "Fil, timsah, su aygırı, pelikan",
    "Sabah + öğleden sonra 2 safari",
    "Otel: Oakray Yala / Chaarya Resorts",
]
iy = cy - 0.95*cm
for p in yala_pts:
    cv.setFillColor(GOLD); cv.circle(LM+0.4*cm, iy+3, 2, fill=1, stroke=0)
    T(cv, p, LM+0.6*cm, iy, "M-Regular", 8, NAVY, max_w=HALF-0.7*cm); iy -= 0.55*cm

# Udawalawe
R(cv, RX2, cy-SAFARI_BOX_H, HALF, SAFARI_BOX_H, fill=WHITE, stroke=BORDER, r=5)
R(cv, RX2, cy-SAFARI_BOX_H, 5, SAFARI_BOX_H, fill=TEAL, r=0)
T(cv, "UDAWALAWE ULUSAL PARKI", RX2+0.3*cm, cy-0.30*cm, "M-Bold",  9, NAVY)
T(cv, "Fil sürüsü garantili · daha sakin",  RX2+0.3*cm, cy-0.62*cm, "M-Light", 8, MUTED)
udawa_pts = [
    "200+ fil doğal ortamda — garanti",
    "Pinnawala'dan çok daha etik",
    "Sakin, odaklı, küçük park",
    "Hiriketiya'dan Yala'ya yolüstünde",
]
iy2 = cy - 0.95*cm
for p in udawa_pts:
    cv.setFillColor(TEAL); cv.circle(RX2+0.4*cm, iy2+3, 2, fill=1, stroke=0)
    T(cv, p, RX2+0.6*cm, iy2, "M-Regular", 8, NAVY, max_w=HALF-0.7*cm); iy2 -= 0.55*cm

cy -= SAFARI_BOX_H + 0.45*cm
L(cv, LM, cy, RM, cy, BORDER, 0.5)
cy -= 0.45*cm

# ── Oteller ──────────────────────────────────────────────────────────────────
reklame(cv, "Konaklama", LM+CW/2, cy, 14, rgba=(26,23,48,255), align="center")
cy -= 0.75*cm

hotels = [
    ("Colombo",    "1 Gece", "Granbell Colombo",
     "Merkezi konum · modern tasarım"),
    ("Mirissa",    "2 Gece", "Mandara Resort / Paradise Beach Club",
     "Plaja sıfır · okyanus manzarası"),
    ("Hiriketiya", "2 Gece", "Seven Turtles / Hotel Ferola",
     "Hiriketiya koyu · wellness atmosferi"),
    ("Safari",     "1 Gece", "Oakray Yala / Chaarya Resorts",
     "Veya Udawalawe bölge oteli"),
]
HOT_W = CW/4 - 0.2*cm
HOT_H = 2.2*cm
for i, (dest, nights, otel, desc) in enumerate(hotels):
    hx = LM + i*(HOT_W+0.25*cm)
    R(cv, hx, cy-HOT_H, HOT_W, HOT_H, fill=WHITE, stroke=BORDER, r=5)
    R(cv, hx, cy-HOT_H, HOT_W, 0.52*cm, fill=NAVY, r=5)
    R(cv, hx, cy-HOT_H, HOT_W, 0.26*cm, fill=NAVY, r=0)
    T(cv, dest,   hx+HOT_W/2, cy-0.35*cm, "M-Bold",    8, GOLD, "center")
    T(cv, nights, hx+HOT_W/2, cy-0.75*cm, "M-SemiBold", 8, NAVY, "center")
    T(cv, otel,   hx+0.2*cm,  cy-1.15*cm, "M-SemiBold", 7, NAVY, max_w=HOT_W-0.3*cm)
    T(cv, desc,   hx+0.2*cm,  cy-1.65*cm, "M-Light",   6.5, MUTED, max_w=HOT_W-0.3*cm)

cy -= HOT_H + 0.4*cm
L(cv, LM, cy, RM, cy, BORDER, 0.5)
cy -= 0.45*cm

# ── Dahil / Dahil Değil ──────────────────────────────────────────────────────
reklame(cv, "Kapsam", LM+CW/2, cy, 14, rgba=(26,23,48,255), align="center")
cy -= 0.7*cm

BAR2 = 0.56*cm
R(cv, LM,  cy-BAR2, HALF, BAR2, fill=NAVY,               r=3)
R(cv, RX2, cy-BAR2, HALF, BAR2, fill=HexColor("#5a1a1a"), r=3)
T(cv, "+ DAHİL",       LM+0.3*cm,  cy-0.34*cm, "M-Bold", 9, WHITE)
T(cv, "- DAHİL DEĞİL", RX2+0.3*cm, cy-0.34*cm, "M-Bold", 9, WHITE)
cy -= BAR2
ROW = 0.56*cm

INC = [
    "6 gece konaklama (seçili oteller)",
    "Tüm havalimanı – otel transferleri",
    "Sahil treni bileti (Colombo → Galle)",
    "Programda belirtilen geziler",
    "Safari (Yala veya Udawalawe)",
    "6 açık büfe kahvaltı + 6 açık büfe akşam",
]
EXC = [
    "Yurt dışı uçak biletleri (~700 €)",
    "Sri Lanka vizesi (ücretsiz)",
    "Öğle yemekleri",
    "Balina turu (+~100 USD · ekstra)",
    "Kişisel harcamalar",
]

for i in range(max(len(INC), len(EXC))):
    bg_c = WARM if i % 2 == 0 else WHITE
    R(cv, LM,  cy-ROW, HALF, ROW, fill=bg_c, stroke=BORDER)
    if i < len(INC):
        cv.setFillColor(GREEN); cv.circle(LM+0.25*cm, cy-ROW/2+1, 2.5, fill=1, stroke=0)
        T(cv, INC[i], LM+0.42*cm, cy-0.34*cm, "M-Regular", 8, NAVY, max_w=HALF-0.55*cm)
    R(cv, RX2, cy-ROW, HALF, ROW, fill=bg_c, stroke=BORDER)
    if i < len(EXC):
        cv.setFillColor(RED_M); cv.circle(RX2+0.25*cm, cy-ROW/2+1, 2.5, fill=1, stroke=0)
        T(cv, EXC[i], RX2+0.42*cm, cy-0.34*cm, "M-Regular", 8, NAVY, max_w=HALF-0.55*cm)
    cy -= ROW

# CTA kutusu
cy -= 0.3*cm
CTA_H = 1.4*cm
R(cv, LM, cy-CTA_H, CW, CTA_H, fill=NAVY, r=6)
T(cv, "Rezervasyon & Bilgi:", LM+0.4*cm, cy-0.38*cm, "M-Regular", 8.5, GOLD)
T(cv, "lostvoyages.com  ·  WhatsApp: +90 545 170 69 27  ·  @ahmeterenvci",
  LM+0.4*cm, cy-0.78*cm, "M-SemiBold", 9, WHITE)
T(cv, "Şubat–Mart 2027  ·  6 Gece / 7 Gün  ·  Wellness Odaklı Özel Tur",
  LM+0.4*cm, cy-1.1*cm, "M-Light", 7.5, HexColor("#c0b8a0"))

footer(cv); cv.showPage()

cv.save()
print(f"OK: {OUTPUT}  ({os.path.getsize(OUTPUT)//1024} KB)")

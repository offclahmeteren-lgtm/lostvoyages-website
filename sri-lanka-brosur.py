"""
Lost Voyages — Sri Lanka PDF Brochure  v1
8 Gün / 7 Gece · 1.595€ (uçak hariç)
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageEnhance
import io

W, H  = A4
OUTPUT   = "/Users/ahmeterenvci/lostvoyages-website/sri-lanka-brosur.pdf"
HERO_IMG = "/Users/ahmeterenvci/lostvoyages-website/images/srilanka-hero.jpg"
FONTS    = "/Users/ahmeterenvci/lostvoyages-website/fonts"
IMGS     = "/Users/ahmeterenvci/lostvoyages-website/images"

for name, file in [("M-Light","Montserrat-Light"),("M-Regular","Montserrat-Regular"),
                   ("M-SemiBold","Montserrat-SemiBold"),("M-Bold","Montserrat-Bold")]:
    pdfmetrics.registerFont(TTFont(name, f"{FONTS}/{file}.ttf"))

REKLAME = f"{FONTS}/ReklameScript-Medium.otf"

CREAM  = HexColor("#FAF8F4")
NAVY   = HexColor("#1B1730")
GOLD   = HexColor("#C8940E")
WARM   = HexColor("#F2EFE8")
BORDER = HexColor("#E2DDD4")
MUTED  = HexColor("#8A8070")
WHITE  = white
GREEN  = HexColor("#3A7A50")
RED_M  = HexColor("#A03030")

LM = 1.5*cm;  RM = W - 1.5*cm;  CW = RM - LM

# ── Yardımcı fonksiyonlar (Güney Kore ile aynı) ──────────────────────────────
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
            t = (cur+" "+w_).strip()
            if c.stringWidth(t, font, size) <= max_w: cur = t
            else:
                if cur: lines.append(cur)
                cur = w_
        if cur: lines.append(cur)
        for i,ln in enumerate(lines):
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

def L(c, x1,y1,x2,y2, color=BORDER, w=0.5):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(w)
    c.line(x1,y1,x2,y2); c.restoreState()

def img_box(c, path, x, y, w, h, q=88):
    try:
        im = PILImage.open(path).convert("RGB")
        pw, ph = int(w*3), int(h*3)
        s = max(pw/im.width, ph/im.height)
        nw, nh = int(im.width*s), int(im.height*s)
        im = im.resize((nw,nh), PILImage.LANCZOS)
        l=(nw-pw)//2; t=(nh-ph)//2
        im = im.crop((l,t,l+pw,t+ph))
        im = ImageEnhance.Sharpness(im).enhance(1.15)
        buf = io.BytesIO(); im.save(buf,"JPEG",quality=q); buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, w, h)
    except Exception as e: print(f"[img] {path}: {e}")

def reklame(c, text, cx, cy, size, rgba=(200,148,14,255), align="center"):
    px = int(size*3.5)
    try:    fnt = ImageFont.truetype(REKLAME, px)
    except: fnt = ImageFont.load_default()
    dummy = PILImage.new("RGBA",(1,1)); dd=ImageDraw.Draw(dummy)
    bb = dd.textbbox((0,0), text, font=fnt)
    pw, ph = bb[2]-bb[0]+24, bb[3]-bb[1]+24
    im = PILImage.new("RGBA",(pw,ph),(0,0,0,0))
    ImageDraw.Draw(im).text((12-bb[0], 12-bb[1]), text, font=fnt, fill=rgba)
    buf=io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
    ptw, pth = pw/3.5, ph/3.5
    if   align=="center": c.drawImage(ImageReader(buf), cx-ptw/2, cy-pth, ptw, pth, mask="auto")
    elif align=="right":  c.drawImage(ImageReader(buf), cx-ptw,   cy-pth, ptw, pth, mask="auto")
    else:                 c.drawImage(ImageReader(buf), cx,       cy-pth, ptw, pth, mask="auto")
    return ptw, pth

def footer(c):
    R(c, 0, 0, W, 1*cm, fill=NAVY)
    T(c,"lostvoyages.com  ·  iletisim@lostvoyages.com  ·  +90 545 170 69 27  ·  TÜRSAB 9113",
      W/2, 3.5*mm,"M-Regular",6.5,HexColor("#c0b8a0"),"center")

def make_gradient(pw, ph):
    im = PILImage.new("RGBA", (pw, ph), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    for row in range(ph):
        frac = row / ph
        a = int(frac**1.5 * 0.85 * 255)
        draw.line([(0,row),(pw,row)], fill=(26,23,46,a))
    buf=io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
    return ImageReader(buf)

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 1 — KAPAK
# ══════════════════════════════════════════════════════════════════════════════
cv = canvas.Canvas(OUTPUT, pagesize=A4)
R(cv, 0, 0, W, H, fill=CREAM)

HERO_H = H * 0.60
IY     = H - HERO_H

img_box(cv, HERO_IMG, 0, IY, W, HERO_H, q=92)
cv.drawImage(make_gradient(int(W*1.5), int(HERO_H*1.5)), 0, IY, W, HERO_H, mask="auto")

R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)
reklame(cv, "Lost Voyages", W/2, H - 7*mm, 14, rgba=(232,173,24,255), align="center")

reklame(cv, "Sri Lanka", W/2, IY + 7.4*cm, 54, rgba=(255,255,255,255), align="center")

T(cv,"C O L O M B O   ·   S I G I R I Y A   ·   E L L A   ·   G A L L E",
  W/2, IY+4.6*cm,"M-Light",10.5,WHITE,"center")

T(cv,"7 Gece / 8 Gün   ·   Butik Tur   ·   Vizesiz",
  W/2, IY+3.4*cm,"M-Regular",9,HexColor("#E8D898"),"center")

R(cv, 0, IY-5*mm, W, 5*mm, fill=GOLD)

# ── Bilgi alanı ───────────────────────────────────────────────────────────────
INFO_TOP = IY - 5*mm

LCW = CW * 0.50
RCX = LM + LCW + 0.5*cm
RCW = CW - LCW - 0.5*cm
LCX = LM + LCW / 2

cy = INFO_TOP - 0.65*cm

T(cv, "KİŞİ BAŞI FİYAT", LCX, cy, "M-Bold", 7, GOLD, "center")
cy -= 13

_, prh = reklame(cv, "1.595 €", LCX, cy, 38, rgba=(26,23,48,255), align="center")
cy -= prh + 4

T(cv,"butik tur  ·  tüm vergiler dahil", LCX, cy,"M-Light",8,MUTED,"center")
cy -= 14

L(cv, LM+0.2*cm, cy, LM+LCW-0.2*cm, cy, BORDER, 0.6)
cy -= 11

T(cv,"Ön ödeme:", LM+0.2*cm, cy,"M-Regular",8,MUTED)
T(cv,"595 €", LM+2.1*cm, cy,"M-SemiBold",9,NAVY)
cy -= 12

T(cv,"kalan taksitlerle  ·  tek kişilik oda farkı +400 €",
  LM+0.2*cm, cy,"M-Light",7.5,MUTED, max_w=LCW-0.3*cm)
cy -= 10
cy_left_end = cy

# SAĞ KOLON — rozetler
badges = [
    ("Rota",   "Colombo · Sigiriya · Ella · Galle"),
    ("Süre",   "7 Gece / 8 Gün"),
    ("Rehber", "Türkçe Tur Lideri + Yerel Rehber"),
    ("Konak.", "4 Yıldızlı Doğa Otelleri"),
    ("Uçuş",  "Ayrı Satın Alınır — ~700 €"),
]
by = INFO_TOP - 0.2*cm
for lbl, val in badges:
    R(cv, RCX, by-0.62*cm, RCW, 0.60*cm, fill=WHITE, stroke=BORDER, r=3)
    T(cv, lbl.upper(), RCX+0.25*cm, by-0.38*cm,"M-Bold",6.5,GOLD)
    T(cv, val, RCX+RCW-0.25*cm, by-0.38*cm,"M-SemiBold",8,NAVY,"right")
    by -= 0.66*cm
cy_right_end = by

# ── Fotoğraf şeridi ───────────────────────────────────────────────────────────
STRIP_GAP = 0.4*cm
FOOTER_H  = 1*cm
content_end   = min(cy_left_end, cy_right_end)
avail_strip   = content_end - STRIP_GAP - FOOTER_H
ROW_GAP       = 1.5  # pt between rows
STRIP_H_dyn   = min(avail_strip, 2.2*cm * 2 + ROW_GAP)
row_h         = (STRIP_H_dyn - ROW_GAP) / 2
strip_y       = content_end - STRIP_GAP - STRIP_H_dyn

g_imgs_row1 = [f"{IMGS}/gallery/sl-new-{i}.jpg" for i in [3,5,8,10,14,16]]
g_imgs_row2 = [
    f"{IMGS}/gallery/sl-new-1.jpg",
    f"{IMGS}/gallery/sl-stupa.jpg",
    f"{IMGS}/gallery/sl-new-4.jpg",
    f"{IMGS}/gallery/sl-new-15.jpg",
    f"{IMGS}/gallery/sl-new-9.jpg",
    f"{IMGS}/gallery/sl-new-11.jpg",
]
gw = W / 6
# Alt sıra
for i, gp in enumerate(g_imgs_row2):
    img_box(cv, gp, i*gw, strip_y, gw-1.5, row_h, q=85)
# Üst sıra
for i, gp in enumerate(g_imgs_row1):
    img_box(cv, gp, i*gw, strip_y + row_h + ROW_GAP, gw-1.5, row_h, q=85)
R(cv, 0, strip_y + STRIP_H_dyn, W, 2, fill=GOLD)

footer(cv)
cv.showPage()

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 2 — TUR PROGRAMI
# ══════════════════════════════════════════════════════════════════════════════
R(cv, 0, 0, W, H, fill=CREAM)
R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)

cy = H - 1.3*cm
_, sh = reklame(cv, "Tur Programı", W/2, cy, 22, rgba=(26,23,48,255), align="center")
cy -= sh + 0.15*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.5*cm

# ── 8 Günlük program ─────────────────────────────────────────────────────────
DAYS = [
    (1, "Colombo – Dambulla – Sigiriya", [
        ("Varış",          "Sri Lanka'ya Varış",         "Bandaranaike Uluslararası Havalimanı"),
        ("Öğleden Sonra",  "Pinnawala Fil Yetimhanesi",  "Onlarca yabani filin yüzdüğü nehir kıyısı"),
        ("Sonra",          "Dambulla Kaya Tapınakları",  "UNESCO Dünya Mirası"),
        ("Akşam",          "Sigiriya Şehir Turu",        "Geleneksel akşam yemeği & check-in"),
    ]),
    (2, "Sigiriya Kaya Kalesi – Kandy", [
        ("Sabah",          "Sigiriya Kaya Kalesi",       "5. yüzyıl sarayı — 200m yüksekte panorama"),
        ("Öğleden Sonra",  "Kandy Şehrine Yolculuk",     "Çay bahçelerinden manzaralı rota"),
        ("Akşam",          "Kültür Gecesi & Akşam Yemeği","Kandy sokaklarında serbest zaman"),
    ]),
    (3, "Kandy — Diş Tapınağı – Ella Treni", [
        ("Sabah",          "Kutsal Diş Tapınağı",        "Sri Lanka'nın en kutsal Budist mabedi"),
        ("Öğleden Sonra",  "Nuwara Eliya'ya Yolculuk",   "Öğle yemeği, çay tarlaları, dağ manzarası"),
        ("Akşam",          "Ella Tren Yolculuğu",        "Dünyanın en guzel tren hattı — çay & sisler"),
        ("Gece",           "Ella'da Akşam Yemeği",       "Serbest zaman"),
    ]),
    (4, "Ella — Nine Arch Köprüsü – Yala", [
        ("Sabah",          "Dokuz Kemerli Köprü",        "Ella'nın ikonik köprüsü — çay bahçesi manzarası"),
        ("Öğleden Sonra",  "Ravana Şelalesi",            "Sri Lanka'nın en güzel şelalelerinden biri"),
        ("Akşam",          "Yala'ya Transfer",           "Safari kampına varış & dinlenme"),
    ]),
    (5, "Yala Safarisi – Mirissa Sahili", [
        ("Sabah",          "Yala Ulusal Parkı Safarisi", "Leopar, fil, timsah — açık jeepte vahşi yaşam"),
        ("Öğleden Sonra",  "Mirissa'ya Transfer",        "Hint Okyanusu kıyısı, sörf & yüzme"),
        ("Akşam",          "Sahilde Akşam Yemeği",       "Taze deniz mahsulleri"),
    ]),
    (6, "Mirissa — Coconut Hill & Plaj Günü", [
        ("Sabah",          "Coconut Hill Ziyareti",      "Meşhur palmiye salıncağında fotoğraf molası"),
        ("Öğleden Sonra",  "Mirissa Plajı'nda Deniz Keyfi","Sörf, yüzme, dinlenme — tam serbest gün"),
        ("Akşam",          "Birlikte Akşam Yemeği",      "Otele dönüş & serbest zaman"),
    ]),
    (7, "Mirissa – Galle – Colombo", [
        ("Sabah",          "Galle Tarihi Fort Turu",     "UNESCO Dünya Mirası — Portekiz & Hollanda kale şehri"),
        ("Öğleden Sonra",  "Deniz Kaplumbağaları",       "Nesli tehlike altında türlerin üretme merkezi"),
        ("Sonra",          "Colombo Şehir Turu",         "Üstü açık çift katlı otobüs turu"),
        ("Akşam",          "Veda Akşam Yemeği",          "8 günlük maceranın son sofrasına hoş geldin"),
    ]),
    (8, "Colombo – BIA — Dönüş", [
        ("Sabah",          "Otelde Kahvaltı & Check-out",""),
        ("Gün İçi",        "Bandaranaike Havalimanı",    "Istanbul uçusu — gözler kapalı, anılar dolu"),
    ]),
]

BAR      = 0.72*cm
RH_SUB   = 1.10*cm   # Sri Lanka için biraz daha sıkı (8 gün sığsın)
RH_NOSUB = 0.78*cm
GAP_DAY  = 0.30*cm
HALF     = (CW - 0.4*cm) / 2
col_assign = [0, 0, 0, 0, 1, 1, 1, 1]   # 1-4 sol, 5-8 sağ
col_x  = [LM, LM + HALF + 0.4*cm]
col_y  = [cy, cy]

for idx, (num, title, items) in enumerate(DAYS):
    col  = col_assign[idx]
    cx   = col_x[col]
    y    = col_y[col]

    # Gün başlık barı
    R(cv, cx, y-BAR, HALF, BAR, fill=NAVY, r=3)
    T(cv, f"GÜN {num}", cx+0.25*cm, y-0.46*cm,"M-Bold",7.5,GOLD)
    T(cv, title, cx+HALF-0.2*cm, y-0.46*cm,"M-SemiBold",7,WHITE,"right",
      max_w=HALF-2.0*cm)

    used = BAR
    for time_lbl, lbl, sub in items:
        rh = RH_SUB if sub else RH_NOSUB
        row_y = y - used
        bg = WARM if (items.index((time_lbl,lbl,sub)) % 2 == 0) else WHITE
        R(cv, cx, row_y-rh, HALF, rh, fill=bg, stroke=BORDER)
        T(cv, time_lbl, cx+0.2*cm, row_y-0.26*cm,"M-Bold",6,GOLD)
        T(cv, lbl, cx+0.2*cm, row_y-0.50*cm,"M-SemiBold",8,NAVY, max_w=HALF-0.4*cm)
        if sub:
            T(cv, sub, cx+0.2*cm, row_y-0.78*cm,"M-Light",7,MUTED, max_w=HALF-0.4*cm)
        used += rh

    col_y[col] -= (used + GAP_DAY)

# ── Ayurveda & Spice kutusu ───────────────────────────────────────────────────
BOTTOM_Y   = min(col_y) - 0.2*cm
FOOTER_TOP = 1*cm + 2*mm
GAP_ABOVE  = 0.4*cm
bx   = LM
bby  = FOOTER_TOP + 0.15*cm
BOX_H = BOTTOM_Y - GAP_ABOVE - bby
if BOX_H >= 2.0*cm:
    R(cv, bx, bby, CW, BOX_H, fill=HexColor("#FDF9F0"), stroke=GOLD, r=5, sw=1)
    R(cv, bx, bby, 5, BOX_H, fill=GOLD)

    spots = [
        ("Mirissa Butikleri", "El yapımı ürünler & yerel tasarım"),
        ("Çay Fabrikası",     "Nuwara Eliya'da taze çay tadımı"),
        ("Spice Garden",      "Yerli baharat & doğal ürünler"),
    ]
    TITLE_H  = 0.75*cm
    DESC_H   = 0.45*cm
    SPOT_H   = 0.72*cm
    GAP_TD   = 0.18*cm
    GAP_DS   = 0.38*cm
    CONTENT_H = TITLE_H + GAP_TD + DESC_H + GAP_DS + SPOT_H

    content_top = bby + BOX_H/2 + CONTENT_H/2

    reklame(cv, "Alışveriş & Yerel Pazarlar",
            bx + CW/2, content_top, 14, rgba=(26,23,48,255), align="center")
    cur = content_top - TITLE_H - GAP_TD

    T(cv, "Rehberimiz eşliğinde çay fabrikası, baharat bahçesi ve Mirissa butiklerini keşfedin.",
      bx + CW/2, cur, "M-Regular", 8.5, MUTED, "center", max_w=CW-1.2*cm)
    cur -= DESC_H + GAP_DS

    sw3 = CW / 3
    for si, (sname, sdesc) in enumerate(spots):
        sx = bx + si*sw3 + sw3/2
        T(cv, sname, sx, cur, "M-Bold", 8.5, NAVY, "center")
        T(cv, sdesc, sx, cur-0.36*cm, "M-Light", 7.5, MUTED, "center")

footer(cv)
cv.showPage()

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 3 — KAPSAM + ÖDEME + NOTLAR
# ══════════════════════════════════════════════════════════════════════════════
R(cv, 0, 0, W, H, fill=CREAM)
R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)

cy = H - 1.3*cm
_, sh = reklame(cv,"Tur Kapsamı", W/2, cy, 22, rgba=(26,23,48,255), align="center")
cy -= sh + 0.25*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.5*cm

# DAHİL / DAHİL DEĞİL
INC = [
    "7 gece konaklama (4 yıldızlı doğa otelleri)",
    "Tüm transferler & iç ulaşım",
    "Ella Tren bileti (Nuwara Eliya → Ella)",
    "Tur lideri + yerel rehber (tüm program)",
    "Sigiriya Kaya Kalesi giriş bileti",
    "Yala Ulusal Parkı Safarisi",
    "Kandy Diş Tapınağı ziyareti",
    "Kaplumbağa merkezi ziyareti",
    "7 kahvaltı",
    "7 akşam yemeği",
]
EXC = [
    "Uçak biletleri (~700 € · rehber ile aynı uçakta)",
    "30 € yerel ekip bahşişi",
]

HALF = (CW - 0.4*cm) / 2
RX2  = LM + HALF + 0.4*cm

BAR2 = 0.58*cm
R(cv, LM,  cy-BAR2, HALF, BAR2, fill=NAVY,             r=3)
R(cv, RX2, cy-BAR2, HALF, BAR2, fill=HexColor("#6a1a1a"), r=3)
T(cv,"✓  DAHİL",       LM+0.3*cm,  cy-0.36*cm,"M-Bold",9,WHITE)
T(cv,"✕  DAHİL DEĞİL", RX2+0.3*cm, cy-0.36*cm,"M-Bold",9,WHITE)
cy -= BAR2

ROW = 0.62*cm
inc_cy = cy
for i, item in enumerate(INC):
    bg = WARM if i%2==0 else WHITE
    R(cv, LM, inc_cy-ROW, HALF, ROW, fill=bg, stroke=BORDER)
    R(cv, LM, inc_cy-ROW, 3, ROW, fill=GREEN)
    T(cv,"✓", LM+0.2*cm, inc_cy-0.39*cm,"M-Bold",8,GREEN)
    T(cv, item, LM+0.6*cm, inc_cy-0.39*cm,"M-Regular",8,NAVY, max_w=HALF-0.75*cm)
    inc_cy -= ROW

exc_cy = cy
for i, item in enumerate(EXC):
    bg = WARM if i%2==0 else WHITE
    R(cv, RX2, exc_cy-ROW, HALF, ROW, fill=bg, stroke=BORDER)
    R(cv, RX2, exc_cy-ROW, 3, ROW, fill=RED_M)
    T(cv,"✕", RX2+0.2*cm, exc_cy-0.39*cm,"M-Bold",8,RED_M)
    T(cv, item, RX2+0.6*cm, exc_cy-0.39*cm,"M-Regular",8,NAVY, max_w=HALF-0.75*cm)
    exc_cy -= ROW

remaining_h = exc_cy - inc_cy
if remaining_h > 0.5*cm:
    R(cv, RX2, inc_cy, HALF, remaining_h, fill=HexColor("#FFF0F0"), stroke=BORDER)
    R(cv, RX2, inc_cy, 3, remaining_h, fill=RED_M)
    note_cy = inc_cy + remaining_h * 0.62
    T(cv, "Air Arabia veya Qatar Havayolları ile tüm grup aynı uçakta seyahat eder — biletleri adım adım birlikte satın alacağız.",
      RX2+0.4*cm, note_cy, "M-Light", 8.5, MUTED, max_w=HALF-0.6*cm)

cy = min(inc_cy, exc_cy)
cy -= 0.5*cm

# ── KONAKLAMA ─────────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Konaklama", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

for region, desc in [
    ("Sigiriya",  "4 Yıldızlı Doğa Oteli  ·  Ormanın içinde"),
    ("Kandy",     "4 Yıldızlı Şehir Oteli  ·  Dağ & şehir manzarası"),
    ("Ella",      "Butik Otel  ·  Dağların arasında"),
    ("Yala",      "Safari Lodge  ·  Ulusal Park kıyısında"),
    ("Mirissa",   "4 Yıldızlı Sahil Oteli  ·  Hint Okyanusu kıyısında"),
    ("Colombo",   "Lüks Şehir Oteli  ·  Okyanus manzarası"),
]:
    R(cv, LM, cy-0.6*cm, CW, 0.58*cm, fill=WARM, stroke=BORDER)
    R(cv, LM, cy-0.6*cm, 4, 0.58*cm, fill=GOLD)
    T(cv, region.upper(), LM+0.35*cm, cy-0.36*cm,"M-Bold",8,NAVY)
    T(cv, desc, LM+3.0*cm, cy-0.36*cm,"M-Regular",8,MUTED)
    cy -= 0.64*cm

cy -= 0.4*cm

# ── ÖDEME & İPTAL ─────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Ödeme & İptal", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

BOX_H = 1.5*cm
R(cv, LM, cy-BOX_H, CW, BOX_H, fill=NAVY, r=5)
R(cv, LM, cy-BOX_H, 5, BOX_H, fill=GOLD)

_, ph2 = reklame(cv,"1.595 €", LM+0.5*cm, cy-0.12*cm, 26,
                  rgba=(232,173,24,255), align="left")
T(cv,"kişi başı · uçak hariç",  LM+0.5*cm, cy-BOX_H+0.28*cm,"M-Light",8,HexColor("#a09080"))
T(cv,"Ön ödeme: 595 €  ·  kalan geziden 3 hafta önce",
  RM-0.3*cm, cy-0.55*cm,"M-SemiBold",9,WHITE,"right")
T(cv,"Tek kişilik oda farkı: +400 €",
  RM-0.3*cm, cy-BOX_H+0.28*cm,"M-Light",8.5,HexColor("#a09080"),"right")
cy -= BOX_H + 0.5*cm

for item in ["60–30 gün kala yapılan iptallerde 100 € kesinti uygulanır.",
             "30 günden az süre kala yapılan iptallerde kapora iade edilmez."]:
    T(cv, f"— {item}", LM, cy,"M-Light",8,MUTED, max_w=CW)
    cy -= 13

cy -= 0.35*cm

# ── ÖNEMLİ NOTLAR ─────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Önemli Notlar", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

notes = [
    "Sri Lanka vizesi e-Vize ile online alınmaktadır (ücretsiz). Tüm detayları paylaşacağız.",
    "Tur programı yerel trafik ve hava koşullarına göre değişebilir; sıralama korunarak alternatif güzergah uygulanabilir.",
    "Bu tur 9113 TÜRSAB belge no'lu acente ile düzenlenmektedir.",
]
for note in notes:
    R(cv, LM, cy-0.58*cm, CW, 0.56*cm, fill=WARM, stroke=BORDER, r=3)
    T(cv, note, LM+0.3*cm, cy-0.36*cm,"M-Light",8,NAVY, max_w=CW-0.6*cm)
    cy -= 0.62*cm

cy -= 0.5*cm

# ── NEDEN LOST VOYAGES? ───────────────────────────────────────────────────────
_, sh = reklame(cv, "Neden Lost Voyages?", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.4*cm

CARD_H = 2.0*cm
fw = CW / 3
cards = [
    ("VIP Konaklama",
     "Özenle seçilmiş otellerde\nkendini özel hissedeceksin"),
    ("Küçük & Samimi Grup",
     "Kalabalık tur kaosundan uzak,\narkadaş ortamında seyahat"),
    ("Koşuşturmacasız Deneyim",
     "Tüm lojistik bizde —\nsen sadece anını yaşa"),
]
for fi, (title, desc) in enumerate(cards):
    fx = LM + fi * fw
    R(cv, fx+0.12*cm, cy-CARD_H, fw-0.24*cm, CARD_H, fill=WARM, stroke=BORDER, r=5)
    R(cv, fx+0.12*cm, cy-CARD_H, fw-0.24*cm, 3, fill=GOLD)
    T(cv, title, fx+fw/2, cy-0.42*cm, "M-Bold", 8.5, NAVY, "center", max_w=fw-0.5*cm)
    for li, ln in enumerate(desc.split("\n")):
        T(cv, ln, fx+fw/2, cy-0.78*cm-li*0.38*cm, "M-Light", 8, MUTED, "center", max_w=fw-0.5*cm)
cy -= CARD_H + 0.35*cm

# İletişim satırı
T(cv,"lostvoyages.com", LM, cy,"M-Bold",8.5,NAVY)
T(cv,"iletisim@lostvoyages.com", LM+3.5*cm, cy,"M-Regular",8,MUTED)
T(cv,"+90 545 170 69 27", LM+8.5*cm, cy,"M-Regular",8,MUTED)
T(cv,"@ahmeterenvci", RM, cy,"M-Regular",8,MUTED,"right")

footer(cv)
cv.save()
print(f"✓  {OUTPUT}")

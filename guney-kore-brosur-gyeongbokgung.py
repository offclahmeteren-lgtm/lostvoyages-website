"""
Lost Voyages — Güney Kore PDF Brochure  v3
Tüm y-pozisyonları ölçülü; tarihsiz; üst üste binme yok.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageEnhance
import io

W, H = A4          # 595.27 × 841.89 pt
OUTPUT    = "/Users/ahmeterenvci/lostvoyages-website/guney-kore-brosur-gyeongbokgung.pdf"
HERO_IMG  = "/Users/ahmeterenvci/Downloads/kore ads/stock/02_gyeongbokgung.jpg"
FONTS  = "/Users/ahmeterenvci/lostvoyages-website/fonts"
IMGS   = "/Users/ahmeterenvci/lostvoyages-website/images"

# ── Montserrat ────────────────────────────────────────────────────────────────
for name, file in [("M-Light","Montserrat-Light"),("M-Regular","Montserrat-Regular"),
                    ("M-SemiBold","Montserrat-SemiBold"),("M-Bold","Montserrat-Bold")]:
    pdfmetrics.registerFont(TTFont(name, f"{FONTS}/{file}.ttf"))

REKLAME = f"{FONTS}/ReklameScript-Medium.otf"

# ── Renkler ───────────────────────────────────────────────────────────────────
CREAM  = HexColor("#FAF8F4")
NAVY   = HexColor("#1B1730")
GOLD   = HexColor("#C8940E")
GOLD_A = HexColor("#E8AD18")   # açık altın
WARM   = HexColor("#F2EFE8")   # kart arka planı
BORDER = HexColor("#E2DDD4")
MUTED  = HexColor("#8A8070")
WHITE  = white
GREEN  = HexColor("#3A7A50")
RED_M  = HexColor("#A03030")

LM = 1.5*cm;  RM = W - 1.5*cm;  CW = RM - LM

# ══════════════════════════════════════════════════════════════════════════════
# Yardımcı fonksiyonlar
# ══════════════════════════════════════════════════════════════════════════════
def R(c, x, y, w, h, fill=None, stroke=None, r=0, sw=0.5):
    c.saveState(); c.setLineWidth(sw)
    if fill:   c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke)
    kw = dict(fill=1 if fill else 0, stroke=1 if stroke else 0)
    (c.roundRect(x,y,w,h,r,**kw) if r else c.rect(x,y,w,h,**kw))
    c.restoreState()

def T(c, text, x, y, font="M-Regular", size=10, color=NAVY, align="left", max_w=None):
    """Tek satır veya word-wrap. Döner: kullanılan toplam yükseklik (pt)."""
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
    """Kırp-sığdır, 3× supersampling."""
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
    """
    Reklame Script'i PIL ile render et, PDF'e göm.
    cy = metnin ÜSTÜ.  Döner: (pt_w, pt_h)
    """
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

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 1 — KAPAK
# ══════════════════════════════════════════════════════════════════════════════
cv = canvas.Canvas(OUTPUT, pagesize=A4)

# Arka plan
R(cv, 0, 0, W, H, fill=CREAM)

# ── Hero bölgesi ──────────────────────────────────────────────────────────────
HERO_H = H * 0.60          # 505pt ≈ 17.8cm
IY     = H - HERO_H        # 337pt — hero'nun alt kenarı (beyaz alanın üst kenarı)

img_box(cv, HERO_IMG, 0, IY, W, HERO_H, q=92)

# Gradient overlay — PIL ile render (banding yok)
def make_gradient(pw, ph):
    im = PILImage.new("RGBA", (pw, ph), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    for row in range(ph):
        frac = row / ph          # 0=üst(sayfa üstü)→şeffaf, 1=alt(hero alt)→koyu
        a = int(frac**1.5 * 0.82 * 255)
        draw.line([(0,row),(pw,row)], fill=(26,23,46,a))
    buf=io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
    return ImageReader(buf)
cv.drawImage(make_gradient(int(W*1.5), int(HERO_H*1.5)),
             0, IY, W, HERO_H, mask="auto")

# Üstte ince altın bant
R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)

# "Lost Voyages" marka yazısı — hero üstünde
reklame(cv, "Lost Voyages", W/2, H - 7*mm, 14,
        rgba=(232,173,24,255), align="center")

# Büyük tur başlığı — hero ortasında
_, gk_h = reklame(cv, "Güney Kore", W/2, IY + 7.4*cm, 54,
                   rgba=(255,255,255,255), align="center")

# Alt hat
T(cv,"S E U L   ·   G Y E O N G J U   ·   B U S A N",
  W/2, IY+4.6*cm,"M-Light",10.5,WHITE,"center")

T(cv,"5 Gece / 6 Gün   ·   Uçak Dahil   ·   Maks. 20 Kişi",
  W/2, IY+3.4*cm,"M-Regular",9,HexColor("#E8D898"),"center")

# ── Hero altı altın bant ──────────────────────────────────────────────────────
R(cv, 0, IY-5*mm, W, 5*mm, fill=GOLD)

# ── Beyaz bilgi alanı ─────────────────────────────────────────────────────────
# Kullanılabilir alan: IY - 5mm (üst) → 1cm + 2.2cm + 3pt (alt)
# Fotoğraf şeridi + footer aşağıda
STRIP_H   = 2.2*cm
STRIP_TOP = 1*cm + STRIP_H + 3      # fotoğraf şeridinin üst y koordinatı
INFO_TOP  = IY - 5*mm               # bilgi alanı başlangıcı (y)
INFO_BOT  = STRIP_TOP + 0.25*cm     # bilgi alanı sonu (y)

# SOL KOLON — fiyat bloğu
LCW = CW * 0.50          # eşit ağırlık
RCX = LM + LCW + 0.5*cm
RCW = CW - LCW - 0.5*cm
LCX = LM + LCW / 2       # sol kolonun merkezi (yatay)

# Sol içerik yüksekliği: sağ kolon ile aynı başlangıca hizala
# Sağ: by = INFO_TOP - 0.2cm → ilk rozet üstü INFO_TOP - 0.82cm
# Sol: aynı görsel ağırlık için üst padding 0.2cm
cy = INFO_TOP - 0.65*cm

T(cv, "KİŞİ BAŞI FİYAT", LCX, cy, "M-Bold", 7, GOLD, "center")
cy -= 13

_, prh = reklame(cv, "3.095 €", LCX, cy, 38,
                  rgba=(26,23,48,255), align="center")
cy -= prh + 4

# "uçak dahil" → fiyatın altında ortalı
T(cv,"uçak dahil  ·  tüm vergiler dahil", LCX, cy,"M-Light",8,MUTED,"center")
cy -= 14

L(cv, LM+0.2*cm, cy, LM+LCW-0.2*cm, cy, BORDER, 0.6)
cy -= 11

# Ön ödeme satırı — düzenli iki sütun
T(cv,"Ön ödeme:", LM+0.2*cm, cy,"M-Regular",8,MUTED)
T(cv,"1.095 €",  LM+2.1*cm, cy,"M-SemiBold",9,NAVY)
cy -= 12

T(cv,"kalan taksitlerle  ·  tek kişilik oda farkı +400 €",
  LM+0.2*cm, cy,"M-Light",7.5,MUTED, max_w=LCW-0.3*cm)
cy -= 10
cy_left_end = cy   # sol içerik sonu

# SAĞ KOLON — bilgi rozetleri
badges = [
    ("Rota",    "Seul · Gyeongju · Busan"),
    ("Süre",    "5 Gece / 6 Gün"),
    ("Rehber",  "Korece & Türkçe Tur Lideri"),
    ("Konak.",  "4 Yıldızlı Oteller"),
    ("Uçak",    "Dahil — İstanbul – Seul"),
]
by = INFO_TOP - 0.2*cm
for lbl, val in badges:
    R(cv, RCX, by-0.62*cm, RCW, 0.60*cm, fill=WHITE, stroke=BORDER, r=3)
    T(cv, lbl.upper(), RCX+0.25*cm, by-0.38*cm,"M-Bold",6.5,GOLD)
    T(cv, val, RCX+RCW-0.25*cm, by-0.38*cm,"M-SemiBold",8,NAVY,"right")
    by -= 0.66*cm
cy_right_end = by   # sağ içerik sonu

# ── Fotoğraf şeridi — içeriğin hemen altına dinamik konumlanır ────────────────
STRIP_GAP  = 0.4*cm
FOOTER_H   = 1*cm
content_end = min(cy_left_end, cy_right_end)  # iki kolunun daha aşağısı
avail_strip = content_end - STRIP_GAP - FOOTER_H
STRIP_H_dyn = min(avail_strip, 2.8*cm)        # mevcut alanı doldur, max 2.8cm
strip_y = content_end - STRIP_GAP - STRIP_H_dyn

g_imgs = [f"{IMGS}/gallery/kore-0{i}.jpg" for i in [2,3,4,5,6,7]]
gw = W / len(g_imgs)
for i, gp in enumerate(g_imgs):
    img_box(cv, gp, i*gw, strip_y, gw-1.5, STRIP_H_dyn, q=85)

R(cv, 0, strip_y + STRIP_H_dyn, W, 2, fill=GOLD)

footer(cv)
cv.showPage()

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 2 — PROGRAM
# ══════════════════════════════════════════════════════════════════════════════
R(cv, 0, 0, W, H, fill=CREAM)
R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)

cy = H - 1.3*cm
_, sh = reklame(cv,"Tur Programı", W/2, cy, 22, rgba=(26,23,48,255), align="center")
cy -= sh + 0.25*cm
L(cv, LM, cy, RM, cy, GOLD, 1.2)
cy -= 0.55*cm

DAYS = [
    ("1","✈","İstanbul → Seul",[
        ("Gündüz", "İstanbul'dan Kalkış",  "Seul Incheon Uluslararası Havalimanına uçuş"),
        ("Varış",  "Incheon & Otel",        "Rehber karşılama · Check-in · Serbest zaman"),
    ]),
    ("2","🏯","Seul — Saraylar & N Kulesi",[
        ("Sabah",     "Gyeongbokgung Sarayı",  "Joseon Hanedanlığı'nın en büyük sarayı"),
        ("Öğle Önc.", "Hanbok Deneyimi",        "Geleneksel kıyafetle saray fotoğrafı"),
        ("Öğle Son.", "Bukchon Hanok Köyü",     "Tarihi geleneksel Kore evleri"),
        ("Akşam",     "N Seul Kulesi",          "360° Seul panoraması, gece ışıkları"),
    ]),
    ("3","🍃","Nami Adası & Morning Calm",[
        ("Sabah",     "Nami Adası",              "Feribotla ulaşılan romantik ada"),
        ("Öğle Son.", "Garden of Morning Calm",  "Kore'nin en güzel botanik bahçesi"),
        ("Akşam",     "Seul'e Dönüş",            "Serbest zaman"),
    ]),
    ("4","🚄","KTX ile Gyeongju",[
        ("Sabah",     "KTX Seul → Gyeongju",         "~2 saat · 300 km hızlı tren"),
        ("Öğle Son.", "Bulguksa Tapınağı",             "UNESCO Dünya Mirası"),
        ("Sonra",     "Seokguram & Cheomseongdae",     "Dev Buda heykeli · En eski astronomi gözlemevi"),
        ("Akşam",     "Donggung & Wolji Gölü",         "Gece yansımalarıyla muhteşem"),
    ]),
    ("5","🌊","Busan — Deniz & Sky Capsule",[
        ("Sabah",     "Gyeongju → Busan",           "~1,5 saat transfer"),
        ("Öğle Önc.", "Ahopsan Bambu Ormanı",        "Yüzyıllardır korunan özel bambu ormanı"),
        ("Öğle Son.", "Haedong Yonggungsa",           "Kayalık kıyıda Budist tapınağı"),
        ("Akşam",     "Haeundae Sky Capsule",         "Okyanus manzaralı cam kapsülde gün batımı"),
    ]),
    ("6","🎬","Busan Turu & Dönüş",[
        ("Sabah",     "Gamcheon Kültür Köyü",         "Rengarenk teraslı sanat köyü"),
        ("Öğle Önc.", "BIFF & Jagalchi Pazarı",       "Kore'nin en büyük deniz ürünleri pazarı"),
        ("Öğle Son.", "KTX Busan → Incheon",           "~2,5 saat · Havalimanına transfer"),
        ("Gece",      "İstanbul'a Dönüş Uçuşu",       "Kore anılarıyla dolu bavullar"),
    ]),
]

COL_W = (CW - 0.6*cm) / 2
COL_X = [LM, LM + COL_W + 0.6*cm]
# Kolon dengesi: sol 1+2+4, sağ 3+5+6  (yaklaşık eşit yükseklik)
col_assign = [0, 0, 0, 1, 1, 1]
col_y = [cy, cy]
BAR = 0.72*cm
RH_SUB  = 1.18*cm
RH_NOSUB = 0.82*cm
GAP_DAY = 0.38*cm

for idx, (num, emoji, title, items) in enumerate(DAYS):
    col = col_assign[idx]
    cx  = COL_X[col]
    y   = col_y[col]

    R(cv, cx, y-BAR, COL_W, BAR, fill=NAVY, r=3)
    T(cv, f"GÜN {num}", cx+0.25*cm, y-0.46*cm,"M-Bold",7.5,GOLD)
    t = title if cv.stringWidth(title,"M-SemiBold",8) < COL_W-2.8*cm else title[:24]+"…"
    T(cv, t, cx+COL_W-0.25*cm, y-0.46*cm,"M-SemiBold",8,WHITE,"right")
    used = BAR

    for tlbl, label, sub in items:
        RH = RH_SUB if sub else RH_NOSUB
        ry = y - used
        R(cv, cx, ry-RH, COL_W, RH, fill=WHITE, stroke=BORDER)
        R(cv, cx, ry-RH, 3, RH, fill=GOLD_A)
        T(cv, tlbl,  cx+0.22*cm, ry-0.28*cm,"M-Bold",6,GOLD)
        T(cv, label, cx+0.22*cm, ry-0.54*cm,"M-SemiBold",8.5,NAVY, max_w=COL_W-0.35*cm)
        if sub:
            T(cv, sub, cx+0.22*cm, ry-0.84*cm,"M-Light",7.5,MUTED, max_w=COL_W-0.35*cm)
        used += RH

    col_y[col] -= (used + GAP_DAY)

# K-Beauty kutusu — kolonların hemen altından footer'a kadar
BOTTOM_Y  = min(col_y) - 0.2*cm
FOOTER_TOP = 1*cm + 2*mm
GAP_ABOVE = 0.4*cm
bx  = LM
bby = FOOTER_TOP + 0.15*cm          # kutunun alt kenarı (footer hizası)
BOX_H = BOTTOM_Y - GAP_ABOVE - bby  # kutunun tam yüksekliği
if BOX_H >= 2.0*cm:
    R(cv, bx, bby, CW, BOX_H, fill=HexColor("#FDF9F0"), stroke=GOLD, r=5, sw=1)
    R(cv, bx, bby, 5, BOX_H, fill=GOLD)

    # ── içerik yüksekliğini hesapla, dikey ortala ───────────────────────
    spots = [
        ("Myeongdong",   "Kore'nin en büyük kozmetik caddesi"),
        ("Olive Young",  "Ulusal zincir — 1.800+ marka"),
        ("Apgujeong",    "Lüks & bağımsız tasarımcılar"),
    ]
    TITLE_H  = 0.80*cm   # Reklame 15pt ≈ 0.8cm
    DESC_H   = 0.45*cm   # tek satır açıklama
    SPOT_H   = 0.75*cm   # spot başlık + alt yazı
    GAP_TD   = 0.20*cm   # title→desc arası
    GAP_DS   = 0.40*cm   # desc→spots arası
    CONTENT_H = TITLE_H + GAP_TD + DESC_H + GAP_DS + SPOT_H

    # dikey ortalama: içeriğin üstü kutunun ortasından CONTENT_H/2 yukarıda
    content_top = bby + BOX_H/2 + CONTENT_H/2

    _, _ = reklame(cv, "K-Beauty & Kozmetik Alışverişi",
                   bx + CW/2, content_top, 15, rgba=(26,23,48,255), align="center")
    cur = content_top - TITLE_H - GAP_TD

    T(cv, "Rehberimiz eşliğinde Kore kozmetik dünyasını keşfedin — markalı ürünler, cilt bakım sırları ve özel indirimler.",
      bx+0.6*cm, cur, "M-Regular", 8.5, MUTED, max_w=CW-1.2*cm)
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

# ── TUR KAPSAMI ───────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Tur Kapsamı", W/2, cy, 22, rgba=(26,23,48,255), align="center")
cy -= sh + 0.25*cm
L(cv, LM, cy, RM, cy, GOLD, 1.2)
cy -= 0.55*cm

INC = ["Uçak biletleri (gidiş-dönüş, İstanbul – Seul)",
       "5 gece 4 yıldızlı otel",
       "Tüm transferler & ulaşım",
       "KTX tren biletleri",
       "Korece & Türkçe bilen tur lideri",
       "Yerel rehber (tüm program)",
       "Tüm giriş ücretleri",
       "Nami Adası feribot bileti",
       "Sky Capsule bileti",
       "5 kahvaltı",
       "5 öğle yemeği"]
EXC = ["Akşam yemekleri",
       "Kişisel harcamalar"]

HALF = (CW - 0.4*cm) / 2
RX2  = LM + HALF + 0.4*cm

# Başlık barları
BAR2 = 0.58*cm
R(cv, LM,  cy-BAR2, HALF, BAR2, fill=NAVY,             r=3)
R(cv, RX2, cy-BAR2, HALF, BAR2, fill=HexColor("#6a1a1a"), r=3)
T(cv,"✓  DAHİL",       LM+0.3*cm,  cy-0.36*cm,"M-Bold",9,WHITE)
T(cv,"✕  DAHİL DEĞİL", RX2+0.3*cm, cy-0.36*cm,"M-Bold",9,WHITE)
cy -= BAR2

ROW = 0.62*cm
# Sol kolon (INC) ve sağ kolon (EXC) bağımsız çiziliyor — boş satır yok
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

# Sağ kolon EXC kısa kaldığında geri kalan alanı not kutusuyla doldur
remaining_h = exc_cy - inc_cy
if remaining_h > 0.5*cm:
    R(cv, RX2, inc_cy, HALF, remaining_h, fill=HexColor("#FFF0F0"), stroke=BORDER)
    R(cv, RX2, inc_cy, 3, remaining_h, fill=RED_M)
    note_cx = RX2 + 0.4*cm
    note_cy = inc_cy + remaining_h * 0.62  # dikey olarak yaklaşık ortala
    T(cv, "Akşam yemekleri kişisel bütçenize aittir — Kore'nin eşsiz sokak lezzetlerini özgürce keşfedin!",
      note_cx, note_cy, "M-Light", 8.5, MUTED, max_w=HALF-0.6*cm)

cy = min(inc_cy, exc_cy)

cy -= 0.5*cm

# ── KONAKLAMA ─────────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Konaklama", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

for city, desc in [
    ("Seul",     "Ibis Styles Ambassador Yongsan veya eşdeğeri  ·  Şehir merkezinde"),
    ("Gyeongju", "Kolon Hotel veya eşdeğeri  ·  Tarihi alana yürüme mesafesinde"),
    ("Busan",    "Asti Hotel veya eşdeğeri  ·  Haeundae sahilinde"),
]:
    R(cv, LM, cy-0.68*cm, CW, 0.66*cm, fill=WHITE, stroke=BORDER, r=3)
    R(cv, LM, cy-0.68*cm, 4, 0.66*cm, fill=GOLD)
    T(cv, city.upper(),     LM+0.35*cm, cy-0.42*cm,"M-Bold",8.5,NAVY)
    T(cv, desc, LM+2.6*cm, cy-0.42*cm,"M-Regular",8,MUTED, max_w=CW-2.8*cm)
    cy -= 0.72*cm

cy -= 0.5*cm

# ── ÖDEME & İPTAL ─────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Ödeme & İptal", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

# Fiyat kutusu
BOX_H = 1.5*cm
R(cv, LM, cy-BOX_H, CW, BOX_H, fill=NAVY, r=5)
R(cv, LM, cy-BOX_H, 5, BOX_H, fill=GOLD)

_, ph2 = reklame(cv,"3.095 €", LM+0.5*cm, cy-0.12*cm, 26,
                  rgba=(232,173,24,255), align="left")
T(cv,"kişi başı · uçak dahil",  LM+0.5*cm, cy-BOX_H+0.28*cm,"M-Light",8,HexColor("#a09080"))
T(cv,"Ön ödeme: 1.095 €  ·  kalan aylık ödemelerle",
  RM-0.3*cm, cy-0.55*cm,"M-SemiBold",9,WHITE,"right")
T(cv,"Tek kişilik oda farkı: +400 €",
  RM-0.3*cm, cy-BOX_H+0.28*cm,"M-Light",8.5,HexColor("#a09080"),"right")
cy -= BOX_H + 0.2*cm

for item in ["60–30 gün kala yapılan iptallerde 100 € kesinti uygulanır.",
             "30 günden az süre kala yapılan iptallerde kapora iade edilmez."]:
    T(cv,f"—  {item}", LM+0.3*cm, cy-0.15*cm,"M-Regular",8.5,MUTED, max_w=CW-0.5*cm)
    cy -= 0.52*cm

cy -= 0.5*cm

# ── ÖNEMLİ NOTLAR ─────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Önemli Notlar", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

for note in [
    "Güney Kore'ye giriş için K-ETA (Elektronik Seyahat İzni) gereklidir. Başvuru ücretsizdir — tüm detayları paylaşacağız.",
    "Tur programı yerel trafik ve hava koşullarına göre değişebilir; sıralama korunarak alternatif güzergah uygulanabilir.",
    "Bu tur 9113 TÜRSAB belge no'lu acente ile düzenlenmektedir.",
]:
    R(cv, LM, cy-0.68*cm, CW, 0.66*cm, fill=WARM, stroke=BORDER, r=3)
    T(cv, note, LM+0.3*cm, cy-0.42*cm,"M-Light",8,NAVY, max_w=CW-0.5*cm)
    cy -= 0.72*cm

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

# ── İLETİŞİM ─────────────────────────────────────────────────────────────────
L(cv, LM, cy, RM, cy, BORDER, 0.5)
cy -= 0.55*cm

for i,(val,fnt,col) in enumerate([
    ("lostvoyages.com",          "M-SemiBold", NAVY),
    ("iletisim@lostvoyages.com", "M-Regular",  MUTED),
    ("+90 545 170 69 27",        "M-Regular",  MUTED),
    ("@ahmeterenvci",            "M-Regular",  MUTED),
]):
    sx = LM + i*(CW/4) + (CW/4)/2
    T(cv, val, sx, cy, fnt, 8.5, col, "center")

footer(cv)
cv.showPage()
cv.save()
print(f"✓  {OUTPUT}")

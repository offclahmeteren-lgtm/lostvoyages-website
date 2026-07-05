"""
Lost Voyages — Mısır PDF Broşürü
Zanzibar / Güney Kore broşürüyle aynı stil: krem zemin, Montserrat + ReklameScript.
Tarihsiz versiyon.
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

W, H = A4
OUTPUT   = "/Users/ahmeterenvci/lostvoyages-website/misir-brosur.pdf"
HERO_IMG = "/Users/ahmeterenvci/lostvoyages-website/images/gallery/eg-2.jpg"
FONTS    = "/Users/ahmeterenvci/lostvoyages-website/fonts"
IMGS     = "/Users/ahmeterenvci/lostvoyages-website/images"

# ── Fontlar ────────────────────────────────────────────────────────────────────
for name, file in [("M-Light","Montserrat-Light"),("M-Regular","Montserrat-Regular"),
                    ("M-SemiBold","Montserrat-SemiBold"),("M-Bold","Montserrat-Bold")]:
    pdfmetrics.registerFont(TTFont(name, f"{FONTS}/{file}.ttf"))

REKLAME = f"{FONTS}/ReklameScript-Medium.otf"

# ── Renkler ────────────────────────────────────────────────────────────────────
CREAM  = HexColor("#FAF8F4")
NAVY   = HexColor("#1B1730")
GOLD   = HexColor("#C8940E")
GOLD_A = HexColor("#E8AD18")
WARM   = HexColor("#F2EFE8")
BORDER = HexColor("#E2DDD4")
MUTED  = HexColor("#8A8070")
WHITE  = white
GREEN  = HexColor("#3A7A50")
RED_M  = HexColor("#A03030")
SAND   = HexColor("#C4831A")

LM = 1.5*cm;  RM = W - 1.5*cm;  CW = RM - LM

# ── Yardımcı fonksiyonlar ──────────────────────────────────────────────────────
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
      W/2, 4.2*mm,"M-Regular",6.5,HexColor("#c0b8a0"),"center")

# ══════════════════════════════════════════════════════════════════════════════
# SAYFA 1 — KAPAK
# ══════════════════════════════════════════════════════════════════════════════
cv = canvas.Canvas(OUTPUT, pagesize=A4)

R(cv, 0, 0, W, H, fill=CREAM)

HERO_H = H * 0.60
IY     = H - HERO_H

img_box(cv, HERO_IMG, 0, IY, W, HERO_H, q=92)

def make_gradient(pw, ph):
    im = PILImage.new("RGBA", (pw, ph), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    for row in range(ph):
        frac = row / ph
        a = int(frac**1.5 * 0.80 * 255)
        draw.line([(0,row),(pw,row)], fill=(26,23,46,a))
    buf=io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
    return ImageReader(buf)

cv.drawImage(make_gradient(int(W*1.5), int(HERO_H*1.5)), 0, IY, W, HERO_H, mask="auto")

R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)
reklame(cv, "Lost Voyages", W/2, H - 7*mm, 14, rgba=(232,173,24,255), align="center")

_, gk_h = reklame(cv, "Mısır", W/2, IY + 7.4*cm, 54, rgba=(255,255,255,255), align="center")

T(cv,"K A H İ R E   ·   F E Y Y U M   ·   G İ Z A   ·   H U R G A D A   ·   L U K S O R",
  W/2, IY+4.6*cm,"M-Light",9.5,WHITE,"center")

T(cv,"5 Gece / 6 Gün   ·   Uçak Dahil   ·   Maks. 20 Kişi",
  W/2, IY+3.4*cm,"M-Regular",9,HexColor("#E8D898"),"center")

R(cv, 0, IY-5*mm, W, 5*mm, fill=GOLD)

# ── Bilgi alanı ───────────────────────────────────────────────────────────────
INFO_TOP = IY - 5*mm

LCW = CW * 0.50
RCX = LM + LCW + 0.5*cm
RCW = CW - LCW - 0.5*cm
LCX = LM + LCW / 2

cy = INFO_TOP - 0.65*cm
T(cv, "TOPLAM TAHMİNİ BÜTÇE", LCX, cy, "M-Bold", 7, GOLD, "center")
cy -= 13

_, prh = reklame(cv, "~1.490 €", LCX, cy, 38, rgba=(26,23,48,255), align="center")
cy -= prh + 4

T(cv,"uçak dahil · tüm vergiler dahil", LCX, cy,"M-Light",8,MUTED,"center")
cy -= 14

L(cv, LM+0.2*cm, cy, LM+LCW-0.2*cm, cy, BORDER, 0.6)
cy -= 11

T(cv,"Tur fiyatı:", LM+0.2*cm, cy,"M-Regular",8,MUTED)
T(cv,"1.250 €",    LM+2.2*cm, cy,"M-SemiBold",9,NAVY)
cy -= 12

T(cv,"Ön ödeme: 595 €  ·  tek kişilik oda farkı +400 €",
  LM+0.2*cm, cy,"M-Light",7.5,MUTED, max_w=LCW-0.3*cm)
cy -= 10
cy_left_end = cy

badges = [
    ("Rota",    "Kahire · Feyyum · Giza · Hurgada · Luksor"),
    ("Süre",    "5 Gece / 6 Gün"),
    ("Rehber",  "Türkçe Tur Lideri + Yerel Rehber"),
    ("Konak.",  "Kahire 4★ (3G) & Hurgada 4★ Her Şey Dahil (2G)"),
    ("Uçak",    "Dahil — İstanbul ↔ Kahire/Hurgada"),
]
by = INFO_TOP - 0.2*cm
for lbl, val in badges:
    R(cv, RCX, by-0.62*cm, RCW, 0.60*cm, fill=WHITE, stroke=BORDER, r=3)
    T(cv, lbl.upper(), RCX+0.25*cm, by-0.38*cm,"M-Bold",6.5,GOLD)
    T(cv, val, RCX+RCW-0.25*cm, by-0.38*cm,"M-SemiBold",7.5,NAVY,"right")
    by -= 0.66*cm
cy_right_end = by

STRIP_GAP  = 0.4*cm
FOOTER_H   = 1*cm
content_end = min(cy_left_end, cy_right_end)
avail_strip = content_end - STRIP_GAP - FOOTER_H
STRIP_H_dyn = min(avail_strip, 2.8*cm)
strip_y = content_end - STRIP_GAP - STRIP_H_dyn

g_imgs = [f"{IMGS}/gallery/eg-{i}.jpg" for i in [1,3,4,5]]
g_imgs.append(f"{IMGS}/gallery/eg-2.jpg")
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
    ("1","✈","İstanbul → Kahire Gece Uçuşu",[
        ("Hareket",  "İstanbul Havalimanı'nda Buluşma", "Tur liderimizle tanışıp check-in ve pasaport işlemlerini tamamlıyoruz"),
        ("Gece",     "Kahire'ye Varış & Otele Transfer", "Gece geç saatlerde Kahire'ye iniyoruz; özel araçla otele geçiyor, dinleniyoruz"),
    ]),
    ("2","🏜️","Feyyum — Çöl Safarisi & Vaha Keşfi",[
        ("Sabah",     "Kahvaltı & Feyyum'a Hareket",              "Mısır'ın en büyük vahası Feyyum'a yola çıkıyoruz"),
        ("Gün İçi",  "Tunus Köyü — Çömlek Atölyeleri",           "Geleneksel çömlek ustalarının yaşadığı otantik Mısır köyünü geziyoruz"),
        ("Gün İçi",  "4x4 Safari — El-Mudavvara & Wadi El-Rayan","Çölde off-road heyecanı — kayalık platolardan Mısır'ın nadir çöl şelalelerine"),
        ("Öğle Son.","Sihirli Göl & Kum Kayağı",                  "Çölün ortasında turkuaz vaha gölü; kum tepelerinde sandboarding"),
        ("Akşam",    "Bedevi Akşam Yemeği & Kahire'ye Dönüş",    "Yıldızların altında geleneksel Bedevi sofrası"),
    ]),
    ("3","🕌","Kahire — Kaleler, Camiler, Nil & Çarşı",[
        ("Sabah",     "Selahaddin Kalesi & Mehmet Ali Paşa Camii","Kahire'ye tepeden bakan tarihi kale; Osmanlı mimarisinin şaheseri cami"),
        ("Gün İçi",  "İbn Tolun Camii & El-Muiz Caddesi",        "9. yüzyıldan kalma cami; İslam mimarisinin en güzel örneklerinin sıralandığı cadde"),
        ("Öğle Son.","Nil Nehri Tekne Gezisi",                    "Nil üzerinde manzaralı tekne turu"),
        ("Akşam Üz.","Fişavi Kafesi & Han el-Halili Çarşısı",    "Yüzyıllık tarihi kafe (Mehmet Akif Ersoy'un uğrak yeri); tarihi çarşıda alışveriş"),
    ]),
    ("4","🏺","Giza Piramitleri & Büyük Mısır Müzesi",[
        ("Sabah",     "Giza Piramitleri & Büyük Sfenks",  "Dünyanın Yedi Harikası'ndan hayatta kalan tek yapı — Keops, Kefren, Mikerinos"),
        ("Öğle Son.","Büyük Mısır Müzesi (GEM)",          "Tutankhamun'un altın maskesi ve hazinelerine ev sahipliği yapan dev müze"),
        ("Akşam",    "Otobüsle Hurgada'ya Transfer",      "Kızıldeniz kıyısına doğru yola çıkıyor, Hurgada'daki otelimize yerleşiyoruz"),
    ]),
    ("5","🤿","Hurgada — Kızıldeniz Şnorkel & Dalış",[
        ("Sabah",     "Kahvaltı & Yata Biniş",                    "Bugün tamamen deniz günü — Kızıldeniz'e açılıyoruz"),
        ("Gün Boy.", "Şnorkel Yat Turu — 2 Tanıtım Tüplü Dalış", "Mercan resifleri, tropikal balıklar ve kristal Kızıldeniz; eğitimli rehber eşliğinde dalış"),
        ("Öğle",     "Tekne Üzerinde Öğle Yemeği",               "Açık denizde taze deniz mahsulleriyle öğle molası"),
        ("Akşam",    "Otele Dönüş & Serbest Zaman",              "Sahil veya havuz keyfinde serbest akşam"),
    ]),
    ("6","⚱️","Luksor Günübirlik — Kranlar & Tapınaklar",[
        ("Sabah",    "Kahvaltı & Luksor'a Hareket",               "Nil kıyısındaki antik başkente doğru yola çıkıyoruz"),
        ("Gün İçi", "Krallar Vadisi",                             "Tutankhamun, Ramses, Seti — firavunların binlerce yıl uyuduğu mezar odaları"),
        ("Gün İçi", "Karnak & Luksor Tapınağı",                  "Dünyanın en büyük antik tapınak alanı; sfenks yolu ve Nil kıyısındaki görkemli tapınak"),
        ("Öğle",    "Öğle Yemeği & Hurgada Havalimanı ✈",       "Öğlenin ardından Hurgada Havalimanı'na geçiyor, İstanbul uçuşumuza biniyoruz"),
    ]),
]

COL_W = (CW - 0.6*cm) / 2
COL_X = [LM, LM + COL_W + 0.6*cm]
col_assign = [0, 0, 0, 1, 1, 1]
col_y = [cy, cy]
BAR      = 0.72*cm
RH_SUB   = 1.18*cm
RH_NOSUB = 0.82*cm
GAP_DAY  = 0.28*cm

for idx, (num, emoji, title, items) in enumerate(DAYS):
    col = col_assign[idx]
    cx  = COL_X[col]
    y   = col_y[col]

    R(cv, cx, y-BAR, COL_W, BAR, fill=NAVY, r=3)
    T(cv, f"GÜN {num}", cx+0.25*cm, y-0.46*cm,"M-Bold",7.5,GOLD)
    t = title if cv.stringWidth(title,"M-SemiBold",8) < COL_W-2.8*cm else title[:26]+"…"
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

BOTTOM_Y   = min(col_y) - 0.2*cm
FOOTER_TOP = 1*cm + 2*mm
GAP_ABOVE  = 0.4*cm
bby        = FOOTER_TOP + 0.15*cm
BOX_H      = BOTTOM_Y - GAP_ABOVE - bby
if BOX_H >= 1.8*cm:
    R(cv, LM, bby, CW, BOX_H, fill=HexColor("#FFF8EE"), stroke=GOLD, r=5, sw=1)
    R(cv, LM, bby, 5, BOX_H, fill=GOLD)
    highlights = [
        ("Feyyum 4x4 Safari",     "Çöl, şelale, sihirli göl"),
        ("Giza & GEM",            "Piramitler & altın hazineler"),
        ("Kızıldeniz Dalışı",     "Mercan resifleri, 2 tüp dalış"),
    ]
    TITLE_H = 0.75*cm
    SPOT_H  = 0.65*cm
    CONTENT_H = TITLE_H + 0.2*cm + SPOT_H
    content_top = bby + BOX_H/2 + CONTENT_H/2
    reklame(cv, "Öne Çıkan Deneyimler", LM+CW/2, content_top, 13,
            rgba=(26,23,48,255), align="center")
    cur = content_top - TITLE_H - 0.15*cm
    sw3 = CW / 3
    for si, (sname, sdesc) in enumerate(highlights):
        sx = LM + si*sw3 + sw3/2
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
L(cv, LM, cy, RM, cy, GOLD, 1.2)
cy -= 0.55*cm

INC = [
    "İstanbul ↔ Mısır gidiş-dönüş uçuşları",
    "Türkçe tur lideri & yerel rehber (tüm program)",
    "Kahire'de 4★ otelde 3 gece oda-kahvaltı",
    "Hurgada'da 4★ otelde 2 gece her şey dahil",
    "Havalimanı karşılama ve uğurlama",
    "Tüm transferler (özel klimalı araç)",
    "Tüm giriş biletleri ve gezi turları",
    "Feyyum 4x4 safari, Wadi El-Rayan, Magic Lake & sandboarding",
    "Bedevi akşam yemeği (Feyyum)",
    "Kahire şehir turu — kale, camiler, Nil tekne turu, çarşı",
    "Giza Piramitleri & Büyük Mısır Müzesi (GEM)",
    "Hurgada şnorkel yat turu (tekne öğle yemeği dahil, 2 tanıtım dalışı)",
    "Luksor turu — Krallar Vadisi, Karnak, Luksor Tapınağı",
    "Tüm servis ücretleri ve vergiler",
]
EXC = [
    "Mısır kapıda vizesi (30 USD)",
    "Öğle & akşam yemekleri (belirtilenler hariç)",
    "Yerel rehber bahşişi (30 €)",
    "Seyahat sigortası (tavsiye edilir)",
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
    note_cy = inc_cy + remaining_h * 0.6
    T(cv,"Vize işlemlerini tur öncesinde birlikte yapıyoruz; nasıl alınacağını adım adım anlatıyoruz.",
      RX2+0.4*cm, note_cy,"M-Light",8.5,MUTED, max_w=HALF-0.6*cm)

cy = min(inc_cy, exc_cy)
cy -= 0.5*cm

# ── KONAKLAMA ─────────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Konaklama", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

HALF2 = (CW - 0.3*cm) / 2
hotels = [
    ("KAHİRE — 3 GECE", "Azal Pyramids Hotel veya benzeri  ·  oda-kahvaltı"),
    ("HURGADA — 2 GECE", "Hurghada Golden Beach Resort veya benzeri  ·  her şey dahil"),
]
for i, (city, desc) in enumerate(hotels):
    hx = LM if i==0 else LM + HALF2 + 0.3*cm
    R(cv, hx, cy-0.68*cm, HALF2, 0.66*cm, fill=WHITE, stroke=BORDER, r=3)
    R(cv, hx, cy-0.68*cm, 4, 0.66*cm, fill=GOLD)
    T(cv, city, hx+0.35*cm, cy-0.40*cm,"M-Bold",8,NAVY)
    T(cv, desc, hx+0.35*cm, cy-0.58*cm,"M-Light",7.5,MUTED, max_w=HALF2-0.45*cm)
cy -= 0.75*cm
cy -= 0.5*cm

# ── ÖDEME & İPTAL ─────────────────────────────────────────────────────────────
_, sh = reklame(cv,"Ödeme & İptal", W/2, cy, 18, rgba=(26,23,48,255), align="center")
cy -= sh + 0.2*cm
L(cv, LM, cy, RM, cy, GOLD, 0.8)
cy -= 0.45*cm

BOX_H2 = 1.5*cm
R(cv, LM, cy-BOX_H2, CW, BOX_H2, fill=NAVY, r=5)
R(cv, LM, cy-BOX_H2, 5, BOX_H2, fill=GOLD)

reklame(cv,"~1.490 €", LM+0.5*cm, cy-0.12*cm, 26, rgba=(232,173,24,255), align="left")
T(cv,"toplam bütçe · uçak dahil · tüm vergiler dahil", LM+0.5*cm, cy-BOX_H2+0.28*cm,"M-Light",8,HexColor("#a09080"))
T(cv,"Tur fiyatı: 1.250 €  ·  ön ödeme: 595 €",
  RM-0.3*cm, cy-0.55*cm,"M-SemiBold",9,WHITE,"right")
T(cv,"Tek kişilik oda farkı: +400 €  ·  Uçuşlar: ~240 €",
  RM-0.3*cm, cy-BOX_H2+0.28*cm,"M-Light",8.5,HexColor("#a09080"),"right")
cy -= BOX_H2 + 0.2*cm

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
    "Pasaportunuzun en az 6 ay geçerlilik süresi olması gerekmektedir.",
    "Türk vatandaşları için kapıda vize gereklidir (30 USD). Vize sürecini tur öncesinde birlikte yürütüyoruz.",
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

CARD_H = 1.7*cm
fw = CW / 3
cards = [
    ("Küçük & Samimi Grup",       "Kalabalık tur kaosundan uzak,\narkadaş ortamında seyahat"),
    ("Uçtan Uca Organizasyon",    "Uçuştan vizesine, otelden\nrehbere her şey bizde"),
    ("Koşuşturmacasız Deneyim",   "Tüm lojistik bizde —\nsen sadece anını yaşa"),
]
for fi, (title, desc) in enumerate(cards):
    fx = LM + fi * fw
    R(cv, fx+0.12*cm, cy-CARD_H, fw-0.24*cm, CARD_H, fill=WARM, stroke=BORDER, r=5)
    R(cv, fx+0.12*cm, cy-CARD_H, fw-0.24*cm, 3, fill=GOLD)
    T(cv, title, fx+fw/2, cy-0.38*cm, "M-Bold", 8.5, NAVY, "center", max_w=fw-0.5*cm)
    for li, ln in enumerate(desc.split("\n")):
        T(cv, ln, fx+fw/2, cy-0.72*cm-li*0.36*cm, "M-Light", 8, MUTED, "center", max_w=fw-0.5*cm)
cy -= CARD_H + 0.25*cm

footer(cv)
cv.showPage()
cv.save()
print(f"✓  {OUTPUT}")

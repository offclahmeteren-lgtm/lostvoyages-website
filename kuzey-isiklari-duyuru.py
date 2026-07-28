"""
Lost Voyages — Kuzey Işıkları Duyuru Kanalı Seti
5 sayfa: Tarihler / Tanıtım / SSS x3
Instagram duyuru kanalına ekran görüntüsü olarak paylaşmak için.
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
OUT_DATED   = "/Users/ahmeterenvci/lostvoyages-website/kuzey-isiklari-duyuru.pdf"
OUT_NODATE  = "/Users/ahmeterenvci/lostvoyages-website/kuzey-isiklari-duyuru-tarihsiz.pdf"
FONTS  = "/Users/ahmeterenvci/lostvoyages-website/fonts"
IMGS   = "/Users/ahmeterenvci/lostvoyages-website/images"

for name, file in [("M-Light","Montserrat-Light"),("M-Regular","Montserrat-Regular"),
                    ("M-SemiBold","Montserrat-SemiBold"),("M-Bold","Montserrat-Bold")]:
    pdfmetrics.registerFont(TTFont(name, f"{FONTS}/{file}.ttf"))
REKLAME = f"{FONTS}/ReklameScript-Medium.otf"

CREAM  = HexColor("#FAF8F4")
NAVY   = HexColor("#1B1730")
GOLD   = HexColor("#C8940E")
GOLD_A = HexColor("#E8AD18")
WARM   = HexColor("#F2EFE8")
BORDER = HexColor("#E2DDD4")
MUTED  = HexColor("#8A8070")
WHITE  = white
AURORA = HexColor("#1D9E75")

LM = 1.5*cm; RM = W - 1.5*cm; CW = RM - LM

# ── helpers ───────────────────────────────────────────────────────────────────
def R(c, x, y, w, h, fill=None, stroke=None, r=0, sw=0.5):
    c.saveState(); c.setLineWidth(sw)
    if fill:   c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke)
    kw = dict(fill=1 if fill else 0, stroke=1 if stroke else 0)
    (c.roundRect(x,y,w,h,r,**kw) if r else c.rect(x,y,w,h,**kw))
    c.restoreState()

def wrap(c, text, font, size, max_w):
    words = str(text).split(); lines, cur = [], ""
    for w_ in words:
        t = (cur+" "+w_).strip()
        if c.stringWidth(t, font, size) <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def T(c, text, x, y, font="M-Regular", size=10, color=NAVY, align="left", max_w=None, lead=1.42):
    c.saveState(); c.setFont(font, size); c.setFillColor(color)
    lh = size * lead
    if max_w:
        lines = wrap(c, text, font, size, max_w)
        for i, ln in enumerate(lines):
            ly = y - i*lh
            if   align=="center": c.drawCentredString(x, ly, ln)
            elif align=="right":  c.drawRightString(x, ly, ln)
            else:                 c.drawString(x, ly, ln)
        c.restoreState(); return len(lines)*lh
    if   align=="center": c.drawCentredString(x, y, str(text))
    elif align=="right":  c.drawRightString(x, y, str(text))
    else:                 c.drawString(x, y, str(text))
    c.restoreState(); return lh

def L(c, x1,y1,x2,y2, color=BORDER, w=0.5):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(w)
    c.line(x1,y1,x2,y2); c.restoreState()

def img_box(c, path, x, y, w, h, q=88, y_anchor=0.5):
    try:
        im = PILImage.open(path).convert("RGB")
        pw, ph = int(w*3), int(h*3)
        s = max(pw/im.width, ph/im.height)
        nw, nh = int(im.width*s), int(im.height*s)
        im = im.resize((nw,nh), PILImage.LANCZOS)
        l=(nw-pw)//2; t=int((nh-ph)*y_anchor)
        im = im.crop((l,t,l+pw,t+ph))
        im = ImageEnhance.Sharpness(im).enhance(1.12)
        buf = io.BytesIO(); im.save(buf,"JPEG",quality=q); buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, w, h)
    except Exception as e: print(f"[img] {path}: {e}")

def reklame(c, text, cx, cy, size, rgba=(200,148,14,255), align="center"):
    px = int(size*3.5)
    try:    fnt = ImageFont.truetype(REKLAME, px)
    except: fnt = ImageFont.load_default()
    dd = ImageDraw.Draw(PILImage.new("RGBA",(1,1)))
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

def gradient(pw, ph, strength=0.82):
    im = PILImage.new("RGBA", (pw, ph), (0,0,0,0)); d = ImageDraw.Draw(im)
    for row in range(ph):
        a = int((row/ph)**1.5 * strength * 255)
        d.line([(0,row),(pw,row)], fill=(26,23,46,a))
    buf=io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
    return ImageReader(buf)

def footer(c):
    R(c, 0, 0, W, 1.05*cm, fill=NAVY)
    T(c,"lostvoyages.com   ·   WhatsApp +90 545 170 69 27   ·   TÜRSAB 9113",
      W/2, 4.4*mm,"M-Regular",7.5,HexColor("#c0b8a0"),"center")

def page_bg(c):
    R(c, 0, 0, W, H, fill=CREAM)
    R(c, 0, H-3*mm, W, 3*mm, fill=GOLD)

def sec_head(c, title, cy, size=19):
    _, sh = reklame(c, title, W/2, cy, size, rgba=(26,23,48,255), align="center")
    cy -= sh + 0.22*cm
    L(c, LM, cy, RM, cy, GOLD, 1.2)
    return cy - 0.55*cm

def build(with_dates, out):
    global cv
    cv = canvas.Canvas(out, pagesize=A4)

    # ══════════════════════════════════════════════════════════════════════════
    # SAYFA 1 — KOLAJ KAPAK (300 DPI tek parça kompozisyon)
    # ══════════════════════════════════════════════════════════════════════════
    from PIL import ImageFilter
    PW, PH = 2480, 3508
    F_REK   = lambda px: ImageFont.truetype(REKLAME, px)
    F_BOLD  = lambda px: ImageFont.truetype(f"{FONTS}/Montserrat-Bold.ttf", px)
    F_SEMI  = lambda px: ImageFont.truetype(f"{FONTS}/Montserrat-SemiBold.ttf", px)
    F_REG   = lambda px: ImageFont.truetype(f"{FONTS}/Montserrat-Regular.ttf", px)
    GOLD_RGB, GOLDA_RGB = (200,148,14), (232,173,24)
    CREAM_RGB, NAVYP = (232,216,152), (34,29,60)

    def cover_crop(img, w, h, y_anchor=0.5):
        s2 = max(w/img.width, h/img.height)
        img = img.resize((int(img.width*s2), int(img.height*s2)), PILImage.LANCZOS)
        l = (img.width-w)//2; t = int((img.height-h)*y_anchor)
        return img.crop((l, t, l+w, t+h))

    # ── zemin ────────────────────────────────────────────────────────────────
    page = cover_crop(PILImage.open(f"{IMGS}/gallery/enson-aurora-orman.jpg").convert("RGB"), PW, PH, 0.4)
    page = ImageEnhance.Color(page).enhance(1.18)
    page = ImageEnhance.Contrast(page).enhance(1.06)
    ov = PILImage.new("L",(PW,PH),0); od = ImageDraw.Draw(ov)
    for row in range(PH):
        f = row/PH
        od.line([(0,row),(PW,row)], fill=int((0.26 + 0.56*(f**0.85)) * 255))
    page = PILImage.composite(PILImage.new("RGB",(PW,PH),(24,20,44)), page, ov)
    D = ImageDraw.Draw(page, "RGBA")

    def ctext(draw_layer, txt, cx, cy, font, fill, tracking=0):
        """merkezli metin; tracking>0 ise harf arasi bosluk px"""
        if tracking:
            widths = [draw_layer.textbbox((0,0), ch, font=font)[2] for ch in txt]
            total = sum(widths) + tracking*(len(txt)-1)
            x = cx - total/2
            for ch, wd in zip(txt, widths):
                draw_layer.text((x, cy), ch, font=font, fill=fill, anchor="lm")
                x += wd + tracking
        else:
            draw_layer.text((cx, cy), txt, font=font, fill=fill, anchor="mm")

    def glow_text(txt, cx, cy, font, fill, glow_rgb, blur=22, alpha=160):
        lay = PILImage.new("RGBA",(PW,PH),(0,0,0,0))
        ld = ImageDraw.Draw(lay)
        ld.text((cx,cy), txt, font=font, fill=glow_rgb+(alpha,), anchor="mm")
        lay = lay.filter(ImageFilter.GaussianBlur(blur))
        page.paste(lay, (0,0), lay)
        D.text((cx,cy), txt, font=font, fill=fill, anchor="mm")

    def circle(path, ccx, ccy, r, y_anchor=0.5):
        d = r*2
        im = cover_crop(PILImage.open(path).convert("RGB"), d, d, y_anchor)
        im = ImageEnhance.Sharpness(im).enhance(1.2)
        im = ImageEnhance.Contrast(im).enhance(1.06)
        im = ImageEnhance.Color(im).enhance(1.1)
        # gölge
        sh = PILImage.new("RGBA",(PW,PH),(0,0,0,0))
        ImageDraw.Draw(sh).ellipse((ccx-r, ccy-r+14, ccx+r, ccy+r+14), fill=(0,0,0,120))
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        page.paste(sh, (0,0), sh)
        # daire + çift halka
        mask = PILImage.new("L",(d,d),0)
        ImageDraw.Draw(mask).ellipse((0,0,d-1,d-1), fill=255)
        page.paste(im, (ccx-r, ccy-r), mask)
        D.ellipse((ccx-r, ccy-r, ccx+r, ccy+r), outline=GOLDA_RGB+(255,), width=8)
        D.ellipse((ccx-r-14, ccy-r-14, ccx+r+14, ccy+r+14), outline=GOLDA_RGB+(110,), width=3)

    # ── üst bant ─────────────────────────────────────────────────────────────
    D.rectangle((0,0,PW,34), fill=GOLD_RGB)
    ctext(D, "Lost Voyages", PW//2, 128, F_REK(86), GOLDA_RGB)
    D.line((PW//2-400, 218, PW//2+400, 218), fill=GOLDA_RGB+(200,), width=3)
    glow_text("Kuzey Işıkları", PW//2, 420, F_REK(250), (255,255,255), (120,220,170), blur=34, alpha=110)
    ctext(D, "GEZİLERİ", PW//2, 640, F_BOLD(66), GOLDA_RGB, tracking=46)
    D.line((PW//2-400, 730, PW//2+400, 730), fill=GOLDA_RGB+(200,), width=3)
    ctext(D, "Moskova  ·  Murmansk  ·  St. Petersburg", PW//2, 812, F_SEMI(72), (255,255,255))
    ctext(D, "7 Gece 8 Gün   ·   Maks. 15 Kişi", PW//2, 905, F_REG(54), CREAM_RGB)

    circle(f"{IMGS}/gallery/aurora-1.jpg",  318, 345, 242)
    circle(f"{IMGS}/gallery/husky.jpg",     PW-318, 345, 242)

    # ── merkez panel ─────────────────────────────────────────────────────────
    DATES = [
        ("1","05 – 12 Kasım 2026",       None),
        ("2","05 – 12 Aralık 2026",      None),
        ("3","13 – 20 Aralık 2026",      "NOEL"),
        ("4","26 Aralık – 02 Ocak",      "YILBAŞI ÖZEL"),
        ("5","03 – 10 Ocak 2027",        None),
        ("6","16 – 23 Ocak 2027",        None),
        ("7","24 – 31 Ocak 2027",        "YARIYIL TATİLİ"),
        ("8","13 – 20 Şubat 2027",       None),
        ("9","21 – 28 Şubat 2027",       None),
        ("10","06 – 13 Mart 2027",       "RAMAZAN BAYRAMI"),
        ("11","20 – 27 Mart 2027",       None),
        ("12","28 Mart – 04 Nisan 2027", None),
    ]
    px1, px2, ptop = 596, PW-596, 1020
    rh = 76
    pbot = ptop + 190 + len(DATES)*rh + 52
    # panel gölgesi
    psh = PILImage.new("RGBA",(PW,PH),(0,0,0,0))
    ImageDraw.Draw(psh).rounded_rectangle((px1,ptop+16,px2,pbot+16), 40, fill=(0,0,0,130))
    psh = psh.filter(ImageFilter.GaussianBlur(30))
    page.paste(psh,(0,0),psh)
    D.rounded_rectangle((px1,ptop,px2,pbot), 40, fill=NAVYP+(238,), outline=GOLDA_RGB+(255,), width=5)
    D.rounded_rectangle((px1-16,ptop-16,px2+16,pbot+16), 52, outline=(138,106,16,180), width=3)
    ctext(D, "Gezi Tarihleri", (px1+px2)//2, ptop+100, F_REK(96), GOLDA_RGB)
    D.line(((px1+px2)//2-330, ptop+168, (px1+px2)//2+330, ptop+168), fill=GOLDA_RGB+(130,), width=2)
    yy = ptop + 190
    for n, dt, tg in DATES:
        D.text((px1+96, yy+rh//2), f"{n}.", font=F_BOLD(52), fill=GOLDA_RGB, anchor="rm")
        D.text((px1+128, yy+rh//2), dt, font=F_SEMI(54), fill=(255,255,255), anchor="lm")
        if tg:
            fnt = F_BOLD(34)
            tw = D.textbbox((0,0), tg, font=fnt)[2]
            pr, pl = px2-52, px2-52-tw-56
            D.rounded_rectangle((pl, yy+8, pr, yy+rh-10), 14, fill=(58,49,96,255), outline=GOLDA_RGB+(220,), width=2)
            D.text(((pl+pr)//2, yy+rh//2-1), tg, font=fnt, fill=GOLDA_RGB, anchor="mm")
        yy += rh

    # ── yan daireler ─────────────────────────────────────────────────────────
    circle(f"{IMGS}/gallery/enson-kizilmeydan-grup.jpg", 300, 1290, 232)
    circle(f"{IMGS}/gallery/ki-new-1.jpg",               286, 1800, 218)
    circle(f"{IMGS}/gallery/ki-new-4.jpg",               PW-300, 1290, 232)
    circle(f"{IMGS}/gallery/ki-aurora-gol.jpg",          PW-286, 1800, 218)

    # ── alt bölge ────────────────────────────────────────────────────────────
    circle(f"{IMGS}/gallery/ki-aurora-grup.jpg",   PW//2, 2745, 352)
    circle(f"{IMGS}/gallery/enson-geyik-grup.jpg", 432, 2640, 256)
    circle(f"{IMGS}/gallery/ki-sami-selfie.jpg",   PW-432, 2640, 256)
    circle(f"{IMGS}/gallery/ki-kar-cift.jpg",      330, 3175, 208)
    circle(f"{IMGS}/gallery/buz-yuzme.jpg",        PW-330, 3175, 208)

    D.line((PW//2-540, 3352, PW//2+540, 3352), fill=(138,106,16,220), width=2)
    ctext(D, "lostvoyages.com   ·   @ahmeterenvci   ·   TÜRSAB 9113", PW//2, 3415, F_REG(44), (216,203,168))

    buf = io.BytesIO(); page.save(buf, "JPEG", quality=92); buf.seek(0)
    cv.drawImage(ImageReader(buf), 0, 0, W, H)
    cv.showPage()



    footer(cv); cv.showPage()

    # ══════════════════════════════════════════════════════════════════════════════
    # SAYFA 2 — TANITIM
    # ══════════════════════════════════════════════════════════════════════════════
    page_bg(cv)
    cy = H - 1.25*cm
    cy = sec_head(cv, "Neden Lost Voyages?", cy, 21)

    # üst foto şeridi
    STRIP = 4.3*cm
    strip_imgs = [f"{IMGS}/gallery/ki-aurora-grup.jpg", f"{IMGS}/gallery/husky.jpg",
                  f"{IMGS}/gallery/ki-sami-grup.jpg", f"{IMGS}/gallery/enson-kizilmeydan-grup.jpg"]
    gw = CW / len(strip_imgs)
    for i, gp in enumerate(strip_imgs):
        img_box(cv, gp, LM + i*gw, cy-STRIP, gw-2, STRIP, q=86)
    cy -= STRIP + 0.55*cm

    # hikaye
    T(cv,"Merhaba, ben Eren.", LM, cy,"M-Bold",13,NAVY); cy -= 0.75*cm
    for para in [
      "5 yıldır grup gezileri düzenliyorum; bugüne kadar birçok ülkede yüzlerce misafiri ağırladım. Kuzey ışıklarının ise bende ayrı bir yeri var.",
      "Gökyüzü dans etmeye başladığında, yıllardır hayalini kuran insanların o hayali gözlerinin önünde gerçek oluyor. Mutluluktan ağlayanlar oluyor. Ve dönüp bana “hayalimi gerçekleştirdiğin için teşekkür ederim” dediklerinde hissettiğim şeyi anlatmak zor.",
      "Bu yüzden burası benim için sıradan bir tur değil. Birlikte kutuplara, hayalleri gerçekleştirmeye çıkıyoruz.",
    ]:
        cy -= T(cv, para, LM, cy,"M-Light",11,HexColor("#4A4438"), max_w=CW, lead=1.6) + 0.42*cm

    cy -= 0.15*cm

    # ── vurgu kutusu: başarı oranı
    BH = 4.05*cm
    R(cv, LM, cy-BH, CW, BH, fill=HexColor("#EAF6F1"), stroke=AURORA, r=6, sw=1)
    R(cv, LM, cy-BH, 5, BH, fill=AURORA)
    iy = cy - 0.62*cm
    T(cv,"5 YILDA SADECE BİR KEZ YAKALAYAMADIK", LM+0.5*cm, iy,"M-Bold",12.5,HexColor("#0F6E56"))
    iy -= 0.62*cm
    iy -= T(cv,"Kuzey ışığı bir doğa olayı — kimse garanti veremez. Ama bu tesadüf değil: bölgede 15 yıldır çalışan profesyonel ışık avcılarıyla birlikteyiz. Her gece solar aktivite ve bulut haritası okunuyor, o gecenin en doğru noktası seçiliyor, gerekirse saatlerce yol gidiyoruz.",
          LM+0.5*cm, iy,"M-Light",10.5,HexColor("#3A5F52"), max_w=CW-1*cm, lead=1.55) + 0.18*cm
    T(cv,"Aynı otelde kaldığımız gruplar bizimle aynı gece ava çıkıp göremeden dönerken biz yakalıyoruz.",
      LM+0.5*cm, iy,"M-SemiBold",10.5,HexColor("#0F6E56"), max_w=CW-1*cm, lead=1.55)
    cy -= BH + 0.5*cm

    # ── iki sütun: otel + grup
    COLW = (CW - 0.45*cm) / 2
    cols = [
        ("ŞEHİR MERKEZİNDE 4 YILDIZLI OTEL",
         "Kuzeyde iki yol var: şehir dışında dağ evleri ya da şehirde otel. Biz oteli seçiyoruz. Dağ evi fotoğrafta romantik görünür ama koşulları biraz zor. Gün boyu süren aktivitelerin ve gece yarısına kadar süren ışık avının yorgunluğunun üstüne 4 yıldızlı otel konforu bambaşka."),
        ("MAKSİMUM 15 KİŞİ",
         "Bu bir otobüs turu değil. 15 kişi, birbirini gerçekten tanıyabilen bir grup demek. Katılımcılarımızın çoğu tek başına geliyor — ve neredeyse hiçbiri tek başına dönmüyor. Bu gezilerden çıkıp birlikte başka ülkelere gitmeye devam eden onlarca arkadaş grubu var."),
    ]
    CH = 0
    for t, d in cols:
        need = 0.55*cm + len(wrap(cv,t,"M-Bold",10.5,COLW-0.7*cm))*10.5*1.42 \
             + 0.16*cm + len(wrap(cv,d,"M-Light",9.8,COLW-0.7*cm))*9.8*1.55 + 0.42*cm
        CH = max(CH, need)
    for i,(t, d) in enumerate(cols):
        cx = LM + i*(COLW + 0.45*cm)
        R(cv, cx, cy-CH, COLW, CH, fill=WHITE, stroke=BORDER, r=5)
        R(cv, cx, cy-CH, COLW, 3, fill=GOLD)
        ty = cy - 0.55*cm
        ty -= T(cv, t, cx+0.35*cm, ty,"M-Bold",10.5,NAVY, max_w=COLW-0.7*cm) + 0.2*cm
        T(cv, d, cx+0.35*cm, ty,"M-Light",9.8,MUTED, max_w=COLW-0.7*cm, lead=1.55)
    cy -= CH + 0.5*cm

    # ── dahil olan deneyimler
    T(cv,"S A D E C E   I Ş I K   D E Ğ İ L", W/2, cy,"M-Bold",10.5,GOLD,"center"); cy -= 0.72*cm
    exps = ["Husky Kızağı","Ren Geyiği & Sami Köyü","Kar Motoru Safarisi",
            "Lenin Buzkıranı","Hermitage & Kızıl Meydan","Işık Avı Fotoğraf Çekimi"]
    ew = CW/3; eh = 0.92*cm
    for i, e in enumerate(exps):
        ex = LM + (i%3)*ew; ey = cy - (i//3)*(eh+0.16*cm)
        R(cv, ex+0.06*cm, ey-eh, ew-0.12*cm, eh, fill=WARM, stroke=BORDER, r=4)
        T(cv, e, ex+ew/2, ey-0.56*cm,"M-SemiBold",9.6,NAVY,"center", max_w=ew-0.35*cm)
    cy -= 2*(eh+0.16*cm) + 0.35*cm

    R(cv, LM, cy-1.05*cm, CW, 1.0*cm, fill=NAVY, r=5)
    T(cv,"🏅  TÜRSAB 9113 belgeli acente güvencesiyle  ·  lostvoyages.com",
      W/2, cy-0.63*cm,"M-SemiBold",11,GOLD_A,"center")

    footer(cv); cv.showPage()

    # ══════════════════════════════════════════════════════════════════════════════
    # SSS SAYFALARI
    # ══════════════════════════════════════════════════════════════════════════════
    FAQ = [
       ("KUZEY IŞIKLARI", [
         ("Kuzey ışıklarını kesin görecek miyiz?",
          "Dünyada kimse buna garanti veremez — bu bir doğa olayı. Ama rakamlar bizden yana: 5 senedir düzenlediğimiz gezilerde sadece bir kez ışıkları yakalayamadık. Bölgede 15 yıldır çalışan profesyonel ışık avcılarıyla birlikteyiz; her gece solar aktivite, bulut yoğunluğu ve şehir ışıklarından uzaklık hesaplanarak o gecenin en doğru noktası seçiliyor. Murmansk'ta 3 gece kalıyoruz ve kutup gecesi sayesinde günde 21 saate varan karanlık var."),
         ("Işıklar en çok hangi aylarda görünür?",
          "Kasım–Nisan arası tüm tarihlerde ihtimal benzer. Belirleyici olan ay değil, o gecenin solar aktivitesi ve gökyüzünün açıklığı. Bu yüzden asıl önemli olan karanlıkta geçirilen saat sayısı ve doğru lokasyon seçimi."),
         ("Işıkları telefonla çekebilir miyim?",
          "Evet, yeni nesil telefonların gece modu iyi sonuç veriyor. Ama asıl güzel haber: ışık avı fotoğraf çekimi fiyata dahil. Ekstra ücret ödemeden profesyonel karelerinle dönüyorsun."),
         ("Profesyonel kamera getirmeli miyim?",
          "Varsa mutlaka getir, tripod da al. Yoksa dert etme — hem telefonun yeterli hem de çekim zaten dahil."),
       ]),
       ("KONAKLAMA & KONFOR", [
         ("Nerede kalıyoruz?",
          "Üç şehirde de 4 yıldızlı, şehir merkezinde otellerde: Moskova 2 gece, Murmansk 3 gece, St. Petersburg 2 gece. Murmansk'ta da şehir dışında dağ evinde değil merkezde oteldeyiz — gece ışık avından döndüğünde kendi odan, sıcak suyun ve internetin seni bekliyor."),
         ("Odalarda internet var mı?",
          "Evet, üç şehirde de otellerimizde Wi-Fi mevcut."),
         ("Tek başıma katılırsam oda nasıl oluyor?",
          "Aynı cinsiyetten bir misafirle eşleştiriyoruz ve bunu yaparken karakter uyumuna dikkat ediyoruz. Tek kalmak istersen fiyat farkıyla tek kişilik oda alabilirsin; detayı bize sorabilirsin."),
         ("Arkadaşımla aynı odada kalabilir miyim?",
          "Tabii ki, iki kişi katılırsanız aynı odayı paylaşabilirsiniz."),
       ]),
       ("GRUP & KATILIM", [
         ("Gruplar kaç kişilik?",
          "Maksimum 15 kişi. Bu sayıyı hiçbir koşulda aşmıyoruz — 15'ten sonrası artık grup değil kalabalık oluyor."),
         ("Tek başıma katılabilir miyim?",
          "Katılımcılarımızın çoğunluğu tek başına geliyor. İlk akşam herkes tanışıyor, gezinin sonunda kimse yabancı kalmıyor. Çekinecek hiçbir şey yok."),
         ("Katılımcı profili nasıl?",
          "Genellikle 24–40 yaş arası, keşfetmeyi seven, yeni insanlara açık, uyumlu bir kitle. Bay-bayan dengesine de özen gösteriyoruz."),
         ("Yaş sınırı var mı?",
          "Gezi +18. Program yoğun tempolu ve soğuk hava koşullarında geçtiği için çocuklar için uygun değil."),
       ]),
       ("GÜVENLİK & GÜVENCE", [
         ("Lost Voyages resmi bir acente mi?",
          "Evet. Turlarımız 9113 belge numarasıyla TÜRSAB'a kayıtlı ALHARAMAIN UNITED GROUP TURİZM güvencesi altında düzenleniyor."),
         ("Savaş nedeniyle riskli mi?",
          "Gezi düzenlediğimiz bölgeler — Moskova, Murmansk ve St. Petersburg — çatışma bölgelerinden çok uzakta. Bu şehirlerde günlük hayat, turizm ve ulaşım olağan şekilde devam ediyor. Programı her zaman güncel koşullara göre planlıyoruz ve riskli gördüğümüz hiçbir rotayı dahil etmiyoruz."),
         ("Seyahat sigortası gerekli mi?",
          "Kesinlikle öneriyoruz. Sigorta katılımcıya ait, ancak isteyen misafirlerimize süreçte yardımcı oluyoruz."),
       ]),
       ("ÖDEME & KAYIT", [
         ("Fiyata ne dahil, ne değil?",
          "Dahil: 7 gece 4 yıldızlı otel konaklama, tüm transferler, husky kızağı, ren geyiği kızağı, kar motoru safarisi, Sami köyü, 2× aurora avı turu, ışık avı fotoğraf çekimi, 7 sabah kahvaltısı. Dahil değil: uçak biletleri, e-vize, yemekler ve müze girişleri, buz yüzme aktivitesi (opsiyonel)."),
         ("Nasıl kayıt oluyorum?",
          "Yerini kesinleştirmek için 395 € ön ödeme yeterli. Kalan tutarı geziden bir ay öncesine kadar tamamlayabilirsin."),
         ("İptal edersem ne oluyor?",
          "Geziye 60 günden fazla varsa 80 € kesinti, kalan tutar iade edilir. 60–30 gün kala 100 € kesinti uygulanır. 30 günden az kala kapora iade edilmez."),
         ("Uçak biletini kim alıyor?",
          "Biletler sana ait ama birlikte alıyoruz. 2 yurt dışı, 2 Rusya içi olmak üzere toplam 4 uçuş var. Yerin kesinleştiğinde uygun uçuşları link ile paylaşıyoruz, kendi kartınla alıyorsun."),
       ]),
       ("VİZE & BELGELER", [
         ("Rusya vizesi gerekiyor mu?",
          "Evet, ama endişelenme — e-vize ile oldukça kolay. Başvuru online yapılıyor, vizen birkaç gün içinde PDF olarak mailine geliyor."),
         ("Vize işlemlerinde yardımcı oluyor musunuz?",
          "Kesinlikle. İki seçeneğin var: adım adım hazırladığımız bilgilendirme broşürüyle başvuruyu kendin yaparsın, ya da dilersen tüm süreci senin adına biz tamamlarız."),
         ("Pasaportum ne kadar geçerli olmalı?",
          "Giriş tarihinden itibaren en az 6 ay geçerli olmalı ve en az 2 boş vize sayfası bulunmalı."),
         ("Pasaportum yok, yetişir mi?",
          "Randevu durumuna göre genelde birkaç hafta içinde çıkıyor. Turdan en az 2 ay önce başvurmanı öneririz."),
       ]),
       ("HAZIRLIK & PRATİK BİLGİLER", [
         ("Hava ne kadar soğuk?",
          "Kasım–Nisan arasında −25 ile +5 derece arasında değişebiliyor. Ama şunu bil: kötü hava yoktur, kötü kıyafet vardır. Grupta yerini ayırdıktan sonra ne alman gerektiğini detaylı listeyle paylaşıyoruz."),
         ("Kıyafetleri Türkiye'den mi almalıyım?",
          "Evet, alışverişini Türkiye'de yapmanı öneriyoruz. Listeyi önceden gönderiyor, hazırlık sürecinde birebir yardımcı oluyoruz."),
         ("Rusya'da kartlar çalışıyor mu?",
          "Hayır — yaptırımlar nedeniyle yabancı banka kartları geçmiyor. Yanında nakit euro getirmen gerekiyor, orada rubleye çeviriyoruz. Kişisel harcamalar için 300–450 € bulundurman yeterli olacaktır."),
         ("İnternet ve SIM kart nasıl olacak?",
          "Hattını yurt dışı kullanıma açtırma veya eSIM alma konusunda destek veriyoruz. eSIM kullanırsan VPN'e ihtiyacın olmuyor — bu en pratik çözüm. Ayrıca otellerimizde Wi-Fi mevcut."),
         ("Prizler farklı mı?",
          "Hayır, Rusya'daki prizler Türkiye ile aynı. Dönüştürücüye gerek yok."),
         ("Program fiziksel olarak zorlayıcı mı?",
          "Herkesin katılabileceği şekilde planlanıyor. Yoğun ve dolu dolu bir program — bazı günler erken kalkıyoruz. Kronik bir rahatsızlığın varsa lütfen gezi öncesi bize bildir."),
         ("Buz yüzme için yüzme bilmek gerekiyor mu?",
          "Hayır. Giydiğimiz özel kuru elbise seni suyun üstünde ve sıcak tutuyor. Denizcilerin acil durumlarda kullandığı ekipmanın aynısı — tamamen güvenli ve kontrollü."),
       ]),
    ]

    BOTTOM  = 1.05*cm + 0.6*cm       # footer + nefes payı
    QH, AH  = 12.5, 11               # telefonda rahat okunacak punto
    GRP_H   = 0.82*cm + 0.34*cm
    GAP     = 0.28*cm

    def qbox_h(q, a):
        return (0.42*cm + len(wrap(cv,q,"M-SemiBold",QH,CW-1.5*cm))*QH*1.45
                + 0.1*cm + len(wrap(cv,a,"M-Light",AH,CW-1.5*cm))*AH*1.55 + 0.42*cm)

    def new_faq_page():
        page_bg(cv)
        return sec_head(cv, "Sık Sorulan Sorular", H - 1.25*cm, 21)

    def draw_grp(cy, title):
        R(cv, LM, cy-0.82*cm, CW, 0.8*cm, fill=NAVY, r=4)
        T(cv, title, LM+0.4*cm, cy-0.54*cm,"M-Bold",11,GOLD_A)
        return cy - GRP_H

    # ── akışı düzleştir ───────────────────────────────────────────────────────────
    items, n = [], 0
    for gtitle, qs in FAQ:
        first = qbox_h(*qs[0]) + GAP
        items.append(("g", gtitle, GRP_H, GRP_H + first))   # yetim başlık koruması
        for q, a in qs:
            n += 1
            hh = qbox_h(q, a) + GAP
            items.append(("q", (n, q, a, gtitle), hh, hh))

    # ── kaç sayfa gerekiyor + sayfalar nasıl dengelenir ──────────────────────────
    _probe = canvas.Canvas("/dev/null", pagesize=A4)
    _top = H - 1.25*cm
    _, _sh = reklame(_probe, "Sık Sorulan Sorular", W/2, _top, 21)
    AVAIL = (_top - _sh - 0.22*cm - 0.55*cm) - BOTTOM

    def simulate(target=None):
        """Verilen hedef yükseklikle kaç sayfa çıkar? ('devam' başlıkları dahil)"""
        pages, room, used, grp = 1, AVAIL, 0, None
        for kind, data, h, mb in items:
            if used > 0 and (room - mb < 0 or (target and used + h > target)):
                pages += 1; room, used = AVAIL, 0
                if kind == "q" and grp:
                    room -= GRP_H; used += GRP_H
            if kind == "g": grp = data
            room -= h; used += h
        return pages

    TOTAL = sum(h for _,_,h,_ in items)
    NPAGE = simulate()                       # önce açgözlü doldur → gerçek sayfa sayısı
    TARGET = None
    for k in range(0, 40):                   # sayfa sayısını artırmadan en dengeli hedefi bul
        cand = (TOTAL / NPAGE) * (1 + k*0.02)
        if simulate(cand) <= NPAGE:
            TARGET = cand; break

    # ── çiz ───────────────────────────────────────────────────────────────────────
    cy = new_faq_page()
    room, used, cur_grp = AVAIL, 0, None
    qno = 0

    for kind, data, h, mb in items:
        if used > 0 and (room - mb < 0 or (TARGET and used + h > TARGET)):
            footer(cv); cv.showPage()
            cy = new_faq_page(); room, used = AVAIL, 0
            if kind == "q" and cur_grp:
                cy = draw_grp(cy, cur_grp + "  (devam)"); room -= GRP_H; used += GRP_H

        if kind == "g":
            cur_grp = data
            cy = draw_grp(cy, data); room -= h; used += h
            continue

        qno, q, a, _ = data
        bh = h - GAP
        R(cv, LM, cy-bh, CW, bh, fill=WHITE, stroke=BORDER, r=5)
        R(cv, LM, cy-bh, 3.5, bh, fill=GOLD_A)
        R(cv, LM+0.34*cm, cy-0.72*cm, 0.64*cm, 0.46*cm, fill=HexColor("#FBF0D6"), r=3)
        T(cv, str(qno), LM+0.66*cm, cy-0.57*cm,"M-Bold",9.5,HexColor("#7A5A08"),"center")
        ty = cy - 0.55*cm
        ty -= T(cv, q, LM+1.2*cm, ty,"M-SemiBold",QH,NAVY, max_w=CW-1.5*cm, lead=1.45) + 0.1*cm
        T(cv, a, LM+1.2*cm, ty,"M-Light",AH,MUTED, max_w=CW-1.5*cm, lead=1.55)
        cy -= h; room -= h; used += h

    footer(cv); cv.showPage()
    cv.save()
    print(f"✓  {out}  ({qno} soru, {cv.getPageNumber()-1} sayfa)")


build(True,  OUT_DATED)

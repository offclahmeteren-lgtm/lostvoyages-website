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
    # SAYFA 1 — KOLAJ KAPAK (fiyatsız, yüksek çözünürlük)
    # ══════════════════════════════════════════════════════════════════════════
    SS = 6  # supersample çarpanı — netlik için
    def img_circle(c, path, ccx, ccy, r, y_anchor=0.5):
        try:
            im = PILImage.open(path).convert("RGB")
            d = int(r*2*SS)
            s2 = max(d/im.width, d/im.height)
            nw, nh = int(im.width*s2), int(im.height*s2)
            im = im.resize((nw,nh), PILImage.LANCZOS)
            l=(nw-d)//2; t=int((nh-d)*y_anchor)
            im = im.crop((l,t,l+d,t+d))
            im = ImageEnhance.Sharpness(im).enhance(1.18)
            im = ImageEnhance.Contrast(im).enhance(1.05)
            mask = PILImage.new("L",(d,d),0)
            ImageDraw.Draw(mask).ellipse((0,0,d-1,d-1), fill=255)
            out_im = PILImage.new("RGBA",(d,d),(0,0,0,0))
            out_im.paste(im,(0,0),mask)
            ring = ImageDraw.Draw(out_im)
            rw = max(3, int(d*0.013))
            ring.ellipse((rw//2, rw//2, d-1-rw//2, d-1-rw//2), outline=(232,173,24,255), width=rw)
            buf=io.BytesIO(); out_im.save(buf,"PNG"); buf.seek(0)
            c.drawImage(ImageReader(buf), ccx-r, ccy-r, r*2, r*2, mask="auto")
        except Exception as e: print(f"[circ] {path}: {e}")

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

    # ── tam sayfa aurora zemin + koyu degrade ────────────────────────────────
    try:
        bg = PILImage.open(f"{IMGS}/gallery/enson-aurora-orman.jpg").convert("RGB")
        pw, ph = 1240, 1754
        s2 = max(pw/bg.width, ph/bg.height)
        bg = bg.resize((int(bg.width*s2), int(bg.height*s2)), PILImage.LANCZOS)
        l=(bg.width-pw)//2; bg = bg.crop((l, 0, l+pw, ph))
        ov = PILImage.new("L",(pw,ph),0); od = ImageDraw.Draw(ov)
        for row in range(ph):
            f = row/ph
            a = int((0.30 + 0.55*(f**0.8)) * 255)   # üst hafif, alt koyu
            od.line([(0,row),(pw,row)], fill=a)
        navy_l = PILImage.new("RGB",(pw,ph),(27,23,48))
        bg = PILImage.composite(navy_l, bg, ov)
        buf=io.BytesIO(); bg.save(buf,"JPEG",quality=90); buf.seek(0)
        cv.drawImage(ImageReader(buf), 0, 0, W, H)
    except Exception as e:
        R(cv, 0, 0, W, H, fill=NAVY); print(f"[bg] {e}")
    R(cv, 0, H-3*mm, W, 3*mm, fill=GOLD)

    G = f"{IMGS}/gallery"

    # ── başlık bloğu ─────────────────────────────────────────────────────────
    reklame(cv, "Lost Voyages", W/2, H-0.95*cm, 13, rgba=(232,173,24,255))
    L(cv, W/2-3.4*cm, H-1.75*cm, W/2+3.4*cm, H-1.75*cm, GOLD_A, 0.8)
    reklame(cv, "Kuzey Işıkları", W/2, H-2.35*cm, 40, rgba=(255,255,255,255))
    T(cv,"G   E   Z   İ   L   E   R   İ", W/2, H-5.3*cm,"M-Bold",14,GOLD_A,"center")
    L(cv, W/2-3.4*cm, H-5.75*cm, W/2+3.4*cm, H-5.75*cm, GOLD_A, 0.8)
    T(cv,"Moskova  ·  Murmansk  ·  St. Petersburg", W/2, H-6.55*cm,"M-SemiBold",12.5,WHITE,"center")
    T(cv,"7 Gece 8 Gün   ·   Maks. 15 Kişi", W/2, H-7.35*cm,"M-Regular",10.5,HexColor("#E8D898"),"center")

    # üst köşe daireleri
    img_circle(cv, f"{G}/aurora-1.jpg",  2.65*cm,  H-2.9*cm, 2.05*cm)
    img_circle(cv, f"{G}/husky.jpg",     W-2.65*cm, H-2.9*cm, 2.05*cm)

    # ── merkez tarih paneli ───────────────────────────────────────────────────
    bx1, bx2 = 5.0*cm, W-5.0*cm
    bw = bx2 - bx1
    rh = 0.63*cm
    bh_total = 1.5*cm + len(DATES)*rh + 0.45*cm
    btop = H - 8.1*cm
    # çift altın çerçeve
    R(cv, bx1-0.1*cm, btop-bh_total-0.1*cm, bw+0.2*cm, bh_total+0.2*cm, stroke=HexColor("#8A6A10"), r=12, sw=0.8)
    R(cv, bx1, btop-bh_total, bw, bh_total, fill=HexColor("#221D3C"), stroke=GOLD_A, r=10, sw=1.4)
    reklame(cv, "Gezi Tarihleri", W/2, btop-0.28*cm, 16, rgba=(232,173,24,255))
    yy = btop - 1.5*cm
    for n, d, tg in DATES:
        T(cv, f"{n}.", bx1+0.6*cm, yy-0.32*cm,"M-Bold",10,GOLD_A)
        T(cv, d, bx1+1.3*cm, yy-0.32*cm,"M-SemiBold",10.5,WHITE)
        if tg:
            tw2 = cv.stringWidth(tg,"M-Bold",7) + 0.44*cm
            R(cv, bx2-tw2-0.45*cm, yy-0.44*cm, tw2, 0.38*cm, fill=HexColor("#3A3160"), stroke=GOLD_A, r=3, sw=0.6)
            T(cv, tg, bx2-tw2/2-0.45*cm, yy-0.315*cm,"M-Bold",7,GOLD_A,"center")
        yy -= rh

    # yan daireler (panelin iki yanı)
    img_circle(cv, f"{G}/enson-kizilmeydan-grup.jpg", 2.5*cm,  H-10.7*cm, 1.95*cm)
    img_circle(cv, f"{G}/ki-new-1.jpg",               2.4*cm,  H-15.1*cm, 1.85*cm)
    img_circle(cv, f"{G}/ki-new-4.jpg",               W-2.5*cm, H-10.7*cm, 1.95*cm)
    img_circle(cv, f"{G}/ki-aurora-gol.jpg",          W-2.4*cm, H-15.1*cm, 1.85*cm)

    # ── alt bölge: aynı hizada üçlü + köşe daireleri ─────────────────────────
    img_circle(cv, f"{G}/ki-aurora-grup.jpg",   W/2,      6.45*cm, 2.95*cm)
    img_circle(cv, f"{G}/enson-geyik-grup.jpg", 3.55*cm,  7.3*cm, 2.15*cm)
    img_circle(cv, f"{G}/ki-sami-selfie.jpg",   W-3.55*cm, 7.3*cm, 2.15*cm)
    img_circle(cv, f"{G}/ki-kar-cift.jpg",      2.75*cm,   2.55*cm, 1.75*cm)
    img_circle(cv, f"{G}/buz-yuzme.jpg",        W-2.75*cm, 2.55*cm, 1.75*cm)

    L(cv, W/2-4.6*cm, 1.15*cm, W/2+4.6*cm, 1.15*cm, HexColor("#8A6A10"), 0.6)
    T(cv,"lostvoyages.com   ·   @ahmeterenvci   ·   TÜRSAB 9113",
      W/2, 0.55*cm,"M-Regular",8.5,HexColor("#d8cba8"),"center")
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

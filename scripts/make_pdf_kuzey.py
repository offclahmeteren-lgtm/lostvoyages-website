"""
Lost Voyages — Kuzey Isiklari PDF  (sade, guvenilir layout)
17 sayfa · Arial Unicode TTF · canvas.drawString only
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import io, os, math, random

W, H = A4

# ── Fontlar ---------------------------------------------------------------
SYS = '/System/Library/Fonts/Supplemental/'
LIB = '/Library/Fonts/'
pdfmetrics.registerFont(TTFont('AU',  LIB + 'Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('AB',  SYS + 'Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('AI',  SYS + 'Arial Italic.ttf'))

# ── Renkler ---------------------------------------------------------------
BG    = HexColor('#080816')
BG2   = HexColor('#0D1226')
BG3   = HexColor('#0F1A2E')
AUR   = HexColor('#00C8A0')
GOLD  = HexColor('#D4A017')
WHITE = HexColor('#ECEAE5')
DIM   = HexColor('#8A8880')
RED   = HexColor('#C03030')
BLUE  = HexColor('#3A78C8')
PURP  = HexColor('#8B5CF6')

IMG = '/Users/ahmeterenvci/lostvoyages-website/images/gallery/'
OUT = os.path.expanduser('~/Desktop/lostvoyages-kuzey-isiklari.pdf')

_cache = {}
def img(path, mw=1100, q=70):
    if path in _cache: return _cache[path]
    try:
        p = PILImage.open(path).convert('RGB')
        w, h = p.size
        if w > mw: p = p.resize((mw, int(h*mw/w)), PILImage.LANCZOS)
        buf = io.BytesIO()
        p.save(buf, 'JPEG', quality=q, optimize=True)
        buf.seek(0)
        r = ImageReader(buf)
        _cache[path] = r
        return r
    except: return None

# ── Temel yardimcilar -----------------------------------------------------
def bg(c, col=None):
    c.setFillColor(col or BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def overlay(c, x=0, y=0, w=None, h=None, a=0.5):
    c.setFillColor(Color(0,0,0,alpha=a))
    c.rect(x, y, w or W, h or H, fill=1, stroke=0)

def photo_full(c, path, a=0.52):
    r = img(path)
    if r: c.drawImage(r, 0, 0, W, H, preserveAspectRatio=False)
    else: bg(c)
    overlay(c, a=a)

def photo_band(c, path, y, h2, a=0.45):
    r = img(path)
    if not r: return
    c.drawImage(r, 0, y, W, h2, preserveAspectRatio=False)
    overlay(c, y=y, h=h2, a=a)

def stars(c, n=55, seed=1):
    random.seed(seed)
    for _ in range(n):
        x = random.uniform(8, W-8)
        y = random.uniform(H*0.32, H-8)
        r = random.uniform(0.4, 1.0)
        a = random.uniform(0.3, 0.9)
        c.setFillColor(Color(1,1,1,alpha=a))
        c.circle(x, y, r, fill=1, stroke=0)

def aurora_glow(c, y0=H*0.5):
    for dy, bh, alpha in [(0,22,0.11),(30,15,0.08),(-32,12,0.07),(55,9,0.05)]:
        bw = W * 0.78
        bx = (W-bw)/2
        for i in range(28):
            t = i/28
            a = alpha * math.sin(t*math.pi)
            c.setFillColor(Color(0,0.78,0.63,alpha=a))
            c.rect(bx + t*bw, y0+dy-bh/2, bw/28+1, bh, fill=1, stroke=0)

def hline(c, x1, y, x2=None, col=None, lw=0.5):
    c.setStrokeColor(col or Color(1,1,1,alpha=0.14))
    c.setLineWidth(lw)
    c.line(x1, y, x2 or W-x1, y)

def dot(c, x, y, r=3.5, col=AUR):
    c.setFillColor(col)
    c.circle(x, y, r, fill=1, stroke=0)

def bar(c, x, y, h2=40, w2=4, col=AUR):
    c.setFillColor(col)
    c.rect(x, y, w2, h2, fill=1, stroke=0)

def t(c, s, x, y, fn='AU', fs=10, col=WHITE, align='l'):
    c.setFont(fn, fs)
    c.setFillColor(col)
    if align=='c': c.drawCentredString(x, y, s)
    elif align=='r': c.drawRightString(x, y, s)
    else: c.drawString(x, y, s)

def pill(c, x, y, label, bg2=AUR, fg=BG, fs=8):
    c.setFont('AB', fs)
    tw = c.stringWidth(label, 'AB', fs)
    ph, pv = 8, 3
    rw = tw + ph*2
    rh = fs + pv*2 + 2
    c.setFillColor(bg2)
    c.roundRect(x, y, rw, rh, 3, fill=1, stroke=0)
    c.setFillColor(fg)
    c.drawString(x+ph, y+pv+1.5, label)
    return rw

def lv_logo(c):
    t(c, 'LOST VOYAGES', W/2, 18, 'AB', 7, Color(1,1,1,alpha=0.35), 'c')

def pgnum(c, n):
    t(c, str(n), W/2, 7, 'AU', 6, Color(1,1,1,alpha=0.3), 'c')

def wrap(c, text, x, y, max_w, fn='AU', fs=10, col=WHITE, leading=15, align='l'):
    """Metni kelime kelime satirlara boler. Donen y son satirin alti."""
    c.setFont(fn, fs)
    words = text.split()
    line = ''
    cy = y
    for word in words:
        test = (line + ' ' + word).strip()
        if c.stringWidth(test, fn, fs) <= max_w:
            line = test
        else:
            if line:
                c.setFillColor(col)
                if align=='c': c.drawCentredString(x + max_w/2, cy, line)
                elif align=='r': c.drawRightString(x + max_w, cy, line)
                else: c.drawString(x, cy, line)
            line = word
            cy -= leading
    if line:
        c.setFillColor(col)
        if align=='c': c.drawCentredString(x + max_w/2, cy, line)
        elif align=='r': c.drawRightString(x + max_w, cy, line)
        else: c.drawString(x, cy, line)
        cy -= leading
    return cy

def section_tag(c, label, x, y, col=AUR, align='l'):
    t(c, label, x, y, 'AB', 8, col, align)

def day_hdr(c, day, city, title, col=AUR, y=None):
    y = y or H-80
    bar(c, 30, y-10, h2=52, w2=4, col=col)
    section_tag(c, day + '   ' + city, 44, y+32, col)
    t(c, title, 44, y, 'AB', 22, WHITE)
    hline(c, 30, y-16, W-30)

# ═══════════════════════════════════════════════════════════════════════════
# S.1  KAPAK
# ═══════════════════════════════════════════════════════════════════════════
def p1(c):
    photo_full(c, IMG+'ki-new-1.jpg', a=0.46)
    stars(c, 80, 7)
    aurora_glow(c, H*0.54)

    # Üst bant
    c.setFillColor(Color(0,0,0,alpha=0.42))
    c.rect(0, H-50, W, 50, fill=1, stroke=0)
    t(c, 'LOST VOYAGES', 28, H-32, 'AB', 11, Color(1,1,1,alpha=0.92))
    t(c, 'lostvoyages.com', W-28, H-32, 'AU', 8, Color(1,1,1,alpha=0.5), 'r')

    # Rozetler
    py = H*0.61
    rw1 = pill(c, W/2-162, py+90, 'ARA 2026 — OCA 2027')
    pill(c, W/2-162+rw1+8, py+90, '7 GECE / 8 GUN', bg2=GOLD)

    # Ana baslik
    t(c, 'KUZEY', W/2, py+44, 'AB', 56, WHITE, 'c')
    t(c, 'ISIKLARI', W/2, py-20, 'AB', 56, AUR, 'c')

    hline(c, W/2-100, py-38, W/2+100, col=Color(1,1,1,alpha=0.4))
    t(c, 'Moskova   ·   Murmansk   ·   St. Petersburg', W/2, py-55, 'AU', 12,
      Color(1,1,1,alpha=0.8), 'c')
    hline(c, W/2-100, py-68, W/2+100, col=Color(1,1,1,alpha=0.4))
    t(c, '"Bu bir tur degil, bir Kuzey Isiklari avi."', W/2, py-90,
      'AI', 13, Color(1,1,1,alpha=0.7), 'c')

    # Alt bilgi banti
    c.setFillColor(Color(0,0,0,alpha=0.62))
    c.rect(0, 0, W, 88, fill=1, stroke=0)
    items = [
        ('4 Kontenjan','Ara. 2026 - Oca. 2027'),
        ('Maks. 15 Kisi','Butik grup'),
        ('4 Yildizli Otel','3 sehir, 7 gece'),
        ('2x Aurora Avi','Rehber esliginde'),
        ('~750 EUR Ucak','Gidis - Donus'),
    ]
    cw2 = W/len(items)
    for i,(a2,b2) in enumerate(items):
        cx = cw2*i + cw2/2
        if i>0: hline(c, cw2*i, 88, cw2*i, col=Color(1,1,1,alpha=0.1))
        t(c, a2, cx, 63, 'AB', 9, WHITE, 'c')
        t(c, b2, cx, 48, 'AU', 7.5, DIM, 'c')

    hline(c, 0, 88, W, col=Color(1,1,1,alpha=0.18))
    lv_logo(c); pgnum(c,1); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.2  MESAJ
# ═══════════════════════════════════════════════════════════════════════════
def p2(c):
    bg(c)
    stars(c, 45, 12)
    photo_band(c, IMG+'ki-aurora-erkek.jpg', H*0.44, H*0.56, a=0.28)
    bar(c, 28, 175, h2=H-255, w2=3, col=AUR)

    y = H-78
    section_tag(c, 'AHMET EREN   |   LOST VOYAGES   |   7 YIL', 46, y, AUR)
    t(c, '7 yildir insanlari', 46, y-38, 'AB', 28, WHITE)
    t(c, "Aurora'nin altina", 46, y-74, 'AB', 28, AUR)
    t(c, 'gotürüyorum.', 46, y-110, 'AB', 28, WHITE)
    hline(c, 46, y-124, W-46)

    msg_lines = [
        "Kuzey Isiklari'ni ilk gordügümde ne hissettigi mi",
        'hâlâ hatirliyorum. Yukaridan dökülen o yesil perdeler',
        'gökyüzünde dans ederken insanin sesi kesilir.',
        '',
        'O andan beri tek amacim: sizi de o anin tam ortasina',
        'götürmek.',
        '',
        "Murmansk'ta 3 yildir ayni isik avcisi ekiple çalisiyoruz.",
        'Dogru ekip + dogru zamanlama = en yüksek görme orani.',
        'Iki kez ava çikiyoruz — ikisi de pik aktivite saatlerinde.',
        '',
        'Siz sadece gelin. Gerisini biz halledelim.',
    ]
    my = y-140
    for line in msg_lines:
        if line == '':
            my -= 7
        else:
            t(c, line, 46, my, 'AU', 10.5, WHITE)
            my -= 16

    # Imza
    sy = 240
    bar(c, 46, sy, h2=50, w2=3, col=GOLD)
    t(c, 'Ahmet Eren', 58, sy+33, 'AB', 13, GOLD)
    t(c, 'Kurucu  |  Lost Voyages', 58, sy+17, 'AU', 9, DIM)
    t(c, '@ahmeterenvci', 58, sy+4, 'AU', 9, DIM)

    hline(c, 46, 134, W-46)
    t(c, '3 yildir Murmansk\'ta — sektördeki en yüksek aurora görme orani', W/2, 118,
      'AU', 9, DIM, 'c')

    lv_logo(c); pgnum(c,2); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.3  NEDEN LOST VOYAGES
# ═══════════════════════════════════════════════════════════════════════════
def p3(c):
    bg(c, BG2)
    stars(c, 40, 3)
    aurora_glow(c, H*0.47)

    y = H-70
    section_tag(c, 'NEDEN LOST VOYAGES?', W/2, y, AUR, 'c')
    t(c, 'Bu bir tur degil,', W/2, y-42, 'AB', 34, WHITE, 'c')
    t(c, 'bir Kuzey Isiklari avi.', W/2, y-82, 'AB', 34, AUR, 'c')
    hline(c, 60, y-98, W-60)
    t(c, '"Klasik paketlerde otobüs ve kalabalik var. Bunda yok."', W/2, y-115,
      'AI', 11, DIM, 'c')

    cards = [
        (AUR,  'Butik Grup',         'Maks. 15 kisi. Herkes birbirini tanir, kimse kaybolmaz.'),
        (GOLD, '2x Aurora Avi',      "Her gece degil, en iyi 2 geceyi seciyoruz. Dogru zaman = 3x daha yüksek ihtimal."),
        (BLUE, 'Fotograf Destegi',   'Aurora önünde cekileri biz yapiyoruz. Tripod, uzun pozlama, profesyonel kadraj.'),
        (PURP, 'Tek Rehber',         '3 sehirde de ayni rehber. Sürekli degisen yüzler yok.'),
        (RED,  '4 Yildizli',         '3 ayri sehirde konforlu oteller. Gercek isinma, gercek dinlenme.'),
        (AUR,  'Adim Adim Destek',   'E-vize, ucak, bavul listesi — her adimda yanimizdayiz.'),
    ]

    cw2 = (W-60)/3 - 4
    bh = 105
    sy = y-150

    for i,(col,title,desc) in enumerate(cards):
        row, colx = i//3, i%3
        bx = 30 + colx*(cw2+6)
        by = sy - row*(bh+8)
        c.setFillColor(Color(col.red,col.green,col.blue,alpha=0.08))
        c.roundRect(bx, by, cw2, bh, 7, fill=1, stroke=0)
        c.setStrokeColor(Color(col.red,col.green,col.blue,alpha=0.3))
        c.setLineWidth(0.5)
        c.roundRect(bx, by, cw2, bh, 7, fill=0, stroke=1)
        bar(c, bx, by+12, h2=bh-24, w2=3, col=col)
        t(c, title, bx+12, by+bh-22, 'AB', 10, col)
        wrap(c, desc, bx+12, by+bh-38, cw2-20, 'AU', 8.5, DIM, leading=13)

    lv_logo(c); pgnum(c,3); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.4  SOSYAL ATMOSFER
# ═══════════════════════════════════════════════════════════════════════════
def p4(c):
    bg(c)
    photo_band(c, IMG+'ki-aurora-grup.jpg', H*0.5, H*0.5, a=0.3)

    y = H-75
    section_tag(c, 'GRUP ATMOSFERI', 30, y, AUR)
    t(c, 'Yalniz basiniza gelin,', 30, y-36, 'AB', 28, WHITE)
    t(c, 'birlikte dönersiniz.', 30, y-70, 'AB', 28, AUR)
    hline(c, 30, y-84, W-30)
    wrap(c, 'Grubumuzun büyük cogunlugu yalniz geliyor — ve bu tamamen normal. '
         "Aurora'nin altinda herkes ayni anda ayni seyi yasiyor; "
         'o ani paylasmak insanlari aninda kaynaştiriyor.',
         30, y-100, W-60, 'AU', 10.5, DIM, leading=16)

    items = [
        ('Geziden 10 gün önce WhatsApp grubu açilir', 'Birbirinizi tanimaya basliyorsunuz daha gelmeden.'),
        ('Giris gecesi varis yemegi', 'Tüm grup bir arada, sehre ilk bakis birlikte.'),
        ('Aurora anini birlikte yasiyorsunuz', 'O yesil perdeler ciktiginda yaniinizda insanlar var.'),
        ('Fotograflari biz cekiyoruz', 'Aurora önünde solo veya grup cekimi — icerik hazir.'),
        ('Tur bitince grup bitmez', 'Önceki gruplardan insanlar hâlâ bir arada.'),
    ]
    iy = y-155
    for title,desc in items:
        dot(c, 36, iy+4, r=3, col=AUR)
        t(c, title, 48, iy, 'AB', 10, WHITE)
        t(c, desc, 48, iy-14, 'AU', 8.5, DIM)
        iy -= 38

    # Alintilik
    c.setFillColor(Color(0,0,0,alpha=0.65))
    c.rect(0, 0, W, 118, fill=1, stroke=0)
    hline(c, 30, 118, W-30)
    t(c, '"Yalniz gelip aile olarak döndük."', W/2, 83, 'AI', 14, Color(1,1,1,alpha=0.82), 'c')
    t(c, '— Kuzey Isiklari, Ocak 2025 grubu', W/2, 62, 'AU', 9, DIM, 'c')

    lv_logo(c); pgnum(c,4); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.5  KONTENJANLAR
# ═══════════════════════════════════════════════════════════════════════════
def p5(c):
    bg(c, BG2)
    stars(c, 50, 99)
    aurora_glow(c, H*0.33)

    y = H-70
    section_tag(c, '2026 - 2027 KONTENJANLARI', W/2, y, AUR, 'c')
    t(c, 'Hangi tarihte geliyorsunuz?', W/2, y-40, 'AB', 30, WHITE, 'c')

    dates = [
        (AUR,  'NOEL',         '12 - 19 Aralik 2026',
         'Aralikta Moskova: Noel pazarlari,', 'Kizil Meydan buz pateni.'),
        (GOLD, 'YILBASI',      '26 Ara - 02 Oca 2027',
         "Yilbasi gecesini Murmansk'ta,", 'Aurora altinda kutlayin.'),
        (BLUE, 'ARA TATIL 1',  '16 - 23 Ocak 2027',
         'Okul ara tatilinde tam zamani —', 'Kutup gecesi, Husky, Aurora.'),
        (PURP, 'ARA TATIL 2',  '24 - 31 Ocak 2027',
         'Subata yakin, en güçlü', 'auroralarin görüldügü dönem.'),
    ]

    bw = (W-60)/2 - 5
    bh = 158
    positions = [
        (30, y-100), (30+bw+10, y-100),
        (30, y-100-bh-10), (30+bw+10, y-100-bh-10),
    ]

    for (bx,by),(col,tag,date,d1,d2) in zip(positions, dates):
        c.setFillColor(Color(col.red,col.green,col.blue,alpha=0.08))
        c.roundRect(bx, by, bw, bh, 9, fill=1, stroke=0)
        c.setStrokeColor(Color(col.red,col.green,col.blue,alpha=0.38))
        c.setLineWidth(1)
        c.roundRect(bx, by, bw, bh, 9, fill=0, stroke=1)
        # üst renkli serit
        c.setFillColor(Color(col.red,col.green,col.blue,alpha=0.88))
        c.roundRect(bx, by+bh-30, bw, 30, 9, fill=1, stroke=0)
        c.rect(bx, by+bh-30, bw, 15, fill=1, stroke=0)
        t(c, tag, bx+bw/2, by+bh-18, 'AB', 9, BG, 'c')
        t(c, date, bx+12, by+bh-52, 'AB', 13, WHITE)
        dot(c, bx+13, by+bh-70, r=2.5, col=AUR)
        t(c, 'Kayit Acik', bx+22, by+bh-73, 'AB', 8, AUR)
        t(c, d1, bx+12, by+bh-92, 'AU', 9, DIM)
        t(c, d2, bx+12, by+bh-107, 'AU', 9, DIM)

    ny = y-100-2*(bh+10)-18
    c.setFillColor(Color(0,0,0,alpha=0.4))
    c.roundRect(30, ny-30, W-60, 36, 7, fill=1, stroke=0)
    t(c, 'Yerinizi 595 EUR on odeme ile garantileyebilirsiniz.', W/2, ny-10, 'AU', 9, DIM, 'c')

    lv_logo(c); pgnum(c,5); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.6  KONAKLAMA
# ═══════════════════════════════════════════════════════════════════════════
def p6(c):
    bg(c)
    stars(c, 30, 21)
    photo_band(c, IMG+'enson-kizilmeydan-grup.jpg', H-255, 222, a=0.48)

    y = H-75
    section_tag(c, 'KONAKLAMA', W/2, y, GOLD, 'c')
    t(c, '3 Sehir  |  4 Yildizli  |  7 Gece', W/2, y-36, 'AB', 24, WHITE, 'c')
    hline(c, 40, y-52, W-40)

    hotels = [
        (RED,  'MOSKOVA',         '2 Gece', 'Sehir merkezi.', "Kremlin'e yurume mesafesi."),
        (AUR,  'MURMANSK',        '3 Gece', 'Aurora avina yakin konum.', 'Sicak, konforlu, 24 saat.'),
        (BLUE, 'ST. PETERSBURG',  '2 Gece', 'Nevsky Bulvari bolgesi.', "Hermitage'a yakin."),
    ]
    hw = (W-60)/3 - 6
    hh = 130
    hy = y-68

    for i,(col,city,nights,d1,d2) in enumerate(hotels):
        bx = 30 + i*(hw+9)
        by = hy - hh
        c.setFillColor(BG3)
        c.roundRect(bx, by, hw, hh, 8, fill=1, stroke=0)
        c.setStrokeColor(Color(col.red,col.green,col.blue,alpha=0.4))
        c.setLineWidth(1)
        c.roundRect(bx, by, hw, hh, 8, fill=0, stroke=1)
        c.setFillColor(Color(col.red,col.green,col.blue,alpha=0.85))
        c.roundRect(bx, by+hh-28, hw, 28, 8, fill=1, stroke=0)
        c.rect(bx, by+hh-28, hw, 14, fill=1, stroke=0)
        t(c, city, bx+hw/2, by+hh-17, 'AB', 8.5, BG, 'c')
        t(c, nights, bx+hw/2, by+hh-44, 'AB', 14, WHITE, 'c')
        t(c, '* * * *', bx+hw/2, by+hh-61, 'AU', 9, GOLD, 'c')
        t(c, d1, bx+hw/2, by+hh-76, 'AU', 8.5, DIM, 'c')
        t(c, d2, bx+hw/2, by+hh-90, 'AU', 8.5, DIM, 'c')

    fy = hy - hh - 26
    hline(c, 30, fy, W-30)
    feats = ['Ozel banyo','Mini bar','Sinirsiz WiFi','Kasa','Kahvalti dahil','Transfer dahil']
    fw = (W-60)/3
    for i,f in enumerate(feats):
        r,col = i//3, i%3
        t(c, '+ ' + f, 30+col*fw, fy-20-r*18, 'AU', 9, DIM)

    lv_logo(c); pgnum(c,6); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.7  GUN 1-2: MOSKOVA
# ═══════════════════════════════════════════════════════════════════════════
def p7(c):
    bg(c)
    stars(c, 28, 5)
    photo_band(c, IMG+'enson-kizilmeydan-selfie.jpg', H-265, 234, a=0.42)

    y = H-78
    day_hdr(c, 'GUN 1-2', 'MOSKOVA', 'Kizil Meydan & Kis Masali', RED, y)

    rows = [
        ('GUN 1',  'Istanbul - Moskova Ucusu', ''),
        ('Aksam',  'Check-in & Sehre Ilk Bakis', '4 yildizli otel, serbest zaman'),
        ('GUN 2',  'Noel Pazarlari', 'Kizil Meydan, sicak icecek molasi'),
        ('Gündüz', 'GUM & Kremlin Cevresi', 'Christ the Savior Katedrali'),
        ('Gündüz', 'Moskova Metrosu', 'Dünyanin en güzel metro duraklari'),
        ('Aksam',  'Gece Kizil Meydan', 'Buz pateni (istege baglidir)'),
    ]
    iy = y-40
    for time2,title,sub in rows:
        dot(c, 36, iy+4, r=2.5, col=RED)
        t(c, time2, 48, iy+2, 'AB', 8, RED)
        t(c, title, 48, iy-11, 'AB', 10, WHITE)
        if sub: t(c, sub, 48, iy-23, 'AU', 8.5, DIM)
        iy -= 40 if sub else 28

    # Bilgi kutusu
    bx = W-175; by = y-135
    c.setFillColor(Color(0.8,0.1,0.1,alpha=0.1))
    c.roundRect(bx, by-115, 145, 122, 7, fill=1, stroke=0)
    c.setStrokeColor(Color(0.8,0.1,0.1,alpha=0.3))
    c.setLineWidth(0.5)
    c.roundRect(bx, by-115, 145, 122, 7, fill=0, stroke=1)
    t(c, 'MOSKOVA', bx+72, by-4, 'AB', 9, RED, 'c')
    for i,line in enumerate(['2 gece  |  4 yildizli','Noel pazarlari','Metro turlari','Kremlin cevresi','Kizil Meydan']):
        t(c, line, bx+72, by-22-i*16, 'AU', 8.5, DIM, 'c')

    lv_logo(c); pgnum(c,7); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.8  GUN 3: MURMANSK - AURORA
# ═══════════════════════════════════════════════════════════════════════════
def p8(c):
    photo_full(c, IMG+'ki-new-3.jpg', a=0.55)
    stars(c, 70, 18)
    aurora_glow(c, H*0.49)

    y = H-78
    day_hdr(c, 'GUN 3', 'MURMANSK', "Kutup Sehrine Hos Geldiniz", AUR, y)

    rows = [
        ('18:00', "Murmansk'a Inis", 'Dünyanin en büyük kutup dairesi sehri'),
        ('19:00', 'Otel Check-in', 'Isinma, dinlenme, gece icin hazirlik'),
        ('20:15', 'Aksam Yemegi', 'Grup birlikte — restorantta bulusma'),
    ]
    iy = y-42
    for time2,title,sub in rows:
        dot(c, 36, iy+4, r=2.5, col=AUR)
        t(c, time2, 48, iy+2, 'AB', 8, AUR)
        t(c, title, 48, iy-11, 'AB', 10, WHITE)
        t(c, sub, 48, iy-23, 'AU', 8.5, DIM)
        iy -= 40

    # Aurora vurgu kutusu
    c.setFillColor(Color(0,0.78,0.63,alpha=0.15))
    c.roundRect(30, iy-54, W-60, 58, 9, fill=1, stroke=0)
    c.setStrokeColor(Color(0,0.78,0.63,alpha=0.55))
    c.setLineWidth(1.2)
    c.roundRect(30, iy-54, W-60, 58, 9, fill=0, stroke=1)
    t(c, 'GECE — ILK AURORA AVI', 44, iy, 'AB', 13, AUR)
    t(c, 'Kosullar uygunsa direkt ava — isik avcisi ekip yanimizda', 44, iy-18, 'AU', 9.5, DIM)

    # Not
    c.setFillColor(Color(0,0,0,alpha=0.62))
    c.roundRect(30, 100, W-60, 38, 7, fill=1, stroke=0)
    t(c, 'Aurora Borealis anlik bir doga olayidir. En iyi 2 geceyi günes aktivitesini', W/2, 128, 'AU', 9, Color(1,1,1,alpha=0.75), 'c')
    t(c, 'takip ederek belirliyoruz. Her gece ava cikmayi garanti edemeyiz.', W/2, 114, 'AU', 9, Color(1,1,1,alpha=0.75), 'c')

    lv_logo(c); pgnum(c,8); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.9  GUN 4: HUSKY
# ═══════════════════════════════════════════════════════════════════════════
def p9(c):
    bg(c)
    stars(c, 38, 8)
    photo_band(c, IMG+'ki-husky-erkek.jpg', H-305, 273, a=0.34)

    y = H-78
    day_hdr(c, 'GUN 4', 'MURMANSK / LAPLAND', 'Husky Parki & Lapland Macerasi', AUR, y)

    acts = [
        (AUR,  'Husky Kizagi', 'Surücü siz oluyorsunuz'),
        (GOLD, 'Ren Geyigi',   'Geleneksel Lapland kizagi'),
        (BLUE, 'Kar Motoru',   'Karli ormanda safari'),
        (PURP, "Husky'lerle",  'Köpeklerle burun buruna'),
    ]
    aw = (W-60)/4 - 4
    ah = 80
    ay = y-54

    for i,(col,title,desc) in enumerate(acts):
        ax = 30 + i*(aw+5)
        by2 = ay - ah
        c.setFillColor(Color(col.red,col.green,col.blue,alpha=0.09))
        c.roundRect(ax, by2, aw, ah, 7, fill=1, stroke=0)
        c.setStrokeColor(Color(col.red,col.green,col.blue,alpha=0.24))
        c.setLineWidth(0.5)
        c.roundRect(ax, by2, aw, ah, 7, fill=0, stroke=1)
        t(c, title, ax+aw/2, ay-18, 'AB', 9.5, col, 'c')
        t(c, desc, ax+aw/2, ay-34, 'AU', 8, DIM, 'c')

    iy = ay - ah - 18
    rows = [
        ('09:50', 'Lobide Bulusma', 'Transfer hazir'),
        ('11:00', 'Husky Parkina Varis', '~1 saatlik yolculuk'),
        ('16:40', 'Aksam Yemegi & Dinlenme', ''),
        ('Gece',  'Aurora Aktivite Degerlendirmesi', 'Kosullar uygunsa 2. ava cikis'),
    ]
    for time2,title,sub in rows:
        dot(c, 36, iy+4, r=2.5, col=AUR)
        t(c, time2, 48, iy+2, 'AB', 8, AUR)
        t(c, title, 48, iy-11, 'AB', 10, WHITE)
        if sub: t(c, sub, 48, iy-23, 'AU', 8.5, DIM)
        iy -= 40 if sub else 28

    lv_logo(c); pgnum(c,9); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.10  GUN 5: BUZKIRAN, ICE FLOATING, SAMI
# ═══════════════════════════════════════════════════════════════════════════
def p10(c):
    bg(c, BG2)
    stars(c, 33, 15)

    r1 = img(IMG+'buz-yuzme.jpg')
    r2 = img(IMG+'ki-sami-grup.jpg')
    if r1: c.drawImage(r1, 0, H*0.5, W/2, H*0.5, preserveAspectRatio=False)
    if r2: c.drawImage(r2, W/2, H*0.5, W/2, H*0.5, preserveAspectRatio=False)
    if r1: overlay(c, x=0, y=H*0.5, w=W/2, h=H*0.5, a=0.34)
    if r2: overlay(c, x=W/2, y=H*0.5, w=W/2, h=H*0.5, a=0.34)

    y = H-78
    day_hdr(c, 'GUN 5', 'MURMANSK', 'Buzkiran  |  Buz Yüzme  |  Sami Köyü', AUR, y)

    rows = [
        ('10:00', 'Alyosha Tepesi', "Murmansk'in simgesi — panoramik liman manzarasi"),
        ('11:00', 'Lenin Buzkiran Gemisi', 'Dünyanin ilk nükleer buzkiranini içeriden'),
        ('13:00', 'ICE FLOATING  (+130 EUR)', "Donmus Kuzey Buz Denizi'nde yüzme — istege baglidir"),
        ('15:00', 'Sami Köyü Programi', 'Geleneksel Sami kiyafetleri, ren geyigi'),
        ('Gece',  'Aurora Degerlendirmesi', '2. ava cikis planlamasi'),
    ]
    iy = y-42
    for time2,title,sub in rows:
        is_ice = 'ICE' in title
        col2 = GOLD if is_ice else AUR
        dot(c, 36, iy+4, r=2.5, col=col2)
        t(c, time2, 48, iy+2, 'AB', 8, col2)
        t(c, title, 48, iy-11, 'AB', 10, GOLD if is_ice else WHITE)
        if sub: t(c, sub, 48, iy-23, 'AU', 8.5, DIM)
        iy -= 40

    c.setFillColor(Color(0.13,0.52,0.85,alpha=0.12))
    c.roundRect(30, 168, W-60, 40, 7, fill=1, stroke=0)
    c.setStrokeColor(Color(0.13,0.52,0.85,alpha=0.38))
    c.setLineWidth(0.5)
    c.roundRect(30, 168, W-60, 40, 7, fill=0, stroke=1)
    t(c, 'ICE FLOATING — Istege Bagli  (+130 EUR)', W/2, 198, 'AB', 9, BLUE, 'c')
    t(c, "Drysuit giyerek Kuzey Buz Denizi'nde yüzme. Ömürlük bir deneyim.", W/2, 183, 'AU', 8.5, DIM, 'c')

    lv_logo(c); pgnum(c,10); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.11  GUN 6-7: ST. PETERSBURG
# ═══════════════════════════════════════════════════════════════════════════
def p11(c):
    bg(c)
    stars(c, 28, 6)
    photo_band(c, IMG+'enson-orman-grup.jpg', H-275, 244, a=0.44)

    y = H-78
    day_hdr(c, 'GUN 6-7', 'ST. PETERSBURG', 'Hermitage  |  Kanallar  |  Nevsky', BLUE, y)
    t(c, '"Kuzey\'in Venedigi" — sanat ve tarihin tam ortasi.', 30, y-40, 'AI', 10.5, DIM)

    rows = [
        ('GUN 6 Ogle', 'Murmansk - St. Petersburg', 'Ic hat ucusu  |  Otel check-in'),
        ('GUN 6 Aksam','Nevsky Bulvari & Aksam Yemegi', 'Sehrin ana caddesinde serbest zaman'),
        ('GUN 7 Gündüz','Hermitage Müzesi', 'Dünyanin en büyük müzelerinden — 3 milyon eser'),
        ('GUN 7 Ogle', 'Kanallar & Sehir Kesfi', 'Kanal boyunca yürüyüs, köprüler'),
        ('GUN 7 Aksam','Aksam Yemegi & Vedalasma', 'Son gece birlikte — anilar taze'),
    ]
    iy = y-60
    for time2,title,sub in rows:
        dot(c, 36, iy+4, r=2.5, col=BLUE)
        t(c, time2, 48, iy+2, 'AB', 8, BLUE)
        t(c, title, 48, iy-11, 'AB', 10, WHITE)
        if sub: t(c, sub, 48, iy-23, 'AU', 8.5, DIM)
        iy -= 42

    hline(c, 30, 148, W-30)
    highs = ['Hermitage','Kanallar','Kazansky Katedral','Nevsky Alisveris','Kis Sarayi']
    hw2 = (W-60)/len(highs)
    for i,h2 in enumerate(highs):
        t(c, '+ '+h2, 30+i*hw2, 130, 'AU', 8.5, DIM)

    lv_logo(c); pgnum(c,11); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.12  GUN 8: DONUS
# ═══════════════════════════════════════════════════════════════════════════
def p12(c):
    photo_full(c, IMG+'aurora-portrait.jpg', a=0.60)
    stars(c, 65, 44)
    aurora_glow(c, H*0.48)

    y = H-78
    day_hdr(c, 'GUN 8', 'ST. PETERSBURG -> ISTANBUL', 'Donus', AUR, y)

    rows = [('07:00','Otel Kahvaltisi',''), ('13:30','Lobide Bulusma','Havalimani transferi'),
            ('17:30','Istanbul Ucusu','"Yaninda kuzey isiklari anilari..."')]
    iy = y-42
    for time2,title,sub in rows:
        dot(c, 36, iy+4, r=2.5, col=AUR)
        t(c, time2, 48, iy+2, 'AB', 8, AUR)
        t(c, title, 48, iy-11, 'AB', 10, WHITE)
        if sub: t(c, sub, 48, iy-23, 'AI', 9, DIM)
        iy -= 40

    cy = H*0.37
    c.setFillColor(Color(0,0,0,alpha=0.54))
    c.roundRect(45, cy-70, W-90, 80, 10, fill=1, stroke=0)
    c.setStrokeColor(Color(0,0.78,0.63,alpha=0.38))
    c.setLineWidth(0.8)
    c.roundRect(45, cy-70, W-90, 80, 10, fill=0, stroke=1)
    t(c, '"Aurora\'yu bir kez gördükten sonra', W/2, cy-2, 'AI', 13, Color(1,1,1,alpha=0.86), 'c')
    t(c, 'hiçbir sey ayni olmaz."', W/2, cy-22, 'AI', 13, Color(1,1,1,alpha=0.86), 'c')
    t(c, '— Her tur sonrasi duyduğumuz sey bu.', W/2, cy-48, 'AU', 9, DIM, 'c')

    lv_logo(c); pgnum(c,12); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.13  AURORA HAKKINDA
# ═══════════════════════════════════════════════════════════════════════════
def p13(c):
    bg(c, BG2)
    stars(c, 78, 77)
    aurora_glow(c, H*0.43)

    r1 = img(IMG+'enson-aurora-orman.jpg')
    if r1:
        c.drawImage(r1, W/2, H*0.1, W/2, H*0.52, preserveAspectRatio=False)
        overlay(c, x=W/2, y=H*0.1, w=W/2, h=H*0.52, a=0.4)

    y = H-70
    section_tag(c, 'KUZEY ISIKLARI HAKKINDA', 30, y, AUR)
    t(c, "Aurora Borealis'i", 30, y-36, 'AB', 26, WHITE)
    t(c, 'nerede, ne zaman görürsünüz?', 30, y-68, 'AB', 26, AUR)

    facts = [
        ('Kutup Gecesi', "Murmansk'ta Aralik-Ocak'ta günde 21 saate varan karanlik. Aurora icin mükemmel."),
        ('En Iyi Sezon', 'Aralik-Mart arasi en yüksek aurora frekansi. Bu pencereye özellikle giriyoruz.'),
        ('Solar Zirve',  '2025-2027 günes aktivitesinin zirvesi. Aurora görme orani tarihsel olarak yüksekte.'),
        ('Strateji',     '2 gece planliyoruz. Dogru gece secmek görme ihtimalini 3 katina cikariyor.'),
        ('Fotograf',     'Aurora kamerayla gözden daha güçlü görünür. Cekimleri biz yapiyoruz.'),
    ]
    iy = y-100
    for title,desc in facts:
        dot(c, 35, iy+4, r=3, col=AUR)
        t(c, title, 46, iy, 'AB', 10.5, WHITE)
        iy = wrap(c, desc, 46, iy-16, W/2-56, 'AU', 8.5, DIM, 12) - 8

    lv_logo(c); pgnum(c,13); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.14  DAHIL / DAHIL DEGIL
# ═══════════════════════════════════════════════════════════════════════════
def p14(c):
    bg(c, BG3)
    stars(c, 22, 31)

    y = H-65
    section_tag(c, 'TUR KAPSAMI', W/2, y, AUR, 'c')
    t(c, 'Dahil & Dahil Degil', W/2, y-38, 'AB', 28, WHITE, 'c')

    cw2 = (W-70)/2
    top = y-82
    bot = 82

    # Sol — Dahil
    c.setFillColor(Color(0,0.78,0.63,alpha=0.07))
    c.roundRect(30, bot, cw2, top-bot, 9, fill=1, stroke=0)
    c.setStrokeColor(Color(0,0.78,0.63,alpha=0.28))
    c.setLineWidth(0.5)
    c.roundRect(30, bot, cw2, top-bot, 9, fill=0, stroke=1)
    t(c, 'DAHIL', 42, top-10, 'AB', 11, AUR)
    inc = [
        "Moskova'da 2 gece 4 yildizli",
        "Murmansk'ta 3 gece 4 yildizli",
        "St. Petersburg'da 2 gece 4 yildizli",
        'Tüm havalimani-otel transferleri',
        'Husky kizagi deneyimi',
        'Ren geyigi kizagi',
        'Kar motoru safarisi',
        'Sami köyü ziyareti',
        '2x Aurora Avi (rehber esliginde)',
        'Isik avi fotograf cekimi',
        '7 sabah kahvaltisi',
        'Rusya ici ucus (MUR-SPB)',
        'WhatsApp grubu & hazirlik destegi',
    ]
    iy = top-28
    for item in inc:
        dot(c, 42, iy+4, r=2.5, col=AUR)
        t(c, item, 52, iy, 'AU', 9, WHITE)
        iy -= 17

    # Sag — Dahil Degil
    ex = 30+cw2+10
    c.setFillColor(Color(0.8,0.2,0.2,alpha=0.06))
    c.roundRect(ex, bot, cw2, top-bot, 9, fill=1, stroke=0)
    c.setStrokeColor(Color(0.8,0.2,0.2,alpha=0.22))
    c.setLineWidth(0.5)
    c.roundRect(ex, bot, cw2, top-bot, 9, fill=0, stroke=1)
    t(c, 'DAHIL DEGIL', ex+12, top-10, 'AB', 11, RED)
    exc = [
        ('Yurt disi ucak biletleri',   '~750 EUR  |  IST-MOW ve SPB-IST'),
        ('E-Vize (50 EUR)',             'Kendiniz yapabilirsiniz'),
        ('Ice Floating (+130 EUR)',     'Istege baglidir'),
        ('Ogle & aksam yemekleri',      'Kahvalti dahil, digerleri serbest'),
        ('Müze giris ücretleri',        'Hermitage vb.'),
        ('Kisisel harcamalar',          '~150-250 EUR tahmin'),
    ]
    iy2 = top-28
    for title,note in exc:
        dot(c, ex+12, iy2+4, r=2.5, col=RED)
        t(c, title, ex+22, iy2, 'AB', 9, HexColor('#FF7070'))
        t(c, note, ex+22, iy2-13, 'AU', 8, DIM)
        iy2 -= 36

    lv_logo(c); pgnum(c,14); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.15  KAYIT SURECI
# ═══════════════════════════════════════════════════════════════════════════
def p15(c):
    bg(c, BG2)
    stars(c, 40, 55)
    aurora_glow(c, H*0.29)

    y = H-70
    section_tag(c, 'NASIL KATILIRSINIZ?', W/2, y, AUR, 'c')
    t(c, '4 Adimda Yerinizi Alin', W/2, y-40, 'AB', 30, WHITE, 'c')

    steps = [
        (AUR,  '01', 'Formu Doldurun',
         'lostvoyages.com/kuzey-isiklari.html sayfasindaki',
         'on kayit formunu doldurun.'),
        (GOLD, '02', '595 EUR On Odeme',
         'Yerinizi on odeme ile garantileyebilirsiniz.',
         'Kalan tutar geziden 1 ay oncesine kadar tamamlanir.'),
        (BLUE, '03', "WhatsApp Grubuna Girin",
         'Geziden 10 gün önce grup açilir.',
         'E-vize, bavul listesi, her sey orada.'),
        (PURP, '04', 'Ucak Biletini Alin',
         'Yeriniz kesinlesince ucak linkini paylasiyoruz.',
         'Birlikte ayni ucusta gitmeyi tercih ediyoruz.'),
    ]

    sw = (W-60)/2 - 5
    sh = 130
    positions = [
        (30, y-90), (30+sw+10, y-90),
        (30, y-90-sh-10), (30+sw+10, y-90-sh-10),
    ]

    for (bx,by2),(col,num,title,d1,d2) in zip(positions, steps):
        c.setFillColor(BG3)
        c.roundRect(bx, by2-sh, sw, sh, 9, fill=1, stroke=0)
        c.setStrokeColor(Color(col.red,col.green,col.blue,alpha=0.32))
        c.setLineWidth(1)
        c.roundRect(bx, by2-sh, sw, sh, 9, fill=0, stroke=1)
        c.setFillColor(Color(col.red,col.green,col.blue,alpha=0.85))
        c.circle(bx+22, by2-17, 13, fill=1, stroke=0)
        t(c, num, bx+22, by2-21, 'AB', 10, BG, 'c')
        t(c, title, bx+42, by2-13, 'AB', 10.5, WHITE)
        t(c, d1, bx+12, by2-sh+48, 'AU', 8.5, DIM)
        t(c, d2, bx+12, by2-sh+34, 'AU', 8.5, DIM)

    cta_y = y-90-2*(sh+10)-16
    c.setFillColor(AUR)
    c.roundRect(W/2-140, cta_y-30, 280, 38, 9, fill=1, stroke=0)
    t(c, 'lostvoyages.com  ->  Kuzey Isiklari', W/2, cta_y-8, 'AB', 11, BG, 'c')
    t(c, 'WhatsApp: +90 545 170 69 27', W/2, cta_y-52, 'AU', 9, DIM, 'c')

    lv_logo(c); pgnum(c,15); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.16  ODEME & IPTAL
# ═══════════════════════════════════════════════════════════════════════════
def p16(c):
    bg(c, BG3)
    stars(c, 20, 88)

    y = H-68
    section_tag(c, 'ODEME & IPTAL', W/2, y, GOLD, 'c')
    t(c, 'Seffaf Kosullar', W/2, y-36, 'AB', 26, WHITE, 'c')

    # Odeme plani
    py = y-80
    c.setFillColor(Color(0.83,0.63,0.09,alpha=0.08))
    c.roundRect(30, py-92, W-60, 96, 9, fill=1, stroke=0)
    c.setStrokeColor(Color(0.83,0.63,0.09,alpha=0.3))
    c.setLineWidth(0.5)
    c.roundRect(30, py-92, W-60, 96, 9, fill=0, stroke=1)
    t(c, 'ODEME PLANI', 44, py, 'AB', 10, GOLD)
    for i,(lbl,amt,note) in enumerate([
        ('Rezervasyon',          '595 EUR', 'Yerinizi garantilemek icin'),
        ('Kalan tutar',          '1.600 EUR', 'Geziden 1 ay oncesine kadar'),
        ('Toplam (ucak haric)', '2.195 EUR', 'Tüm vergiler dahil'),
    ]):
        iy = py - 24 - i*27
        t(c, lbl, 44, iy, 'AU', 9.5, WHITE)
        t(c, amt, W-44, iy, 'AB', 10, GOLD, 'r')
        t(c, note, 44, iy-12, 'AU', 8, DIM)

    # Iptal
    pol_y = py-115
    t(c, 'IPTAL POLITIKASI', 30, pol_y, 'AB', 10, WHITE)
    pols = [
        ('Geziye 60+ gün kala iptal',      '80 EUR kesinti — kalan iade edilir'),
        ('Geziye 30-60 gün kala iptal',    '100 EUR kesinti — kalan iade edilir'),
        ('Geziye 30 günden az kala iptal', 'Kapora iade edilmez'),
    ]
    iy2 = pol_y-20
    for cond,result in pols:
        t(c, cond, 30, iy2, 'AU', 9, DIM)
        t(c, result, W-30, iy2, 'AB', 9, WHITE, 'r')
        hline(c, 30, iy2-7, W-30)
        iy2 -= 24

    # Notlar
    notes_y = pol_y-96
    hline(c, 30, notes_y, W-30)
    notes = [
        'Tek kisilik oda farki: +400 EUR',
        'E-vize basvurusu: kendiniz (50 EUR) veya biz yapalim (100 EUR)',
        'Ucak biletleri ~750 EUR (4 ucus) — grupla birlikte alinir',
        'Tüm ödemeler Türk Lirasi üzerinden de yapilabilir',
    ]
    iy3 = notes_y-18
    for note in notes:
        dot(c, 36, iy3+4, r=2, col=DIM)
        t(c, note, 46, iy3, 'AU', 8.5, DIM)
        iy3 -= 17

    lv_logo(c); pgnum(c,16); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# S.17  FIYAT
# ═══════════════════════════════════════════════════════════════════════════
def p17(c):
    photo_full(c, IMG+'ki-new-5.jpg', a=0.56)
    stars(c, 80, 111)
    aurora_glow(c, H*0.45)

    y = H-75
    section_tag(c, 'FIYATLANDIRMA', W/2, y, AUR, 'c')
    t(c, '7 gece · 3 sehir · Husky · 2x Aurora Avi · 4 yildizli otel', W/2, y-34,
      'AU', 11, Color(1,1,1,alpha=0.72), 'c')
    hline(c, W/2-115, y-46, W/2+115, col=Color(1,1,1,alpha=0.3))

    t(c, 'Kisi Basi Fiyat', W/2, y-68, 'AU', 14, DIM, 'c')
    t(c, '2.195 EUR', W/2, y-128, 'AB', 58, GOLD, 'c')
    t(c, 'ucak haric  |  tum vergiler dahil', W/2, y-152, 'AU', 10, DIM, 'c')

    # Fiyat tablosu
    tw = 274
    tx = W/2-tw/2
    table_y = y-184

    rows = [
        ('Gezi ücreti (kisi basi)',     '2.195 EUR', True),
        ('Tek kisilik oda farki',        '+400 EUR', False),
        ('Ice Floating (istege bagli)', '+130 EUR', False),
        ('E-vize (kendiniz)',            '50 EUR', False),
        ('Ucak biletleri (tahmin)',      '~750 EUR', False),
    ]
    rh = len(rows)*28 + 16
    c.setFillColor(Color(0,0,0,alpha=0.58))
    c.roundRect(tx, table_y-rh, tw, rh, 9, fill=1, stroke=0)
    c.setStrokeColor(Color(1,1,1,alpha=0.14))
    c.setLineWidth(0.5)
    c.roundRect(tx, table_y-rh, tw, rh, 9, fill=0, stroke=1)

    iy = table_y - 8
    for lbl,amt,is_main in rows:
        iy -= 8
        t(c, lbl, tx+10, iy, 'AB' if is_main else 'AU', 9, WHITE if is_main else DIM)
        t(c, amt, tx+tw-10, iy, 'AB', 9, GOLD if is_main else WHITE, 'r')
        if not is_main: hline(c, tx+10, iy-6, tx+tw-10, col=Color(1,1,1,alpha=0.07))
        iy -= 20

    oy = table_y - rh - 26
    t(c, 'On odeme ile yerinizi garantileyin:', W/2, oy, 'AU', 11, Color(1,1,1,alpha=0.8), 'c')
    t(c, '595 EUR', W/2, oy-32, 'AB', 26, AUR, 'c')

    c.setFillColor(AUR)
    c.roundRect(W/2-138, oy-68, 276, 30, 8, fill=1, stroke=0)
    t(c, 'lostvoyages.com  ->  Kayit Ol', W/2, oy-54, 'AB', 11, BG, 'c')
    t(c, 'WhatsApp: +90 545 170 69 27   |   @ahmeterenvci',
      W/2, oy-88, 'AU', 8.5, Color(1,1,1,alpha=0.5), 'c')

    lv_logo(c); pgnum(c,17); c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# ANA
# ═══════════════════════════════════════════════════════════════════════════
def main():
    cv = canvas.Canvas(OUT, pagesize=A4)
    cv.setTitle('Lost Voyages — Kuzey Isiklari Brosur')
    cv.setAuthor('Lost Voyages | Ahmet Eren')
    cv.setSubject('Moskova · Murmansk · St. Petersburg | 7 Gece 8 Gün')

    p1(cv); p2(cv); p3(cv); p4(cv); p5(cv); p6(cv); p7(cv); p8(cv); p9(cv)
    p10(cv); p11(cv); p12(cv); p13(cv); p14(cv); p15(cv); p16(cv); p17(cv)

    cv.save()
    size_kb = os.path.getsize(OUT)//1024
    print(f'OK: {OUT}  ({size_kb} KB)')

if __name__ == '__main__':
    main()

/* ─────────────────────────────────────────────
   LOST VOYAGES — globe.js
   Interactive destination globe for hero section
───────────────────────────────────────────── */
(function () {
  'use strict';

  const DESTINATIONS = [
    { name: 'Kuzey Işıkları', country: 'Rusya',     lat: 68.97, lng: 33.08,  flag: '🇷🇺', url: 'kuzey-isiklari.html', dates: 'Aralık 2026 · Yılbaşı',    desc: 'Murmansk\'ta aurora borealis altında unutulmaz bir kış masalı.' },
    { name: 'Sri Lanka',      country: 'Sri Lanka',  lat: 7.87,  lng: 80.77,  flag: '🇱🇰', url: 'sri-lanka.html',      dates: '2026 · Tarih Yakında',     desc: 'Çay tarlaları, safari ve kristal sularda baş döndüren bir ada deneyimi.' },
    { name: 'Ürdün',          country: 'Ürdün',      lat: 30.59, lng: 36.24,  flag: '🇯🇴', url: '#turlar',             dates: '2–6 Ekim 2026',            desc: 'Petra\'nın kanyonlarında kaybolan ve Wadi Rum\'da yıldızlara dokunan bir rota.' },
    { name: 'Fas',            country: 'Fas',        lat: 31.79, lng: -7.09,  flag: '🇲🇦', url: '#turlar',             dates: '23–29 Ekim 2026',          desc: 'Marakeş\'in labirentleri, Sahara\'nın sessizliği, Chefchaouen\'in mavisi.' },
    { name: 'Güney Kore',     country: 'Güney Kore', lat: 37.56, lng: 126.97, flag: '🇰🇷', url: '#turlar',             dates: '2026 · Planlanıyor',       desc: 'Seul\'ün neon ışıkları ile antik tapınaklar arasında şiirsel bir kontrast.' },
    { name: 'Bali',           country: 'Endonezya',  lat: -8.34, lng: 115.09, flag: '🇮🇩', url: '#turlar',             dates: '31 Ağu – 7 Eyl 2026',     desc: 'Pirinç terasları, tapınak törenleri ve Hint Okyanusu\'na açılan sonsuz gün batımları.' },
    { name: 'Vietnam',        country: 'Vietnam',    lat: 14.06, lng: 108.28, flag: '🇻🇳', url: '#turlar',             dates: '26 Ara – 1 Oca',           desc: 'Halong Körfezi\'nin yeşil sularında tekne gezisi ve Hanoi\'nin taze enerjisi.' },
    { name: 'Azerbaycan',     country: 'Azerbaycan', lat: 40.41, lng: 49.87,  flag: '🇦🇿', url: '#turlar',             dates: '1–5 Ağustos 2026',         desc: 'Bakü\'nün çağdaş silueti ve kadim kervansarayları arasında zamanda yolculuk.' },
    { name: 'Tayland',        country: 'Tayland',    lat: 7.90,  lng: 98.30,  flag: '🇹🇭', url: '#turlar',             dates: '14–21 Kasım 2026',         desc: 'Phi Phi adaları, maya koylar ve Phuket\'in turkuaz sularında özgürlük.' },
    { name: 'Karadağ',        country: 'Karadağ',    lat: 42.71, lng: 19.37,  flag: '🇲🇪', url: '#turlar',             dates: '25–28 Temmuz 2026',        desc: 'Adriyatik\'in gizli cenneti: fiyort koylarda kayık, ortaçağ surlarında akşam.' },
    { name: 'Japonya',        country: 'Japonya',    lat: 35.68, lng: 139.69, flag: '🇯🇵', url: '#turlar',             dates: '30 Eki – 7 Kas 2026',     desc: 'Tokyo\'nun kaotik zarafeti, Kyoto\'nun sakura duvarları ve Osaka\'nın lezzetleri.' },
    { name: 'Zanzibar',       country: 'Tanzanya',   lat: -6.16, lng: 39.19,  flag: '🇹🇿', url: '#turlar',             dates: '5–11 Aralık 2026',         desc: 'Beyaz kumlar, turkuaz okyanus ve baharatlı Stone Town sokaklarında bir rüya.' },
  ];

  let worldData  = null;
  let rotation   = [10, -20, 0];
  let autoRotate = true;
  let isDragging = false;
  let activePin  = -1;
  let canvas, ctx, projection, path;
  let W, H, R;
  let lastMX, lastMY;
  let resumeTimer;

  /* ── Init ── */
  function init() {
    canvas = document.getElementById('globeCanvas');
    if (!canvas || typeof d3 === 'undefined' || typeof topojson === 'undefined') return;

    const card = document.getElementById('destCard');
    setSize();
    setupInteraction(card);

    fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
      .then(r => r.json())
      .then(data => {
        worldData = topojson.feature(data, data.objects.countries);
        startLoop();
      })
      .catch(() => startLoop());
  }

  /* ── Canvas sizing ── */
  function setSize() {
    const wrap    = canvas.parentElement;
    const mobile  = window.innerWidth < 960;
    const maxSize = mobile
      ? Math.min(wrap.offsetWidth - 16, 320)
      : Math.min(wrap.offsetWidth, wrap.offsetHeight || 460, 460);

    W = maxSize;
    H = maxSize;
    R = W * 0.43;

    const dpr = window.devicePixelRatio || 1;
    canvas.width       = W * dpr;
    canvas.height      = H * dpr;
    canvas.style.width  = W + 'px';
    canvas.style.height = H + 'px';

    ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    projection = d3.geoOrthographic()
      .scale(R)
      .translate([W / 2, H / 2])
      .clipAngle(90)
      .rotate(rotation);

    path = d3.geoPath(projection, ctx);
  }

  /* ── Render frame ── */
  function render() {
    ctx.clearRect(0, 0, W, H);

    // Atmosphere glow
    const atm = ctx.createRadialGradient(W/2, H/2, R * 0.88, W/2, H/2, R * 1.20);
    atm.addColorStop(0,   'rgba(0,185,160,0.11)');
    atm.addColorStop(0.5, 'rgba(70,120,220,0.05)');
    atm.addColorStop(1,   'transparent');
    ctx.beginPath();
    ctx.arc(W/2, H/2, R * 1.20, 0, 2 * Math.PI);
    ctx.fillStyle = atm;
    ctx.fill();

    // Ocean
    const ocean = ctx.createRadialGradient(W * 0.38, H * 0.36, 0, W/2, H/2, R);
    ocean.addColorStop(0,   '#0e2038');
    ocean.addColorStop(0.7, '#081424');
    ocean.addColorStop(1,   '#040c16');
    ctx.beginPath();
    ctx.arc(W/2, H/2, R, 0, 2 * Math.PI);
    ctx.fillStyle = ocean;
    ctx.fill();

    // Graticule
    ctx.beginPath();
    path(d3.geoGraticule().step([30, 30])());
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth   = 0.5;
    ctx.stroke();

    // Land
    if (worldData) {
      ctx.beginPath();
      path(worldData);
      ctx.fillStyle   = '#173048';
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.09)';
      ctx.lineWidth   = 0.5;
      ctx.stroke();
    }

    // Globe rim
    ctx.beginPath();
    ctx.arc(W/2, H/2, R, 0, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(255,255,255,0.07)';
    ctx.lineWidth   = 1;
    ctx.stroke();

    drawPins();
  }

  /* ── Draw destination pins ── */
  function drawPins() {
    const rot = projection.rotate();

    DESTINATIONS.forEach((dest, i) => {
      const dist = d3.geoDistance([dest.lng, dest.lat], [-rot[0], -rot[1]]);
      if (dist > Math.PI / 2 - 0.04) return; // back side

      const p = projection([dest.lng, dest.lat]);
      if (!p) return;
      const [px, py] = p;
      const active   = activePin === i;

      // Glow ring
      const gr = ctx.createRadialGradient(px, py, 0, px, py, active ? 15 : 10);
      gr.addColorStop(0, `rgba(212,160,23,${active ? 0.55 : 0.22})`);
      gr.addColorStop(1, 'rgba(212,160,23,0)');
      ctx.beginPath();
      ctx.arc(px, py, active ? 15 : 10, 0, 2 * Math.PI);
      ctx.fillStyle = gr;
      ctx.fill();

      // Pin dot
      ctx.beginPath();
      ctx.arc(px, py, active ? 5.5 : 3.5, 0, 2 * Math.PI);
      ctx.fillStyle   = '#D4A017';
      ctx.fill();
      ctx.strokeStyle = active ? '#ffffff' : 'rgba(255,255,255,0.60)';
      ctx.lineWidth   = active ? 1.5 : 1;
      ctx.stroke();
    });
  }

  /* ── Animation loop ── */
  function startLoop() {
    let last = 0;
    (function tick(t) {
      requestAnimationFrame(tick);
      if (t - last < 16) return;
      last = t;
      if (autoRotate && !isDragging) {
        rotation[0] += 0.07;
        projection.rotate(rotation);
      }
      render();
    })(0);
  }

  /* ── Hit test ── */
  function hitTest(mx, my) {
    const rot = projection.rotate();
    for (let i = 0; i < DESTINATIONS.length; i++) {
      const dest = DESTINATIONS[i];
      const dist = d3.geoDistance([dest.lng, dest.lat], [-rot[0], -rot[1]]);
      if (dist > Math.PI / 2 - 0.04) continue;
      const p = projection([dest.lng, dest.lat]);
      if (!p) continue;
      const dx = mx - p[0], dy = my - p[1];
      if (Math.sqrt(dx * dx + dy * dy) < 16) return i;
    }
    return -1;
  }

  /* ── Card ── */
  function showCard(i, mx, my, card) {
    const dest = DESTINATIONS[i];
    activePin  = i;

    card.innerHTML = `
      <div class="dc-flag">${dest.flag}</div>
      <div class="dc-name">${dest.name}</div>
      <div class="dc-country">${dest.country}</div>
      <p class="dc-desc">${dest.desc}</p>
      <div class="dc-dates">🗓 ${dest.dates}</div>
      <a href="${dest.url}" class="dc-btn">Turu Gör →</a>
    `;

    let left = mx + 20;
    let top  = my - 20;
    if (left + 220 > W)  left = mx - 236;
    top = Math.max(4, Math.min(top, H - 240));

    card.style.left = left + 'px';
    card.style.top  = top  + 'px';
    card.classList.add('visible');
  }

  function hideCard(card) {
    activePin = -1;
    card.classList.remove('visible');
  }

  /* ── Canvas → logical coords ── */
  function toLogical(e) {
    const rect = canvas.getBoundingClientRect();
    return [
      (e.clientX - rect.left) * (W / rect.width),
      (e.clientY - rect.top)  * (H / rect.height),
    ];
  }

  function scheduleResume() {
    clearTimeout(resumeTimer);
    resumeTimer = setTimeout(() => { autoRotate = true; }, 2500);
  }

  /* ── Interaction ── */
  function setupInteraction(card) {

    /* Mouse hover */
    canvas.addEventListener('mousemove', e => {
      const [mx, my] = toLogical(e);

      if (isDragging) {
        const dx = e.clientX - lastMX;
        const dy = e.clientY - lastMY;
        rotation[0] += dx * 0.28;
        rotation[1]  = Math.max(-80, Math.min(80, rotation[1] - dy * 0.28));
        projection.rotate(rotation);
        lastMX = e.clientX;
        lastMY = e.clientY;
        return;
      }

      const hit = hitTest(mx, my);
      canvas.style.cursor = hit >= 0 ? 'pointer' : 'grab';
      if (hit >= 0) showCard(hit, mx, my, card);
      else          hideCard(card);
    });

    canvas.addEventListener('mousedown', e => {
      isDragging  = true;
      autoRotate  = false;
      lastMX      = e.clientX;
      lastMY      = e.clientY;
      canvas.style.cursor = 'grabbing';
      hideCard(card);
    });

    window.addEventListener('mouseup', () => {
      if (!isDragging) return;
      isDragging = false;
      canvas.style.cursor = 'grab';
      scheduleResume();
    });

    canvas.addEventListener('mouseleave', () => {
      if (!isDragging) hideCard(card);
    });

    // Keep card open when mouse moves into it
    card.addEventListener('mouseleave', () => hideCard(card));

    /* Touch drag */
    let lastTX, lastTY;

    canvas.addEventListener('touchstart', e => {
      e.preventDefault();
      autoRotate = false;
      lastTX = e.touches[0].clientX;
      lastTY = e.touches[0].clientY;
      hideCard(card);
    }, { passive: false });

    canvas.addEventListener('touchmove', e => {
      e.preventDefault();
      const dx = e.touches[0].clientX - lastTX;
      const dy = e.touches[0].clientY - lastTY;
      rotation[0] += dx * 0.35;
      rotation[1]  = Math.max(-80, Math.min(80, rotation[1] - dy * 0.35));
      projection.rotate(rotation);
      lastTX = e.touches[0].clientX;
      lastTY = e.touches[0].clientY;
    }, { passive: false });

    canvas.addEventListener('touchend', () => scheduleResume());

    /* Tap to show card on mobile */
    canvas.addEventListener('click', e => {
      const [mx, my] = toLogical(e);
      const hit = hitTest(mx, my);
      if (hit >= 0) showCard(hit, mx, my, card);
      else          hideCard(card);
    });

    /* Resize */
    window.addEventListener('resize', () => { setSize(); render(); });
  }

  /* ── Bootstrap ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();

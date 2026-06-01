/* ─────────────────────────────────────────────
   LOST VOYAGES — main.js
───────────────────────────────────────────── */

// ── NAV SCROLL ──
const nav = document.getElementById('nav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

// ── MOBILE MENU ──
const burger      = document.getElementById('burger');
const mobileMenu  = document.getElementById('mobileMenu');
const mobileClose = document.getElementById('mobileClose');

function openMobile()  { mobileMenu && mobileMenu.classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeMobile() { mobileMenu && mobileMenu.classList.remove('open'); document.body.style.overflow = ''; }

burger      && burger.addEventListener('click', openMobile);
mobileClose && mobileClose.addEventListener('click', closeMobile);

// Close on overlay click
mobileMenu && mobileMenu.addEventListener('click', (e) => {
  if (e.target === mobileMenu) closeMobile();
});

// ── SCROLL REVEAL ──
function revealOnScroll() {
  // Section-level reveals
  document.querySelectorAll('.reveal').forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 80) el.classList.add('visible');
  });

  // Staggered children: tour cards, steps, feats, nums
  const staggerGroups = [
    '.tours-grid',
    '.steps-grid',
    '.about-features',
    '.about-nums',
  ];

  staggerGroups.forEach(selector => {
    const group = document.querySelector(selector);
    if (!group) return;
    const groupRect = group.getBoundingClientRect();
    if (groupRect.top < window.innerHeight - 40) {
      group.querySelectorAll(':scope > *').forEach((child, i) => {
        setTimeout(() => child.classList.add('visible'), i * 80);
      });
    }
  });
}

window.addEventListener('scroll', revealOnScroll, { passive: true });
window.addEventListener('load',   revealOnScroll);
revealOnScroll();

// ── SMOOTH ANCHOR SCROLL (account for fixed nav) ──
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', (e) => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const offset = 76;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top, behavior: 'smooth' });
    closeMobile();
  });
});

// ── PROGRAM ACCORDION (rusya.html) ──
document.querySelectorAll('.program-day-head').forEach(head => {
  head.addEventListener('click', () => {
    const day = head.closest('.program-day');
    const wasOpen = day.classList.contains('open');
    // Close all
    document.querySelectorAll('.program-day').forEach(d => d.classList.remove('open'));
    // Toggle clicked
    if (!wasOpen) day.classList.add('open');
  });
});

// Auto-open first day on tour pages
const firstDay = document.querySelector('.program-day');
if (firstDay) firstDay.classList.add('open');

// ── FORM: success state ──
const forms = document.querySelectorAll('.contact-form, .tour-form');
forms.forEach(form => {
  // Netlify handles submission; show thank you if ?sent=1 in URL
  if (window.location.search.includes('sent=1')) {
    const wrap = form.closest('.contact-form-wrap, .tour-form-wrap');
    if (wrap) {
      wrap.innerHTML = `
        <div style="text-align:center;padding:48px 24px;">
          <div style="font-size:3rem;margin-bottom:16px;">✈️</div>
          <h3 style="font-family:inherit;font-size:1.2rem;color:#D4A017;margin-bottom:8px;">Formunuz Alındı!</h3>
          <p style="font-size:0.88rem;color:rgba(232,230,225,0.6);">En kısa sürede size ulaşacağız. WhatsApp'tan da yazabilirsiniz.</p>
        </div>`;
    }
  }
});

// ── ANIMATED COUNTER ──
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const suffix = el.dataset.suffix || '';
  const duration = 1600;
  const step = 16;
  const increment = target / (duration / step);
  let current = 0;

  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = Math.floor(current) + suffix;
  }, step);
}

function checkCounters() {
  document.querySelectorAll('[data-target]').forEach(el => {
    if (el.dataset.counted) return;
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 60) {
      el.dataset.counted = '1';
      animateCounter(el);
    }
  });
}

window.addEventListener('scroll', checkCounters, { passive: true });
window.addEventListener('load', checkCounters);
checkCounters();

// ── PHOTO SLIDER (otomatik akış, sürükleme yok) ──

// ── BİLDİRİ AL MODAL ──
(function() {
  const overlay  = document.getElementById('bildiriOverlay');
  const closeBtn = document.getElementById('bildiriClose');
  const turInput = document.getElementById('bildiriTurInput');
  const turAdi   = document.getElementById('bildiriTurAdi');
  if (!overlay) return;

  function openModal(tourName) {
    turInput.value = tourName || '';
    turAdi.textContent = tourName
      ? tourName + ' turu için kayıt açıldığında seni ilk biz arayalım.'
      : 'Bu tur için kayıt açıldığında seni ilk biz arayalım.';
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  // Intercept clicks on tour cards with href="#iletisim"
  document.querySelectorAll('a.tour-card[href="javascript:void(0)"]').forEach(card => {
    card.addEventListener('click', function(e) {
      e.preventDefault();
      const name = card.querySelector('.tour-name')?.textContent?.trim() || '';
      openModal(name);
    });
  });

  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
  });
})();

/* ============================================================
   BASE.JS — Shared JS for all pages
   ============================================================ */

// ── Custom Cursor ──
const cursor = document.getElementById('cursor');
const cursorRing = document.getElementById('cursorRing');
let mx = 0, my = 0, rx = 0, ry = 0;

document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });

(function animateCursor() {
  cursor.style.left = mx + 'px';
  cursor.style.top = my + 'px';
  rx += (mx - rx) * 0.12;
  ry += (my - ry) * 0.12;
  cursorRing.style.left = rx + 'px';
  cursorRing.style.top = ry + 'px';
  requestAnimationFrame(animateCursor);
})();

// ── Particles ──
const pc = document.getElementById('particles');
for (let i = 0; i < 30; i++) {
  const p = document.createElement('div');
  p.className = 'particle';
  const x = Math.random() * 100;
  const dur = 8 + Math.random() * 15;
  const del = Math.random() * 15;
  const dx = (Math.random() - 0.5) * 100;
  p.style.cssText = `left:${x}%;animation-duration:${dur}s;animation-delay:${del}s;--dx:${dx}px;
    ${Math.random() > 0.5 ? 'background:var(--accent2);' : ''}`;
  pc.appendChild(p);
}

// ── Scroll Reveal ──
const scrollObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-up').forEach(el => scrollObserver.observe(el));

// ── Toast Notifications ──
function showToast(msg, isError = false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast' + (isError ? ' error' : '');
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 4000);
}

// ── Helper: observe newly added fade-up elements ──
function observeFadeUps(container) {
  container.querySelectorAll('.fade-up').forEach(el => scrollObserver.observe(el));
}

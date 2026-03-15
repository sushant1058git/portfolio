/* ============================================================
   BASE.JS — Shared JS for all pages
   ============================================================ */

// ── Custom Cursor ──
(function initCursor() {
  const dot = document.getElementById("cursor");
  const ring = document.getElementById("cursorRing");
  if (!dot || !ring) return;

  // Half-sizes for centering — calculated once, never recalculated
  const DOT_HALF = 6; // dot  is 12px wide
  const RING_HALF = 18; // ring is 36px wide

  // Start at viewport center so cursor doesn't flash at (0,0) on load
  let mx = window.innerWidth / 2;
  let my = window.innerHeight / 2;
  let rx = mx,
    ry = my;

  // Hide until first real mouse move
  dot.style.opacity = "0";
  ring.style.opacity = "0";

  // Dot: update via transform on mousemove — zero lag, GPU composited
  document.addEventListener(
    "mousemove",
    (e) => {
      mx = e.clientX;
      my = e.clientY;
      // Reveal cursor on first move
      dot.style.opacity = "1";
      ring.style.opacity = "1";
      dot.style.transform = `translate(${mx - DOT_HALF}px, ${my - DOT_HALF}px)`;
    },
    { passive: true },
  );

  // Ring: smooth lerp follow via rAF — also GPU composited
  (function animateRing() {
    rx += (mx - rx) * 0.14;
    ry += (my - ry) * 0.14;
    ring.style.transform = `translate(${rx - RING_HALF}px, ${ry - RING_HALF}px)`;
    requestAnimationFrame(animateRing);
  })();
})();

// ── Particles ──
const pc = document.getElementById("particles");
for (let i = 0; i < 30; i++) {
  const p = document.createElement("div");
  p.className = "particle";
  const x = Math.random() * 100;
  const dur = 8 + Math.random() * 15;
  const del = Math.random() * 15;
  const dx = (Math.random() - 0.5) * 100;
  p.style.cssText = `left:${x}%;animation-duration:${dur}s;animation-delay:${del}s;--dx:${dx}px;
    ${Math.random() > 0.5 ? "background:var(--accent2);" : ""}`;
  pc.appendChild(p);
}

// ── Scroll Reveal ──
const scrollObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) e.target.classList.add("visible");
    });
  },
  { threshold: 0.1 },
);

document
  .querySelectorAll(".fade-up")
  .forEach((el) => scrollObserver.observe(el));

// ── Toast Notifications ──
function showToast(msg, isError = false) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "toast" + (isError ? " error" : "");
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 4000);
}

// ── Helper: observe newly added fade-up elements ──
function observeFadeUps(container) {
  container
    .querySelectorAll(".fade-up")
    .forEach((el) => scrollObserver.observe(el));
}

/* ============================================
   AUTH — Login modal & session management
   ============================================ */

// ---- Check auth state on load ----
async function checkAuth() {
  try {
    const res = await fetch("/api/auth/check/");
    const data = await res.json();
    if (data.authenticated) {
      setLoggedIn(data.user);
    } else {
      setLoggedOut();
    }
  } catch (e) {
    setLoggedOut();
  }
}

function setLoggedIn(user) {
  const loginBtn = document.getElementById("nav-login-btn");
  const userEl = document.getElementById("nav-user");
  const usernameEl = document.getElementById("nav-username");
  if (loginBtn) loginBtn.style.display = "none";
  if (userEl) userEl.style.display = "flex";
  if (usernameEl) usernameEl.textContent = user.username;
  window._authUser = user;
}

function setLoggedOut() {
  const loginBtn = document.getElementById("nav-login-btn");
  const userEl = document.getElementById("nav-user");
  if (loginBtn) loginBtn.style.display = "block";
  if (userEl) userEl.style.display = "none";
  window._authUser = null;
}

// ---- Modal open/close ----
function openLoginModal() {
  const modal = document.getElementById("login-modal");
  if (modal) {
    modal.classList.add("open");
    setTimeout(() => document.getElementById("login-username")?.focus(), 100);
  }
}

function closeModal() {
  const modal = document.getElementById("login-modal");
  if (modal) modal.classList.remove("open");
  const err = document.getElementById("login-error");
  if (err) err.style.display = "none";
}

function closeLoginModal(event) {
  if (event.target === document.getElementById("login-modal")) closeModal();
}

// Close on Escape
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});

// ---- Login submit ----
async function submitLogin(e) {
  e.preventDefault();
  const btn = document.getElementById("login-btn");
  const errEl = document.getElementById("login-error");
  const username = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value;

  btn.textContent = "AUTHENTICATING...";
  btn.disabled = true;
  if (errEl) errEl.style.display = "none";

  // Get CSRF token
  const csrf = getCsrf();

  try {
    const res = await fetch("/api/auth/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();

    if (res.ok && data.success) {
      setLoggedIn(data.user);
      closeModal();
      showToast("✓ Welcome back, " + data.user.username + "!");
      // Refresh page content if needed
      if (typeof onAuthChange === "function") onAuthChange(data.user);
    } else {
      if (errEl) {
        errEl.textContent = data.error || "Login failed.";
        errEl.style.display = "block";
      }
    }
  } catch (err) {
    if (errEl) {
      errEl.textContent = "Network error. Please try again.";
      errEl.style.display = "block";
    }
  } finally {
    btn.textContent = "LOGIN →";
    btn.disabled = false;
  }
}

// ---- Logout ----
async function doLogout() {
  const csrf = getCsrf();
  await fetch("/api/auth/logout/", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
  });
  setLoggedOut();
  showToast("Logged out successfully.");
  if (typeof onAuthChange === "function") onAuthChange(null);
  // Redirect home if on a protected page
  if (
    window.location.pathname.includes("/create") ||
    window.location.pathname.includes("/edit")
  ) {
    window.location.href = "/";
  }
}

// ---- CSRF helper ----
function getCsrf() {
  return (
    document.cookie
      .split(";")
      .find((c) => c.trim().startsWith("csrftoken="))
      ?.split("=")[1] || ""
  );
}

// Run on load
checkAuth();

/* ── Nav Dropdown ── */
function toggleDropdown() {
  const dd = document.getElementById("nav-labs-dropdown");
  if (!dd) return;
  const isOpen = dd.classList.toggle("open");
  const btn = dd.querySelector(".nav-dropdown-btn");
  if (btn) btn.setAttribute("aria-expanded", isOpen);
}

// Close dropdown when clicking outside
document.addEventListener("click", function (e) {
  const dd = document.getElementById("nav-labs-dropdown");
  if (dd && !dd.contains(e.target)) {
    dd.classList.remove("open");
    const btn = dd.querySelector(".nav-dropdown-btn");
    if (btn) btn.setAttribute("aria-expanded", "false");
  }
});

// Close on Escape
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    const dd = document.getElementById("nav-labs-dropdown");
    if (dd) {
      dd.classList.remove("open");
      const btn = dd.querySelector(".nav-dropdown-btn");
      if (btn) btn.setAttribute("aria-expanded", "false");
    }
  }
});

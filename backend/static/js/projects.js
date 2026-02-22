/* ============================================
   PROJECTS.JS — Projects, Timeline, Currently Working
   ============================================ */

// ── Projects grid ─────────────────────────────────────────
async function loadProjects() {
  const grid = document.getElementById("projects-grid");
  if (!grid) return;

  try {
    const res = await fetch("/api/projects/");
    const projects = await res.json();

    if (!Array.isArray(projects) || !projects.length) {
      grid.innerHTML = `
        <div style="grid-column:1/-1;text-align:center;padding:4rem;font-family:'Share Tech Mono',monospace;color:var(--text-dim)">
          NO PROJECTS ADDED YET — ADD THEM VIA ADMIN
        </div>`;
      return;
    }

    grid.innerHTML = projects
      .map(
        (p) => `
      <div class="project-card fade-up visible">
        ${
          p.cover_image
            ? `<img src="${p.cover_image}" class="project-cover" alt="${p.title}">`
            : `<div class="project-cover-placeholder">⬡</div>`
        }
        <div class="project-body">
          <div class="project-title">${p.title}</div>
          <div class="project-desc">${p.description}</div>
          ${p.outcome ? `<div class="project-outcome">→ ${p.outcome}</div>` : ""}
          <div class="project-stack">
            ${(p.tech_stack || []).map((t) => `<span class="stack-tag">${t}</span>`).join("")}
          </div>
        </div>
        <div class="project-footer">
          <div class="project-links">
            ${p.demo_url ? `<a href="${p.demo_url}"   target="_blank" class="project-link demo">⬡ LIVE DEMO</a>` : ""}
            ${p.github_url ? `<a href="${p.github_url}" target="_blank" class="project-link github">⌥ GITHUB</a>` : ""}
          </div>
          ${p.github_stars ? `<div class="project-stars">★ ${p.github_stars}</div>` : ""}
        </div>
      </div>
    `,
      )
      .join("");
  } catch (e) {
    console.error("loadProjects error:", e);
  }
}

// ── Interactive Timeline ───────────────────────────────────
async function loadTimeline() {
  const track = document.getElementById("timeline-track");
  if (!track) return;

  try {
    const res = await fetch("/api/experience/");
    const exps = await res.json();

    if (!exps.length) {
      track.innerHTML =
        '<p style="color:var(--text-dim);padding-left:3rem">No experience found.</p>';
      return;
    }

    track.innerHTML = exps
      .map(
        (e, i) => `
      <div class="timeline-item ${i % 2 !== 0 ? "alt" : ""}" id="tl-${i}">
        <div class="timeline-dot" onclick="toggleTimeline(${i})"></div>
        <div class="timeline-header" onclick="toggleTimeline(${i})">
          <div class="tl-top">
            <div>
              <div class="tl-role">${e.role}</div>
              <div class="tl-company">${e.company} · ${e.location}</div>
              <div class="tl-period">${e.period}</div>
            </div>
            <span class="tl-chevron">▾</span>
          </div>
        </div>
        <div class="timeline-body">
          <div class="timeline-body-inner">
            <ul class="tl-points">
              ${e.points.map((p) => `<li>${p.text}</li>`).join("")}
            </ul>
          </div>
        </div>
      </div>
    `,
      )
      .join("");

    // Open first by default
    toggleTimeline(0);
  } catch (e) {
    console.error("loadTimeline error:", e);
  }
}

function toggleTimeline(i) {
  const item = document.getElementById("tl-" + i);
  if (!item) return;
  const isOpen = item.classList.contains("open");
  document
    .querySelectorAll(".timeline-item.open")
    .forEach((el) => el.classList.remove("open"));
  if (!isOpen) item.classList.add("open");
}

// ── Currently Working — ALL active items ──────────────────
let cwItems = [];
let cwIndex = 0;
let cwInterval = null;

async function loadCurrentlyWorking() {
  const section = document.getElementById("currently-wrap");
  if (!section) return;

  try {
    const res = await fetch("/api/currently-working/");
    const data = await res.json();

    // Handle both array (new) and single object (old) response
    cwItems = Array.isArray(data) ? data : data && data.title ? [data] : [];

    if (!cwItems.length) {
      section.style.display = "none";
      return;
    }

    section.style.display = "block";

    // Render nav dots if more than 1 item
    const dotsEl = document.getElementById("cw-dots");
    if (dotsEl) {
      if (cwItems.length > 1) {
        dotsEl.innerHTML = cwItems
          .map(
            (_, i) =>
              `<button class="cw-dot ${i === 0 ? "active" : ""}" onclick="showCWItem(${i})" title="Item ${i + 1}"></button>`,
          )
          .join("");
        dotsEl.style.display = "flex";
      } else {
        dotsEl.style.display = "none";
      }
    }

    // Show counter
    const counterEl = document.getElementById("cw-counter");
    if (counterEl) {
      counterEl.style.display = cwItems.length > 1 ? "block" : "none";
    }

    // Show first item
    showCWItem(0);

    // Auto-cycle if multiple items
    if (cwItems.length > 1) {
      cwInterval = setInterval(() => {
        cwIndex = (cwIndex + 1) % cwItems.length;
        showCWItem(cwIndex);
      }, 5000);
    }
  } catch (e) {
    console.error("loadCurrentlyWorking error:", e);
    const section = document.getElementById("currently-wrap");
    if (section) section.style.display = "none";
  }
}

function showCWItem(i) {
  if (!cwItems.length) return;
  cwIndex = i;
  const item = cwItems[i];

  // Type badge
  const typeEl = document.getElementById("currently-type");
  if (typeEl) {
    typeEl.textContent = (item.type || "building").toUpperCase();
    // Color by type
    const colors = {
      building: "var(--accent)",
      learning: "var(--accent2)",
      contributing: "#f5c518",
      reading: "var(--accent3)",
    };
    const c = colors[item.type] || "var(--accent)";
    typeEl.style.borderColor = c;
    typeEl.style.color = c;
  }

  // Title
  const titleEl = document.getElementById("currently-title");
  if (titleEl) titleEl.textContent = item.title || "";

  // Description
  const descEl = document.getElementById("currently-desc");
  if (descEl) {
    descEl.textContent = item.description || "";
    descEl.style.display = item.description ? "block" : "none";
  }

  // Tags
  const tagsEl = document.getElementById("currently-tags");
  if (tagsEl) {
    tagsEl.innerHTML = (item.tech_tags || [])
      .map((t) => `<span class="currently-tag">${t}</span>`)
      .join("");
  }

  // Progress bar
  const fill = document.getElementById("progress-fill");
  const pct = document.getElementById("progress-pct");
  const progressWrap = document.getElementById("progress-wrap");
  const prog = item.progress || 0;
  if (fill) {
    fill.style.width = "0%";
    setTimeout(() => (fill.style.width = prog + "%"), 50);
  }
  if (pct) pct.textContent = prog + "%";
  if (progressWrap) progressWrap.style.display = prog > 0 ? "block" : "none";

  // Link
  const card = document.getElementById("currently-card");
  if (card) {
    if (item.link) {
      card.style.cursor = "pointer";
      card.onclick = () => window.open(item.link, "_blank");
    } else {
      card.style.cursor = "default";
      card.onclick = null;
    }
  }

  // Counter
  const counterEl = document.getElementById("cw-counter");
  if (counterEl) counterEl.textContent = i + 1 + " / " + cwItems.length;

  // Dots active state
  document.querySelectorAll(".cw-dot").forEach((dot, idx) => {
    dot.classList.toggle("active", idx === i);
  });

  // Animate in
  const content = document.getElementById("currently-content");
  if (content) {
    content.style.opacity = "0";
    content.style.transform = "translateY(6px)";
    setTimeout(() => {
      content.style.opacity = "1";
      content.style.transform = "translateY(0)";
    }, 50);
  }
}

// ── Init ──────────────────────────────────────────────────
loadProjects();
loadTimeline();
loadCurrentlyWorking();

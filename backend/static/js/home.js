/* ============================================
   HOME.JS — Portfolio homepage logic
   ============================================ */

async function loadPortfolio() {
  try {
    const [profileRes, skillsRes, expRes, blogRes] = await Promise.all([
      fetch("/api/profile/"),
      fetch("/api/skills/"),
      fetch("/api/experience/"),
      fetch("/api/blogs/featured/"),
    ]);
    const profile = await profileRes.json();
    const skills = await skillsRes.json();
    const experiences = await expRes.json();
    const blogs = await blogRes.json();

    renderProfile(profile);
    renderSkills(skills);
    renderExperience(experiences);
    renderBlog(blogs);
  } catch (e) {
    console.error("Portfolio API error:", e);
  }
}

// ── Profile ───────────────────────────────────────────────
function renderProfile(p) {
  if (!p || p.error) return;

  // Hero text
  const subtitle = document.getElementById("hero-subtitle");
  const desc = document.getElementById("hero-desc");
  if (subtitle)
    subtitle.textContent = "> " + (p.role || "Software Engineer") + "_";
  if (desc && p.bio) desc.textContent = p.bio.substring(0, 200) + "...";

  // Stats
  const statExp = document.getElementById("stat-exp");
  const statDep = document.getElementById("stat-deploy");
  if (statExp) statExp.textContent = (p.years_experience || 5) + "+";
  if (statDep) statDep.textContent = p.deploy_improvement || "30%";

  // Terminal
  const tEmail = document.getElementById("t-email");
  const tGithub = document.getElementById("t-github");
  const tPhone = document.getElementById("t-phone");
  if (tEmail && p.email) tEmail.textContent = '"' + p.email + '"';
  if (tGithub && p.github)
    tGithub.textContent = '"' + p.github.replace("https://", "") + '"';
  if (tPhone && p.phone) tPhone.textContent = '"' + p.phone + '"';

  // About bio
  const bio = document.getElementById("about-bio");
  if (bio && p.bio) bio.textContent = p.bio;

  // Avatar
  if (p.avatar_url) {
    const avatarWrap = document.getElementById("hero-avatar-wrap");
    if (avatarWrap) {
      avatarWrap.innerHTML = `<img src="${p.avatar_url}" alt="${p.name}" class="hero-avatar">`;
      avatarWrap.style.display = "block";
    }
    // Also update terminal avatar
    const termAvatar = document.getElementById("t-avatar");
    if (termAvatar) {
      termAvatar.innerHTML = `<img src="${p.avatar_url}" alt="${p.name}" class="terminal-avatar">`;
    }
  }

  // Resume download button — always visible, shows toast if no file uploaded
  const resumeBtn = document.getElementById("resume-btn");
  if (resumeBtn) {
    if (p.resume_url) {
      resumeBtn.href = p.resume_url;
      resumeBtn.setAttribute("download", "Sushant_Sinha_Resume.pdf");

      resumeBtn.onclick = null;
    } else {
      resumeBtn.href = "#";
      resumeBtn.onclick = (e) => {
        e.preventDefault();
        showToast("Resume not uploaded yet. Check back soon!", false);
      };
    }
  }

  // Status badge
  const badge = document.getElementById("status-badge");
  if (badge && !p.is_available) badge.style.display = "none";
}

// ── Skills ────────────────────────────────────────────────
function renderSkills(skills) {
  const grid = document.getElementById("skills-grid");
  if (!grid) return;
  if (!skills.length) {
    grid.innerHTML = '<p style="color:var(--text-dim)">No skills found.</p>';
    return;
  }
  grid.innerHTML = skills
    .map(
      (cat) => `
    <div class="skill-card fade-up visible">
      <div class="skill-card-icon">${cat.icon}</div>
      <div class="skill-card-title">${cat.name.toUpperCase()}</div>
      <div class="skill-tags">
        ${cat.skills.map((s) => `<span class="skill-tag">${s.name}</span>`).join("")}
      </div>
    </div>
  `,
    )
    .join("");
}

// ── Experience ────────────────────────────────────────────
function renderExperience(exps) {
  const tl = document.getElementById("exp-timeline");
  if (!tl) return;
  if (!exps.length) {
    tl.innerHTML = '<p style="color:var(--text-dim)">No experience found.</p>';
    return;
  }
  tl.innerHTML = exps
    .map(
      (e, i) => `
    <div class="exp-item fade-up visible">
      <div class="exp-dot" style="${i !== 0 ? "background:var(--accent2);box-shadow:var(--glow2)" : ""}"></div>
      <div class="exp-period">${e.period}</div>
      <div class="exp-role">${e.role}</div>
      <div class="exp-company">${e.company} · ${e.location}</div>
      <ul class="exp-points">
        ${e.points.map((p) => `<li>${p.text}</li>`).join("")}
      </ul>
    </div>
  `,
    )
    .join("");
}

// ── Blog (featured) ───────────────────────────────────────
function renderBlog(posts) {
  const grid = document.getElementById("blog-grid");
  if (!grid) return;
  if (!posts.length) {
    grid.innerHTML =
      "<p style=\"color:var(--text-dim);font-family:'Share Tech Mono',monospace\">No posts yet.</p>";
    return;
  }
  grid.innerHTML = posts
    .map(
      (p) => `
    <a href="/blog/${p.slug}/" class="blog-card fade-up visible">
      <div class="blog-cat">${p.category ? p.category.name.toUpperCase() : "GENERAL"}</div>
      <div class="blog-title">${p.title}</div>
      <div class="blog-excerpt">${p.excerpt}</div>
      <div class="blog-meta">
        <div class="blog-date">${p.published_date} · ${p.read_time} MIN READ</div>
        <span class="blog-read">READ →</span>
      </div>
    </a>
  `,
    )
    .join("");
}

// ── Contact Form ──────────────────────────────────────────
const contactForm = document.getElementById("contact-form");
if (contactForm) {
  contactForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const btn = document.getElementById("submit-btn");
    btn.textContent = "SENDING...";
    btn.disabled = true;
    const data = Object.fromEntries(new FormData(this).entries());
    try {
      const res = await fetch("/api/contact/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": data.csrfmiddlewaretoken,
        },
        body: JSON.stringify({
          name: data.name,
          email: data.email,
          subject: data.subject,
          message: data.message,
        }),
      });
      const json = await res.json();
      if (res.ok) {
        showToast("✓ Message sent! I'll reply soon.");
        this.reset();
      } else showToast(Object.values(json).flat().join(". "), true);
    } catch (err) {
      showToast("Network error.", true);
    } finally {
      btn.textContent = "SEND MESSAGE →";
      btn.disabled = false;
    }
  });
}

// ── Refresh blog section after login ─────────────────────
function onAuthChange(user) {
  // Reload blog to show "Write Post" button state (already in nav)
}

loadPortfolio();

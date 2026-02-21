/* ============================================================
   HOME.JS — Portfolio homepage API loading & rendering
   ============================================================ */

// ── Load all portfolio data ──
async function loadPortfolio() {
  try {
    const [profileRes, skillsRes, expRes, blogRes] = await Promise.all([
      fetch('/api/profile/'),
      fetch('/api/skills/'),
      fetch('/api/experience/'),
      fetch('/api/blogs/featured/'),
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
    console.error('API load error:', e);
  }
}

// ── Render Profile ──
function renderProfile(p) {
  if (!p || p.error) return;

  const subtitle = document.getElementById('hero-subtitle');
  const desc = document.getElementById('hero-desc');
  const bio = document.getElementById('about-bio');
  const statExp = document.getElementById('stat-exp');
  const statDeploy = document.getElementById('stat-deploy');
  const tEmail = document.getElementById('t-email');
  const tGithub = document.getElementById('t-github');
  const tPhone = document.getElementById('t-phone');
  const statusBadge = document.getElementById('status-badge');

  if (subtitle) subtitle.textContent = '> ' + p.role + '_';
  if (desc) desc.textContent = p.bio ? p.bio.substring(0, 200) + '...' : '';
  if (bio) bio.textContent = p.bio || '';
  if (statExp) statExp.textContent = p.years_experience + '+';
  if (statDeploy) statDeploy.textContent = p.deploy_improvement;
  if (tEmail) tEmail.textContent = '"' + p.email + '"';
  if (tGithub && p.github) tGithub.textContent = '"' + p.github.replace('https://', '') + '"';
  if (tPhone && p.phone) tPhone.textContent = '"' + p.phone + '"';
  if (statusBadge && !p.is_available) statusBadge.style.display = 'none';
}

// ── Render Skills ──
function renderSkills(skills) {
  const grid = document.getElementById('skills-grid');
  if (!grid) return;

  if (!skills.length) {
    grid.innerHTML = '<p style="color:var(--text-dim);font-family:\'Share Tech Mono\',monospace">No skills found.</p>';
    return;
  }

  grid.innerHTML = skills.map(cat => `
    <div class="skill-card fade-up visible">
      <div class="skill-card-icon">${cat.icon}</div>
      <div class="skill-card-title">${cat.name.toUpperCase()}</div>
      <div class="skill-tags">
        ${cat.skills.map(s => `<span class="skill-tag">${s.name}</span>`).join('')}
      </div>
    </div>
  `).join('');
}

// ── Render Experience ──
function renderExperience(exps) {
  const tl = document.getElementById('exp-timeline');
  if (!tl) return;

  if (!exps.length) {
    tl.innerHTML = '<p style="color:var(--text-dim);font-family:\'Share Tech Mono\',monospace">No experience found.</p>';
    return;
  }

  tl.innerHTML = exps.map((e, i) => `
    <div class="exp-item fade-up visible">
      <div class="exp-dot" style="${i === 0 ? '' : 'background:var(--accent2);box-shadow:var(--glow2)'}"></div>
      <div class="exp-period">${e.period}</div>
      <div class="exp-role">${e.role}</div>
      <div class="exp-company">${e.company} · ${e.location}</div>
      <ul class="exp-points">
        ${e.points.map(p => `<li>${p.text}</li>`).join('')}
      </ul>
    </div>
  `).join('');
}

// ── Render Blog ──
function renderBlog(posts) {
  const grid = document.getElementById('blog-grid');
  if (!grid) return;

  if (!posts.length) {
    grid.innerHTML = '<p style="color:var(--text-dim);font-family:\'Share Tech Mono\',monospace">No posts published yet.</p>';
    return;
  }

  grid.innerHTML = posts.map(p => `
    <a href="/blog/${p.slug}/" class="blog-card fade-up visible">
      <div class="blog-cat">${p.category ? p.category.name.toUpperCase() : 'GENERAL'}</div>
      <div class="blog-title">${p.title}</div>
      <div class="blog-excerpt">${p.excerpt}</div>
      <div class="blog-meta">
        <div class="blog-date">${p.published_date} · ${p.read_time} MIN READ</div>
        <span class="blog-read">READ →</span>
      </div>
    </a>
  `).join('');
}

// ── Contact Form ──
const contactForm = document.getElementById('contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const btn = document.getElementById('submit-btn');
    btn.textContent = 'SENDING...';
    btn.disabled = true;

    const data = Object.fromEntries(new FormData(this).entries());

    try {
      const res = await fetch('/api/contact/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': data.csrfmiddlewaretoken,
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
      } else {
        const errs = Object.values(json).flat().join('. ');
        showToast(errs, true);
      }
    } catch (err) {
      showToast('Network error. Please try again.', true);
    } finally {
      btn.textContent = 'SEND MESSAGE →';
      btn.disabled = false;
    }
  });
}

// ── Init ──
loadPortfolio();

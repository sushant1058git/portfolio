/* ============================================================
   BLOG_DETAIL.JS — Blog post detail page
   ============================================================ */

const postSlug = window.location.pathname.split('/').filter(Boolean).pop();

// ── Load Post ──
async function loadPost() {
  try {
    const res = await fetch('/api/blogs/' + postSlug + '/');
    if (!res.ok) {
      document.getElementById('post-hero').innerHTML =
        '<div style="padding:10rem 4rem;color:var(--accent3);font-family:\'Share Tech Mono\',monospace;position:relative;z-index:1">POST NOT FOUND</div>';
      return;
    }
    const post = await res.json();
    renderPost(post);
    loadRelated(post.category?.slug);
  } catch (e) {
    console.error('Failed to load post:', e);
  }
}

// ── Render Post ──
function renderPost(p) {
  const catColor = p.category?.color || 'var(--accent2)';

  // Hero
  document.getElementById('post-hero').innerHTML = `
    <div class="post-hero-bg"></div>
    <div style="position:relative;z-index:1;max-width:900px">
      <div class="post-breadcrumb">
        <a href="/">HOME</a> / <a href="/blog/">BLOG</a> / ${p.category?.name.toUpperCase() || 'POST'}
      </div>
      <div class="post-cat" style="color:${catColor}">
        <span style="display:inline-block;width:20px;height:1px;background:${catColor}"></span>
        ${p.category?.name.toUpperCase() || 'GENERAL'}
      </div>
      <h1 class="post-title">${p.title}</h1>
      <div class="post-meta-row">
        <div class="post-meta-item">📅 <span>${p.published_date}</span></div>
        <div class="post-meta-item">⏱ <span>${p.read_time} MIN READ</span></div>
        <div class="post-meta-item">👁 <span>${p.views} VIEWS</span></div>
        <div class="post-meta-item">💬 <span>${p.comment_count} COMMENTS</span></div>
      </div>
    </div>
  `;

  document.title = p.title + ' | Sushant Sinha';

  // Content
  document.getElementById('post-content').innerHTML = p.content_html;

  // Build TOC from headings
  const headings = document.querySelectorAll('#post-content h2, #post-content h3');
  let tocHtml = '';
  headings.forEach((h, i) => {
    const id = 'heading-' + i;
    h.id = id;
    const isH3 = h.tagName === 'H3';
    tocHtml += `<a href="#${id}" class="toc-link" style="${isH3 ? 'padding-left:1.5rem;font-size:.72rem' : ''}">${h.textContent}</a>`;
  });

  if (tocHtml) {
    document.getElementById('post-sidebar').innerHTML = `
      <div class="sidebar-card">
        <div class="sidebar-title">TABLE OF CONTENTS</div>
        ${tocHtml}
      </div>
      <div class="sidebar-card">
        <div class="sidebar-title">RELATED POSTS</div>
        <div id="related-posts"><span style="font-family:'Share Tech Mono',monospace;font-size:.8rem;color:var(--text-dim)">Loading...</span></div>
      </div>
    `;
  }

  // Comments
  const commentsSection = document.getElementById('comments-section');
  if (commentsSection) commentsSection.style.display = 'block';

  const list = document.getElementById('comments-list');
  if (list) {
    if (p.comments && p.comments.length) {
      list.innerHTML = p.comments.map(c => `
        <div class="comment-card">
          <div class="comment-author">${c.name}</div>
          <div class="comment-date">${new Date(c.created_at).toLocaleDateString('en-IN', { year:'numeric', month:'short', day:'numeric' })}</div>
          <div class="comment-text">${c.content}</div>
        </div>
      `).join('');
    } else {
      list.innerHTML = '<p style="font-family:\'Share Tech Mono\',monospace;font-size:.8rem;color:var(--text-dim);margin-bottom:1.5rem">NO COMMENTS YET. BE THE FIRST!</p>';
    }
  }

  document.getElementById('post-layout').style.display = 'grid';
  setupCommentForm();
}

// ── Load Related Posts ──
async function loadRelated(catSlug) {
  if (!catSlug) return;
  const el = document.getElementById('related-posts');
  if (!el) return;

  try {
    const res = await fetch(`/api/blogs/?category=${catSlug}&page_size=4`);
    const data = await res.json();
    const filtered = (data.results || []).filter(p => p.slug !== postSlug).slice(0, 3);

    if (!filtered.length) {
      el.innerHTML = '<p style="font-size:.8rem;color:var(--text-dim);font-family:\'Share Tech Mono\'">No related posts.</p>';
      return;
    }

    el.innerHTML = filtered.map(p => `
      <a href="/blog/${p.slug}/" class="related-post">
        <div class="rel-title">${p.title}</div>
        <div class="rel-meta">${p.published_date} · ${p.read_time} MIN</div>
      </a>
    `).join('');
  } catch (e) {
    el.innerHTML = '';
  }
}

// ── Comment Form ──
function setupCommentForm() {
  const form = document.getElementById('comment-form');
  if (!form) return;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const btn = this.querySelector('button[type="submit"]');
    btn.textContent = 'SUBMITTING...';
    btn.disabled = true;

    const data = Object.fromEntries(new FormData(this));
    const csrf = document.cookie.split(';')
      .find(c => c.trim().startsWith('csrftoken='))?.split('=')[1] || '';

    try {
      const res = await fetch('/api/blogs/' + postSlug + '/comments/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
        body: JSON.stringify({ name: data.name, email: data.email, content: data.content }),
      });

      const json = await res.json();
      if (res.ok) {
        showToast('✓ Comment submitted! Awaiting approval.');
        this.reset();
      } else {
        showToast(Object.values(json).flat().join('. '), true);
      }
    } catch (err) {
      showToast('Network error. Please try again.', true);
    } finally {
      btn.textContent = 'POST COMMENT →';
      btn.disabled = false;
    }
  });
}

// ── Init ──
loadPost();

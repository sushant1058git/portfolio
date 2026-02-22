/* ============================================
   BLOG-DETAIL.JS — Single post page logic
   ============================================ */

const postSlug = window.location.pathname.split("/").filter(Boolean).pop();

// ---- Load and render the post ----
async function loadPost() {
  const res = await fetch("/api/blogs/" + postSlug + "/");

  if (!res.ok) {
    const hero = document.getElementById("post-hero");
    if (hero)
      hero.innerHTML = `
      <div style="padding:10rem 4rem;color:var(--accent3);font-family:'Share Tech Mono',monospace;font-size:1.2rem">
        404 — POST NOT FOUND
      </div>`;
    return;
  }

  const post = await res.json();
  renderPost(post);
  loadRelated(post.category?.slug);
}

// ---- Render post hero + content ----
function renderPost(p) {
  const catColor = p.category?.color || "var(--accent2)";
  const heroBg = p.cover_image
    ? `style="background-image:url('${p.cover_image}');background-size:cover;background-position:center;"`
    : "";

  // Hero
  const hero = document.getElementById("post-hero");
  if (hero) {
    hero.innerHTML = `
      <div class="post-hero-bg" ${heroBg}></div>
      <div style="position:relative;z-index:1;max-width:900px">
        <div class="post-breadcrumb">
          <a href="/">HOME</a> /
          <a href="/blog/">BLOG</a> /
          ${p.category?.name.toUpperCase() || "POST"}
        </div>
        <div class="post-cat" style="color:${catColor}">
          <span style="display:inline-block;width:20px;height:1px;background:${catColor}"></span>
          ${p.category?.name.toUpperCase() || "GENERAL"}
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
  }

  // Page title
  document.title = p.title + " | Sushant Sinha";

  // Content
  const contentEl = document.getElementById("post-content");
  if (contentEl) contentEl.innerHTML = p.content_html;

  // Build TOC from headings
  const headings = document.querySelectorAll(
    "#post-content h2, #post-content h3",
  );
  const sidebar = document.getElementById("post-sidebar");

  if (sidebar && headings.length) {
    let tocHtml = "";
    headings.forEach((h, i) => {
      const id = "heading-" + i;
      h.id = id;
      const indent =
        h.tagName === "H3" ? "padding-left:1.5rem;font-size:.72rem" : "";
      tocHtml += `<a href="#${id}" class="toc-link" style="${indent}">${h.textContent}</a>`;
    });

    sidebar.innerHTML = `
      <div class="sidebar-card">
        <div class="sidebar-title">TABLE OF CONTENTS</div>
        ${tocHtml}
      </div>
      <div class="sidebar-card">
        <div class="sidebar-title">RELATED POSTS</div>
        <div id="related-posts"><span style="color:var(--text-dim);font-size:.8rem;font-family:'Share Tech Mono',monospace">Loading...</span></div>
      </div>
    `;
  }

  // Show post layout
  const layout = document.getElementById("post-layout");
  if (layout) layout.style.display = "grid";

  // Comments
  renderComments(p.comments);

  // Show comments section
  const commentsSection = document.getElementById("comments-section");
  if (commentsSection) commentsSection.style.display = "block";

  // Comment form
  initCommentForm();
}

// ---- Render comments list ----
function renderComments(comments) {
  const list = document.getElementById("comments-list");
  if (!list) return;

  if (!comments || !comments.length) {
    list.innerHTML = `<p style="font-family:'Share Tech Mono',monospace;font-size:.8rem;color:var(--text-dim);margin-bottom:1.5rem">
      NO COMMENTS YET. BE THE FIRST!
    </p>`;
    return;
  }

  list.innerHTML = comments
    .map(
      (c) => `
    <div class="comment-card">
      <div class="comment-author">${c.name}</div>
      <div class="comment-date">${new Date(c.created_at).toLocaleDateString("en-IN", { year: "numeric", month: "short", day: "numeric" })}</div>
      <div class="comment-text">${c.content}</div>
    </div>
  `,
    )
    .join("");
}

// ---- Load related posts ----
async function loadRelated(catSlug) {
  const el = document.getElementById("related-posts");
  if (!el || !catSlug) return;

  const res = await fetch(`/api/blogs/?category=${catSlug}&page_size=4`);
  const data = await res.json();
  const posts = (data.results || [])
    .filter((p) => p.slug !== postSlug)
    .slice(0, 3);

  if (!posts.length) {
    el.innerHTML =
      "<p style=\"font-size:.8rem;color:var(--text-dim);font-family:'Share Tech Mono'\">No related posts.</p>";
    return;
  }

  el.innerHTML = posts
    .map(
      (p) => `
    <a href="/blog/${p.slug}/" class="related-post">
      <div class="rel-title">${p.title}</div>
      <div class="rel-meta">${p.published_date} · ${p.read_time} MIN</div>
    </a>
  `,
    )
    .join("");
}

// ---- Comment form submission ----
function initCommentForm() {
  const form = document.getElementById("comment-form");
  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const btn = this.querySelector('button[type="submit"]');
    btn.textContent = "SUBMITTING...";
    btn.disabled = true;

    const data = Object.fromEntries(new FormData(this));

    // Get CSRF token from cookie
    const csrf =
      document.cookie
        .split(";")
        .find((c) => c.trim().startsWith("csrftoken="))
        ?.split("=")[1] || "";

    try {
      const res = await fetch("/api/blogs/" + postSlug + "/comments/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf,
        },
        body: JSON.stringify({
          name: data.name,
          email: data.email,
          content: data.content,
        }),
      });

      const json = await res.json();
      if (res.ok) {
        showToast("✓ Comment submitted! Awaiting approval.");
        this.reset();
      } else {
        showToast(Object.values(json).flat().join(". "), true);
      }
    } catch (err) {
      showToast("Network error. Please try again.", true);
    } finally {
      btn.textContent = "POST COMMENT →";
      btn.disabled = false;
    }
  });
}

// ---- Init ----
loadPost();

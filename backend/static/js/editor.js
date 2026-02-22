/* ============================================
   EDITOR.JS — Blog post rich text editor
   ============================================ */

let editingSlug = null;
let isInitialized = false;

// ── Wait for DOM + auth, then init ───────────────────────
window.addEventListener("load", async () => {
  // Show loading state — don't redirect, just verify
  const authRes = await fetch("/api/auth/check/");
  const authData = await authRes.json();

  const lockScreen = document.getElementById("editor-lock");
  const editorBody = document.getElementById("editor-body");

  if (!authData.authenticated) {
    // Show lock screen instead of redirect
    if (lockScreen) lockScreen.style.display = "flex";
    if (editorBody) editorBody.style.display = "none";
    return;
  }

  // Show editor
  if (lockScreen) lockScreen.style.display = "none";
  if (editorBody) editorBody.style.display = "block";

  if (!isInitialized) {
    isInitialized = true;
    await initEditor();
  }
});

// ── Core init ─────────────────────────────────────────────
async function initEditor() {
  await loadCategories();

  // Edit mode?
  const params = new URLSearchParams(window.location.search);
  const slug = params.get("edit");
  if (slug) {
    editingSlug = slug;
    await loadPostForEdit(slug);
    document.getElementById("editor-heading").textContent = "EDIT POST";
  }

  initToolbar();
  initWordCount();
  initCoverImage();
  await loadMyPosts();
}

// ── Load categories ───────────────────────────────────────
async function loadCategories() {
  try {
    const res = await fetch("/api/categories/");
    const cats = await res.json();
    const sel = document.getElementById("post-category");
    if (!sel) return;
    cats.forEach((c) => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.name;
      sel.appendChild(opt);
    });
  } catch (e) {
    console.error("Failed to load categories", e);
  }
}

// ── Load post for editing ─────────────────────────────────
async function loadPostForEdit(slug) {
  const res = await fetch("/api/blogs/" + slug + "/");
  if (!res.ok) {
    showToast("Post not found.", true);
    return;
  }
  const post = await res.json();

  setValue("post-title", post.title);
  setValue("post-excerpt", post.excerpt);
  setValue("post-read-time", post.read_time);
  setValue("post-status", post.status);

  const featured = document.getElementById("post-featured");
  if (featured) featured.checked = post.is_featured;

  // Set rich editor content
  const editor = document.getElementById("rich-editor");
  if (editor) editor.innerHTML = post.content_html || "";

  // Set category after options load
  if (post.category) {
    setTimeout(() => setValue("post-category", post.category.id), 200);
  }

  // Breadcrumb
  const bc = document.getElementById("editor-breadcrumb-post");
  if (bc) bc.textContent = post.title;

  // Cover preview
  if (post.cover_image) showCoverPreview(post.cover_image);
}

function setValue(id, val) {
  const el = document.getElementById(id);
  if (el && val !== undefined && val !== null) el.value = val;
}

// ── Rich Text Toolbar ─────────────────────────────────────
function initToolbar() {
  const editor = document.getElementById("rich-editor");
  if (!editor) return;

  // Prevent toolbar clicks from losing editor focus
  document.querySelectorAll(".toolbar-btn").forEach((btn) => {
    btn.addEventListener("mousedown", (e) => e.preventDefault());
    btn.addEventListener("click", () => {
      const cmd = btn.dataset.cmd;
      if (cmd) execCmd(cmd, btn.dataset.val || null);
    });
  });

  // Heading select
  const headingSel = document.getElementById("heading-select");
  if (headingSel) {
    headingSel.addEventListener("mousedown", (e) => e.preventDefault());
    headingSel.addEventListener("change", function () {
      document.execCommand("formatBlock", false, this.value);
      this.value = "p";
      editor.focus();
    });
  }

  // Update active states on selection change
  editor.addEventListener("keyup", updateToolbarState);
  editor.addEventListener("mouseup", updateToolbarState);

  // Ensure editor has focus styles
  editor.focus();
}

function execCmd(cmd, val) {
  document.execCommand(cmd, false, val);
  document.getElementById("rich-editor")?.focus();
  updateToolbarState();
}

function updateToolbarState() {
  [
    "bold",
    "italic",
    "underline",
    "strikeThrough",
    "insertUnorderedList",
    "insertOrderedList",
  ].forEach((cmd) => {
    const btn = document.querySelector(`[data-cmd="${cmd}"]`);
    if (btn) btn.classList.toggle("active", document.queryCommandState(cmd));
  });
}

// ── Special inserts ───────────────────────────────────────
function insertCodeBlock() {
  const editor = document.getElementById("rich-editor");
  if (!editor) return;
  const pre = document.createElement("pre");
  pre.setAttribute("contenteditable", "true");
  pre.textContent = "// Your code here";
  const p = document.createElement("p");
  p.innerHTML = "<br>";
  editor.appendChild(pre);
  editor.appendChild(p);
  // Place cursor in code block
  const range = document.createRange();
  range.selectNodeContents(pre);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  editor.focus();
}

function insertLink() {
  const url = prompt("Enter URL (e.g. https://example.com):");
  if (url) execCmd("createLink", url);
}

function insertBlockquote() {
  execCmd("formatBlock", "blockquote");
}

// ── Word count ────────────────────────────────────────────
function initWordCount() {
  const editor = document.getElementById("rich-editor");
  const counter = document.getElementById("word-count");
  if (!editor || !counter) return;

  const update = () => {
    const text = editor.innerText || "";
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const mins = Math.max(1, Math.ceil(words / 200));
    counter.textContent = words + " WORDS · ~" + mins + " MIN READ";
    const rt = document.getElementById("post-read-time");
    if (rt) rt.value = mins;
  };

  editor.addEventListener("input", update);
  update();
}

// ── Cover image ───────────────────────────────────────────
function initCoverImage() {
  const input = document.getElementById("cover-image-input");
  if (!input) return;
  input.addEventListener("change", function () {
    if (this.files[0]) showCoverPreview(URL.createObjectURL(this.files[0]));
  });
}

function showCoverPreview(url) {
  const preview = document.getElementById("cover-preview");
  if (!preview) return;
  preview.innerHTML = `
    <img src="${url}" alt="Cover preview" style="width:100%;height:180px;object-fit:cover;border:1px solid var(--border);display:block">
    <button onclick="removeCover()" style="position:absolute;top:.5rem;right:.5rem;background:rgba(255,45,107,.85);border:none;color:#fff;width:28px;height:28px;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center">✕</button>
  `;
  preview.style.position = "relative";
}

function removeCover() {
  const preview = document.getElementById("cover-preview");
  const input = document.getElementById("cover-image-input");
  if (preview) preview.innerHTML = "";
  if (input) input.value = "";
}

// ── Save post ─────────────────────────────────────────────
async function savePost(postStatus) {
  const title = document.getElementById("post-title")?.value.trim();
  const editor = document.getElementById("rich-editor");
  const content = editor?.innerHTML.trim();
  const excerpt = document.getElementById("post-excerpt")?.value.trim();
  const catId = document.getElementById("post-category")?.value;
  const readTime = document.getElementById("post-read-time")?.value || 5;
  const featured = document.getElementById("post-featured")?.checked;

  if (!title) {
    showToast("⚠ Title is required.", true);
    return;
  }
  if (!content || content === "<br>" || content === "") {
    showToast("⚠ Content cannot be empty.", true);
    return;
  }

  const btnId = postStatus === "published" ? "btn-publish" : "btn-draft";
  const btn = document.getElementById(btnId);
  const origText = btn?.textContent;
  if (btn) {
    btn.textContent = "SAVING...";
    btn.disabled = true;
  }

  const formData = new FormData();
  formData.append("title", title);
  formData.append("content", content);
  formData.append("excerpt", excerpt || editor.innerText.substring(0, 200));
  formData.append("status", postStatus);
  formData.append("read_time", readTime);
  formData.append("is_featured", featured ? "true" : "false");
  if (catId) formData.append("category", catId);

  const coverInput = document.getElementById("cover-image-input");
  if (coverInput?.files[0]) formData.append("cover_image", coverInput.files[0]);

  const csrf = getCsrf();

  try {
    const url = editingSlug
      ? "/api/blogs/" + editingSlug + "/update/"
      : "/api/blogs/create/";
    const method = editingSlug ? "PUT" : "POST";

    const res = await fetch(url, {
      method,
      headers: { "X-CSRFToken": csrf },
      body: formData,
    });
    const data = await res.json();

    if (res.ok) {
      const label = postStatus === "published" ? "published" : "saved as draft";
      showToast("✓ Post " + label + "!");
      if (postStatus === "published") {
        setTimeout(
          () => (window.location.href = "/blog/" + data.slug + "/"),
          1200,
        );
      } else {
        // Stay on editor, update slug for future saves
        editingSlug = data.slug;
        await loadMyPosts(); // Refresh table
      }
    } else {
      showToast(data.error || "Save failed.", true);
    }
  } catch (err) {
    console.error(err);
    showToast("Network error. Please try again.", true);
  } finally {
    if (btn) {
      btn.textContent = origText;
      btn.disabled = false;
    }
  }
}

// ── My Posts table ────────────────────────────────────────
async function loadMyPosts() {
  const tbody = document.getElementById("my-posts-body");
  if (!tbody) return;

  tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--text-dim);padding:2rem;font-family:'Share Tech Mono',monospace;letter-spacing:.1em">LOADING...</td></tr>`;

  try {
    const res = await fetch("/api/blogs/staff/");
    if (!res.ok) {
      tbody.innerHTML = `<tr><td colspan="5" style="color:var(--accent3);text-align:center;padding:2rem;font-family:'Share Tech Mono',monospace">Auth error — please re-login.</td></tr>`;
      return;
    }

    const raw = await res.json();
    // Handle both array response and paginated {results:[]} format
    const posts = Array.isArray(raw) ? raw : raw.results || [];

    if (!posts.length) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--text-dim);padding:2.5rem;font-family:'Share Tech Mono',monospace;letter-spacing:.1em">NO POSTS YET — WRITE YOUR FIRST ONE ABOVE ↑</td></tr>`;
      return;
    }

    tbody.innerHTML = posts
      .map((p) => {
        // Guard all fields against undefined/null
        const title = p.title || "Untitled";
        const slug = p.slug || "";
        const status = p.status || "draft";
        const catName = p.category?.name || "—";
        const catColor = p.category?.color || "var(--text-dim)";
        const date = p.published_date || "—";

        return `
        <tr>
          <td style="color:#fff;font-family:'Orbitron',monospace;font-size:.82rem;max-width:260px">
            <a href="/blog/${slug}/" target="_blank" style="color:#fff;text-decoration:none;line-height:1.4;display:block"
               title="${title}">${title.length > 50 ? title.substring(0, 50) + "…" : title}</a>
          </td>
          <td style="color:${catColor};font-family:'Share Tech Mono',monospace;font-size:.8rem">${catName}</td>
          <td><span class="post-status-badge ${status}">${status.toUpperCase()}</span></td>
          <td style="font-family:'Share Tech Mono',monospace;font-size:.72rem;color:var(--text-dim)">${date}</td>
          <td>
            <div class="post-actions">
              <button class="post-action-btn edit"   onclick="editPost('${slug}')">✎ EDIT</button>
              <button class="post-action-btn delete" onclick="deletePost('${slug}', this)">✕ DEL</button>
            </div>
          </td>
        </tr>
      `;
      })
      .join("");
  } catch (e) {
    console.error("loadMyPosts error:", e);
    tbody.innerHTML = `<tr><td colspan="5" style="color:var(--accent3);text-align:center;padding:2rem;font-family:'Share Tech Mono',monospace">Error loading posts: ${e.message}</td></tr>`;
  }
}

function editPost(slug) {
  // Load post into editor without page reload
  editingSlug = slug;
  loadPostForEdit(slug);
  document.getElementById("editor-heading").textContent = "EDIT POST";
  document.getElementById("editor-breadcrumb-post").textContent = slug;
  window.scrollTo({ top: 0, behavior: "smooth" });
  showToast("Post loaded for editing.");
}

async function deletePost(slug, btn) {
  if (!confirm('Delete "' + slug + '"? This cannot be undone.')) return;
  const origText = btn.textContent;
  btn.textContent = "...";
  btn.disabled = true;

  const res = await fetch("/api/blogs/" + slug + "/delete/", {
    method: "DELETE",
    headers: { "X-CSRFToken": getCsrf() },
  });

  if (res.ok) {
    showToast("Post deleted.");
    btn.closest("tr").style.opacity = "0";
    setTimeout(() => {
      btn.closest("tr").remove();
    }, 300);
    if (editingSlug === slug) {
      editingSlug = null;
      document.getElementById("post-title").value = "";
      document.getElementById("rich-editor").innerHTML = "";
      document.getElementById("editor-heading").textContent = "WRITE NEW POST";
    }
  } else {
    showToast("Delete failed.", true);
    btn.textContent = origText;
    btn.disabled = false;
  }
}

/* ============================================================
   BLOG_LIST.JS — Blog listing page with search, filter, pagination
   ============================================================ */

let currentPage = 1;
let currentCat = '';
let searchTimeout;

// ── Load Categories ──
async function loadCategories() {
  try {
    const res = await fetch('/api/categories/');
    const cats = await res.json();
    const filters = document.getElementById('cat-filters');

    cats.forEach(c => {
      const btn = document.createElement('button');
      btn.className = 'cat-btn';
      btn.dataset.cat = c.slug;
      btn.textContent = c.name.toUpperCase() + ' (' + c.post_count + ')';
      btn.style.borderColor = c.color + '66';

      btn.addEventListener('click', () => {
        document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCat = c.slug;
        currentPage = 1;
        loadPosts();
      });

      filters.appendChild(btn);
    });
  } catch (e) {
    console.error('Failed to load categories:', e);
  }
}

// ── Load Posts ──
async function loadPosts() {
  const grid = document.getElementById('blog-grid');
  grid.innerHTML = '<div class="loading" style="grid-column:1/-1">LOADING</div>';

  const search = document.getElementById('search-input').value;
  let url = `/api/blogs/?page=${currentPage}&page_size=6`;
  if (currentCat) url += '&category=' + currentCat;
  if (search) url += '&search=' + encodeURIComponent(search);

  try {
    const res = await fetch(url);
    const data = await res.json();
    renderPosts(data.results);
    renderPagination(data);
  } catch (e) {
    console.error('Failed to load posts:', e);
    grid.innerHTML = '<div class="no-posts" style="grid-column:1/-1"><div class="no-posts-icon">⚠</div><div>FAILED TO LOAD POSTS</div></div>';
  }
}

// ── Render Posts ──
function renderPosts(posts) {
  const grid = document.getElementById('blog-grid');

  if (!posts.length) {
    grid.innerHTML = `
      <div class="no-posts" style="grid-column:1/-1">
        <div class="no-posts-icon">📭</div>
        <div>NO POSTS FOUND</div>
      </div>`;
    return;
  }

  grid.innerHTML = posts.map(p => `
    <a href="/blog/${p.slug}/" class="blog-list-card fade-up visible">
      ${p.is_featured ? '<div class="featured-badge">★ FEATURED</div>' : ''}
      <div class="list-card-cat" style="color:${p.category?.color || 'var(--accent2)'};--cat-color:${p.category?.color || 'var(--accent2)'}">
        <span style="display:inline-block;width:15px;height:1px;background:${p.category?.color || 'var(--accent2)'}"></span>
        ${p.category ? p.category.name.toUpperCase() : 'GENERAL'}
      </div>
      <div class="list-card-title">${p.title}</div>
      <div class="list-card-excerpt">${p.excerpt}</div>
      <div class="list-card-meta">
        <div>
          <div class="list-card-date">${p.published_date} · ${p.read_time} MIN READ</div>
          <div class="list-card-views">${p.views} VIEWS</div>
        </div>
        <span class="list-card-read">READ →</span>
      </div>
    </a>
  `).join('');
}

// ── Render Pagination ──
function renderPagination(data) {
  const pg = document.getElementById('pagination');
  if (data.total_pages <= 1) { pg.innerHTML = ''; return; }

  let html = `<button class="page-btn" onclick="goPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>← PREV</button>`;
  for (let i = 1; i <= data.total_pages; i++) {
    html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goPage(${i})">${i}</button>`;
  }
  html += `<button class="page-btn" onclick="goPage(${currentPage + 1})" ${currentPage === data.total_pages ? 'disabled' : ''}>NEXT →</button>`;
  pg.innerHTML = html;
}

// ── Pagination click ──
function goPage(p) {
  currentPage = p;
  loadPosts();
  window.scrollTo({ top: 300, behavior: 'smooth' });
}

// ── Search input ──
document.getElementById('search-input').addEventListener('input', function () {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => { currentPage = 1; loadPosts(); }, 400);
});

// ── All posts button ──
document.querySelector('.cat-btn[data-cat=""]').addEventListener('click', function () {
  document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
  this.classList.add('active');
  currentCat = '';
  currentPage = 1;
  loadPosts();
});

// ── Init ──
loadCategories();
loadPosts();

/* ============================================
   BLOG-LIST.JS — Blog listing page logic
   ============================================ */

let currentPage = 1;
let currentCat  = '';
let searchTimeout;


// ---- Load categories into filter bar ----
async function loadCategories() {
  const res  = await fetch('/api/categories/');
  const cats = await res.json();
  const filters = document.getElementById('cat-filters');
  if (!filters) return;

  cats.forEach(c => {
    const btn = document.createElement('button');
    btn.className    = 'cat-btn';
    btn.dataset.cat  = c.slug;
    btn.textContent  = c.name.toUpperCase() + ' (' + c.post_count + ')';
    btn.style.borderColor = c.color + '66';

    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCat  = c.slug;
      currentPage = 1;
      loadPosts();
    });

    filters.appendChild(btn);
  });
}


// ---- Load paginated posts ----
async function loadPosts() {
  const grid   = document.getElementById('blog-grid');
  const search = document.getElementById('search-input')?.value || '';
  if (!grid) return;

  grid.innerHTML = `<div class="loading">LOADING</div>`;

  let url = `/api/blogs/?page=${currentPage}&page_size=6`;
  if (currentCat) url += '&category=' + currentCat;
  if (search)     url += '&search=' + encodeURIComponent(search);

  const res  = await fetch(url);
  const data = await res.json();

  renderPosts(data.results);
  renderPagination(data);
}


// ---- Render post cards ----
function renderPosts(posts) {
  const grid = document.getElementById('blog-grid');
  if (!grid) return;

  if (!posts || !posts.length) {
    grid.innerHTML = `
      <div class="no-posts">
        <div class="no-posts-icon">📭</div>
        <div>NO POSTS FOUND</div>
      </div>`;
    return;
  }

  grid.innerHTML = posts.map(p => `
    <a href="/blog/${p.slug}/" class="blog-card fade-up visible">
      ${p.is_featured ? '<div class="featured-badge">★ FEATURED</div>' : ''}
      <div class="blog-cat" style="color:${p.category?.color || 'var(--accent2)'}">
        <span style="display:inline-block;width:15px;height:1px;background:${p.category?.color || 'var(--accent2)'}"></span>
        ${p.category ? p.category.name.toUpperCase() : 'GENERAL'}
      </div>
      <div class="blog-title">${p.title}</div>
      <div class="blog-excerpt">${p.excerpt}</div>
      <div class="blog-meta">
        <div>
          <div class="blog-date">${p.published_date} · ${p.read_time} MIN READ</div>
          <div class="blog-views">${p.views} VIEWS</div>
        </div>
        <span class="blog-read">READ →</span>
      </div>
    </a>
  `).join('');
}


// ---- Render pagination controls ----
function renderPagination(data) {
  const pg = document.getElementById('pagination');
  if (!pg) return;

  if (data.total_pages <= 1) {
    pg.innerHTML = '';
    return;
  }

  let html = `<button class="page-btn" onclick="goPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>← PREV</button>`;

  for (let i = 1; i <= data.total_pages; i++) {
    html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goPage(${i})">${i}</button>`;
  }

  html += `<button class="page-btn" onclick="goPage(${currentPage + 1})" ${currentPage === data.total_pages ? 'disabled' : ''}>NEXT →</button>`;
  pg.innerHTML = html;
}


// ---- Go to page ----
function goPage(p) {
  currentPage = p;
  loadPosts();
  window.scrollTo({ top: 300, behavior: 'smooth' });
}


// ---- Search input handler ----
const searchInput = document.getElementById('search-input');
if (searchInput) {
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      currentPage = 1;
      loadPosts();
    }, 400);
  });
}


// ---- All posts button (reset category) ----
const allBtn = document.querySelector('.cat-btn[data-cat=""]');
if (allBtn) {
  allBtn.addEventListener('click', () => {
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    allBtn.classList.add('active');
    currentCat  = '';
    currentPage = 1;
    loadPosts();
  });
}


// ---- Init ----
loadCategories();
loadPosts();

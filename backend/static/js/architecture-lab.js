(() => {
  const init = () => {
  const byId = (id) => document.getElementById(id);

  let shared = null;              // { components, traffic_metrics, decisions, failure_modes, adrs, simulator_bottlenecks }
  const scenarioDetails = {};     // keyed by scenario key, fetched lazily from /api/scenarios/<key>/
  let activeStage = 'requirements';
  let activeScenario = null;

  function renderStage() {
    const detail = scenarioDetails[activeScenario];
    if (!detail) return;
    const stage = detail.stages[activeStage];
    if (!stage) return;
    byId('architecture-mode').textContent = stage.mode;
    document.querySelector('.journey .section-head h2').textContent = detail.journey_title || detail.title;
    byId('stage-copy').innerHTML = `<span class="section-kicker">${stage.mode}</span><h3>${stage.title}</h3><p>${stage.text}</p><ul>${stage.points.map(x => `<li>${x}</li>`).join('')}</ul>`;
    const d = byId('architecture-diagram');
    d.innerHTML = stage.nodes.map((n, i) => `<button class="diagram-node" data-component="${n}">${n}</button>${i < stage.nodes.length - 1 ? '<span class="diagram-arrow">→</span>' : ''}`).join('');
    d.querySelectorAll('.diagram-node').forEach(n => n.onclick = () => inspect(n.dataset.component));
  }

  function inspect(name) {
    const c = shared && shared.components[name];
    const info = c
      ? [c.display_name, c.problem, c.decision, c.tradeoff, c.alternatives]
      : [name, 'This component supports the delivery path at this stage.', 'It keeps the architecture legible while the constraints remain visible.', 'Every component adds surface area to operate.', 'A simpler design until the measured bottleneck requires it.'];
    let panel = byId('component-inspector');
    if (!panel) {
      panel = document.createElement('aside');
      panel.id = 'component-inspector';
      panel.className = 'component-inspector';
      document.querySelector('.journey-layout').after(panel);
    }
    panel.innerHTML = `<span class="section-kicker">COMPONENT INSPECTION</span><h3>Why ${info[0]}?</h3><p><b>Problem:</b> ${info[1]}</p><p><b>Decision:</b> ${info[2]}</p><p><b>Trade-off:</b> ${info[3]}</p><p><b>Alternatives:</b> ${info[4]}</p>`;
    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function updateMetrics(v) {
    if (!shared) return;
    const m = shared.traffic_metrics[v];
    if (!m) return;
    byId('metric-events').textContent = m.events;
    byId('metric-throughput').textContent = m.throughput;
    byId('metric-latency').textContent = m.latency;
    byId('metric-errors').textContent = m.error_rate;
    byId('metric-lag').textContent = m.queue_lag;
    byId('metric-db').textContent = m.db_load;
    if (v >= 2 && activeStage !== 'evolved') { activeStage = 'bottleneck'; renderStage(); }
  }

  function recommendation() {
    const detail = scenarioDetails[activeScenario];
    if (!detail || !shared) return;
    const values = ['sim-traffic', 'sim-latency', 'sim-availability', 'sim-budget'].map(id => +byId(id).value);
    const [traffic, latency, availability, budget] = values;
    const labels = [['10K events/day', '100K events/day', '1M events/day', '10M events/day'], ['500 ms', '250 ms', '100 ms', '20 ms'], ['99%', '99.5%', '99.9%', '99.99%'], ['$', '$$', '$$$', '$$$$$']];
    ['sim-traffic', 'sim-latency', 'sim-availability', 'sim-budget'].forEach((id, index) => byId(id).nextElementSibling.textContent = labels[index][values[index]]);
    const pressure = traffic + latency + availability - budget;
    const tier = pressure <= 0 ? 0 : pressure <= 3 ? 1 : pressure <= 6 ? 2 : 3;
    const plan = detail.simulator_plans[tier];
    if (!plan) return;
    const bottleneckEntry = shared.simulator_bottlenecks.find(b => b.tier === tier);
    const bottleneck = bottleneckEntry ? bottleneckEntry.text : '';
    byId('recommendation').innerHTML = `<span class="section-kicker">RECOMMENDED ARCHITECTURE · ${activeScenario.toUpperCase()}</span><h3>${plan.name}</h3><pre>${plan.diagram}</pre><p>Every slider changes the pressure score and recommendation. These are engineering estimates, not benchmarks.</p><dl><div><dt>COMPLEXITY</dt><dd>${['Low', 'Moderate', 'High', 'Very high'][tier]}</dd></div><div><dt>SCALABILITY</dt><dd>${['Moderate', 'Queued', 'Horizontal', 'Multi-region'][tier]}</dd></div><div><dt>COST PROFILE</dt><dd>${'$'.repeat(budget + 1)}</dd></div><div><dt>PRIMARY BOTTLENECK</dt><dd>${bottleneck}</dd></div></dl>`;
  }

  async function fetchScenarioDetail(key) {
    if (scenarioDetails[key]) return scenarioDetails[key];
    const res = await fetch(`/api/scenarios/${key}/`);
    const data = await res.json();
    scenarioDetails[key] = data;
    return data;
  }

  const openScenario = async (card) => {
    const key = card.dataset.scenario;
    document.querySelectorAll('.scenario-card').forEach(x => x.classList.toggle('selected', x === card));
    byId('journey').hidden = false;
    byId('stage-copy').innerHTML = '<div class="loading">LOADING SCENARIO</div>';
    byId('journey').scrollIntoView({ behavior: 'smooth', block: 'start' });
    try {
      await fetchScenarioDetail(key);
    } catch (e) {
      console.error('fetchScenarioDetail error:', e);
      byId('stage-copy').innerHTML = '<p>Could not load this scenario. Please try again.</p>';
      return;
    }
    activeScenario = key;
    activeStage = 'requirements';
    document.querySelectorAll('.stage-tab').forEach(t => t.classList.toggle('active', t.dataset.stage === 'requirements'));
    renderStage();
    const panel = byId('component-inspector');
    if (panel) panel.remove();
    recommendation();
  };

  function bindScenarioCards() {
    document.querySelectorAll('.scenario-card').forEach(card => {
      card.onclick = () => openScenario(card);
      card.onkeydown = (event) => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openScenario(card); } };
    });
  }

  async function loadScenarios() {
    const stack = byId('scenario-stack');
    if (!stack) return null;
    try {
      const res = await fetch('/api/scenarios/');
      const data = await res.json();
      if (!Array.isArray(data) || !data.length) return null;
      stack.innerHTML = data.map((s, i) => `
        <article class="scenario-card${i === 0 ? ' selected' : ''}" data-scenario="${s.key}" tabindex="0">
          <div class="scenario-num">${s.number}</div>
          <div class="scenario-main"><span class="difficulty">${s.difficulty}</span>
            <h3>${s.title}</h3>
            <p>${s.description}</p>
          </div>
          <div class="requirement-chips">${(s.requirement_chips || []).map(c => `<span>${c}</span>`).join('')}</div>
          <button class="scenario-open" aria-label="Open ${s.title} scenario">→</button>
        </article>`).join('');
      bindScenarioCards();
      return data;
    } catch (e) {
      console.error('loadScenarios error:', e);
      return null;
    }
  }

  function renderSharedSections() {
    byId('decision-grid').innerHTML = shared.decisions.map(d => `<article class="decision-card"><span class="section-kicker">DECISION</span><h3>${d.title}</h3><p><b>Problem:</b> ${d.problem}</p><p><b>Decision:</b> ${d.decision}</p><button>EXPLORE TRADE-OFFS +</button><div class="decision-detail"><p>${d.detail}</p><p><b>${d.alternatives}</b></p></div></article>`).join('');
    document.querySelectorAll('.decision-card button').forEach(b => b.onclick = () => b.parentElement.classList.toggle('expanded'));

    byId('failure-controls').innerHTML = shared.failure_modes.map(f => `<button class="failure-btn" data-failure="${f.name}">🔴 ${f.name}</button>`).join('');
    document.querySelectorAll('.failure-btn').forEach(b => b.onclick = () => {
      document.querySelectorAll('.failure-btn').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      const f = shared.failure_modes.find(x => x.name === b.dataset.failure);
      if (!f) return;
      byId('failure-result').innerHTML = `<span class="impact-label">IMPACT — ${f.impact}</span><h3>${f.name}</h3><p><b>System response:</b> ${f.response}</p><p><b>Recovery strategy:</b> ${f.recovery}</p>`;
    });

    byId('adr-list').innerHTML = shared.adrs.map(x => `<article class="adr-item"><button class="adr-summary"><span class="adr-id">${x.identifier}</span><strong>${x.title}</strong><span>+</span></button><div class="adr-body">${x.detail}</div></article>`).join('');
    document.querySelectorAll('.adr-summary').forEach(x => x.onclick = () => x.parentElement.classList.toggle('open'));
  }

  async function loadShared() {
    try {
      const res = await fetch('/api/lab-shared/');
      shared = await res.json();
      renderSharedSections();
      return shared;
    } catch (e) {
      console.error('loadShared error:', e);
      return null;
    }
  }

  document.querySelectorAll('.stage-tab').forEach(btn => btn.onclick = () => {
    if (!activeScenario) return;
    document.querySelectorAll('.stage-tab').forEach(x => x.classList.remove('active'));
    btn.classList.add('active');
    activeStage = btn.dataset.stage;
    renderStage();
  });

  byId('traffic-control').querySelector('input').oninput = (e) => {
    const v = +e.target.value;
    const label = shared && shared.traffic_metrics[v] ? shared.traffic_metrics[v].traffic_label : '';
    byId('traffic-value').textContent = label;
    updateMetrics(v);
  };

  byId('cache-toggle').onclick = () => { const on = byId('cache-toggle').getAttribute('aria-pressed') === 'true'; byId('cache-toggle').setAttribute('aria-pressed', !on); byId('cache-toggle').innerHTML = `CACHE <b>${on ? 'OFF' : 'ON'}</b>`; byId('cache-impact').textContent = on ? 'Cache bypasses PostgreSQL: latency and database pressure rise, but durable delivery remains available.' : 'Redis absorbs repeat preference and template reads, keeping Postgres focused on durable delivery state.'; byId('cache-requests').textContent = on ? '100%' : '36%'; byId('cache-latency').textContent = on ? '142 ms' : '48 ms'; byId('cache-headroom').textContent = on ? '1.0×' : '2.8×'; };

  document.querySelectorAll('.sim-controls input').forEach(x => x.oninput = recommendation);
  document.querySelector('[data-action="scenario"]').onclick = () => byId('scenarios').scrollIntoView({ behavior: 'smooth' });
  byId('journey').hidden = true;

  // Boot: load the scenario cards + shared (component/decision/failure/ADR/metric) data in
  // parallel, then eagerly warm the default (first) scenario so the always-visible simulator
  // panel has something to recommend before the visitor opens a card themselves.
  (async function boot() {
    const [scenarioList] = await Promise.all([loadScenarios(), loadShared()]);
    if (!scenarioList || !scenarioList.length) return;
    try {
      await fetchScenarioDetail(scenarioList[0].key);
      activeScenario = scenarioList[0].key;
      recommendation();
    } catch (e) {
      console.error('default scenario detail error:', e);
    }
  })();
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();

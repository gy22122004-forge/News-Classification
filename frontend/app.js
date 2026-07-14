// ─── Category Config ─────────────────────────────────────────────────────────
const CATEGORY_CONFIG = {
  "Politics":      { icon: "🏛️", color: "#7c3aed" },
  "Sports":        { icon: "⚽", color: "#16a34a" },
  "Business":      { icon: "💼", color: "#1d4ed8" },
  "Technology":    { icon: "💻", color: "#0891b2" },
  "Health":        { icon: "🏥", color: "#db2777" },
  "Entertainment": { icon: "🎬", color: "#ea580c" },
  "Science":       { icon: "🔬", color: "#0d9488" },
  "World News":    { icon: "🌍", color: "#4f46e5" },
};

const SAMPLES = [
  { label: "🏛️ Politics — Senate climate bill",
    text: "The Senate passed a landmark climate bill with a 62-38 bipartisan vote, marking the most significant environmental legislation in over a decade. The president is expected to sign it into law by next week, allocating $370 billion toward renewable energy subsidies and emissions reduction targets." },
  { label: "⚽ Sports — Champions League final",
    text: "Manchester City defeated Real Madrid 3-1 in the UEFA Champions League final at Wembley Stadium. Erling Haaland scored a hat-trick in what analysts are calling the greatest individual performance in final history, cementing City's treble-winning season under Pep Guardiola." },
  { label: "💻 Technology — Apple M4 chip",
    text: "Apple unveiled its next-generation M4 Pro chip at WWDC, claiming a 40% performance boost over its predecessor. The new chip features an 18-core CPU and a dedicated AI neural engine processing 38 trillion operations per second for on-device machine learning tasks." },
  { label: "🏥 Health — Anti-aging breakthrough",
    text: "Researchers at Harvard Medical School have discovered a novel compound that can reverse cellular aging in mice by up to 30%. The study, published in Nature, found that the compound restores mitochondrial function and could lead to treatments for age-related diseases in humans." },
  { label: "🔬 Science — James Webb exoplanet",
    text: "NASA's James Webb Space Telescope has detected water ice and carbon dioxide in the atmosphere of an exoplanet 124 light-years away. The discovery is the strongest evidence yet of potentially habitable conditions beyond our solar system and could reshape astrobiology." },
  { label: "🌍 World News — G7 summit",
    text: "Leaders from G7 nations convened in Rome for a two-day summit focused on global trade reform and AI governance. A joint communiqué released Saturday committed members to a new international framework for regulating large language models and autonomous AI systems by 2027." },
];

// ─── DOM Refs ─────────────────────────────────────────────────────────────────
const textarea         = document.getElementById("newsInput");
const classifyBtn      = document.getElementById("classifyBtn");
const charCountEl      = document.getElementById("charCount");
const stateLoading     = document.getElementById("stateLoading");
const stateError       = document.getElementById("stateError");
const errorText        = document.getElementById("errorText");
const statePlaceholder = document.getElementById("statePlaceholder");
const stateResults     = document.getElementById("stateResults");
const samplesList      = document.getElementById("samplesList");

// ─── Build Sample Buttons ────────────────────────────────────────────────────
SAMPLES.forEach((s, i) => {
  const btn = document.createElement("button");
  btn.className = "sample-btn";
  btn.id = `sample-btn-${i}`;
  btn.title = s.text.slice(0, 100) + "…";
  btn.textContent = s.label;
  btn.addEventListener("click", () => {
    textarea.value = s.text;
    updateChar();
    textarea.focus();
  });
  samplesList.appendChild(btn);
});

// ─── Code Tabs ────────────────────────────────────────────────────────────────
document.querySelectorAll(".tab-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".code-panel").forEach(p => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
  });
});

// ─── Char Count ──────────────────────────────────────────────────────────────
function updateChar() {
  const len = textarea.value.length;
  charCountEl.textContent = `${len.toLocaleString()} / 10,000`;
  charCountEl.classList.toggle("warn", len > 9500);
}
textarea.addEventListener("input", updateChar);

// ─── Keyboard shortcut ───────────────────────────────────────────────────────
textarea.addEventListener("keydown", e => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") classifyBtn.click();
});

// ─── Classify ────────────────────────────────────────────────────────────────
classifyBtn.addEventListener("click", async () => {
  const text = textarea.value.trim();
  if (!text) { showError("Please enter some news text first."); return; }
  await runClassification(text);
});

async function runClassification(text) {
  setState("loading");
  try {
    const res = await fetch("/classify", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ text }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    renderResults(data);
    setState("results");
  } catch (err) {
    const msg = err.message.match(/fetch|Failed|NetworkError|ERR_CONNECTION/)
      ? "Cannot reach the classification API — make sure the server is running on port 8000."
      : err.message;
    showError(msg);
  }
}

// ─── Render Results ──────────────────────────────────────────────────────────
function renderResults(data) {
  const top    = data.categories[0];
  const topCfg = CATEGORY_CONFIG[top.label] || { icon: "📰", color: "#1d4ed8" };

  // Top badge
  document.getElementById("topIcon").textContent  = topCfg.icon;
  document.getElementById("topName").textContent  = top.label;
  document.getElementById("topScore").textContent = top.percentage.toFixed(1) + "%";

  // Score chart
  const chart = document.getElementById("scoreChart");
  chart.innerHTML = "";

  data.categories.forEach((cat, idx) => {
    const cfg   = CATEGORY_CONFIG[cat.label] || { icon: "📰", color: "#1d4ed8" };
    const isTop = idx === 0;
    const row   = document.createElement("div");
    row.className = "score-row-item";
    row.style.animationDelay = `${idx * 0.06}s`;
    row.innerHTML = `
      <span class="sc-icon">${cfg.icon}</span>
      <span class="sc-label">${cat.label}</span>
      <div class="sc-bar-wrap">
        <div class="sc-bar" style="--bar-color:${cfg.color};" data-pct="${cat.percentage}"></div>
      </div>
      <span class="sc-pct${isTop ? " top-pct" : ""}">${cat.percentage.toFixed(1)}%</span>
    `;
    chart.appendChild(row);
  });

  // Animate bars
  requestAnimationFrame(() => requestAnimationFrame(() => {
    chart.querySelectorAll(".sc-bar").forEach(bar => {
      bar.style.width = Math.max(parseFloat(bar.dataset.pct), 0.4) + "%";
    });
  }));

  // Meta
  document.getElementById("metaWords").textContent = data.word_count.toLocaleString();
  document.getElementById("metaChars").textContent = data.char_count.toLocaleString();
  document.getElementById("metaTime").textContent  = data.processing_time_ms.toFixed(0) + " ms";
}

// ─── State Manager ───────────────────────────────────────────────────────────
function setState(state) {
  stateLoading.style.display     = state === "loading" ? "flex" : "none";
  stateError.style.display       = state === "error"   ? "flex" : "none";
  statePlaceholder.style.display = state === "idle"    ? "flex" : "none";
  stateResults.style.display     = state === "results" ? "block" : "none";

  classifyBtn.disabled    = state === "loading";
  classifyBtn.innerHTML   = state === "loading"
    ? '<span class="btn-icon">⏳</span> Classifying…'
    : '<span class="btn-icon">▶</span> Run Classification';
}

function showError(msg) {
  errorText.textContent = msg;
  setState("error");
}

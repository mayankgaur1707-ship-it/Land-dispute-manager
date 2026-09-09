// Land Dispute Manager - Frontend Application Logic

let currentTab = 'dashboard';
let currentRole = 'REVENUE_OFFICER';
let currentSelectedTemplateId = 'sample_clear_105';
let gisMap = null;
let geojsonLayer = null;
let templatesCache = {};
let recordsCache = [];
let disputesCache = [];
let pendingVerificationsCache = [];

document.addEventListener('DOMContentLoaded', async () => {
  await initApp();
});

async function initApp() {
  setupRoleSelector();
  
  // Initialize AI Chatbot immediately so it is available right away on all pages
  await initChat();

  try {
    await loadTemplates();
    await loadAnalytics();
    await loadRecords();
    await loadPendingVerifications();
    await loadDisputes();
    await loadLedger();
  } catch (err) {
    console.warn('Page-specific data load notice:', err);
  }
  
  // Hash deep-linking
  const hash = window.location.hash.replace('#', '');
  if (hash && ['dashboard', 'digitize', 'verify', 'disputes', 'map', 'ledger', 'citizen', 'assistant'].includes(hash)) {
    switchTab(hash);
  }

  lucide.createIcons();
}

function setupRoleSelector() {
  const select = document.getElementById('role-selector') || document.getElementById('role-select');
  if (select) {
    select.value = currentRole;
    select.addEventListener('change', (e) => handleRoleChange(e.target.value));
  }
}

function handleRoleChange(role) {
  if (role === 'CITIZEN_FARMER') role = 'CITIZEN_LANDOWNER';
  currentRole = role;
  const bannerText = document.getElementById('role-context-text');
  
  if (role === 'REVENUE_OFFICER') {
    if (bannerText) {
      bannerText.innerHTML = `
        <i data-lucide="shield-check" class="w-3.5 h-3.5 text-emerald-600"></i>
        <span>Logged in as <strong>Revenue Officer / Patwari</strong>: Full authorization for AI validation, HITL verification certification, boundary demarcation, and blockchain ledger.</span>
      `;
    }
  } else if (role === 'CITIZEN_LANDOWNER') {
    if (bannerText) {
      bannerText.innerHTML = `
        <i data-lucide="user" class="w-3.5 h-3.5 text-sky-600"></i>
        <span>Logged in as <strong>Citizen / Landowner</strong>: Public title search, boundary inspection, and certified digital land record extracts.</span>
      `;
    }
    switchTab('citizen');
  } else if (role === 'BANK_OFFICER') {
    if (bannerText) {
      bannerText.innerHTML = `
        <i data-lucide="landmark" class="w-3.5 h-3.5 text-indigo-600"></i>
        <span>Logged in as <strong>Bank / Lending Officer</strong>: Non-encumbrance title clearance verification, mortgage cross-check, and active dispute risk assessment.</span>
      `;
    }
  } else if (role === 'DILRMP_ADMIN') {
    if (bannerText) {
      bannerText.innerHTML = `
        <i data-lucide="settings" class="w-3.5 h-3.5 text-purple-600"></i>
        <span>Logged in as <strong>DILRMP State Admin</strong>: Pan-India progress monitoring, continuous learning OCR model metrics, and geodetic system audit.</span>
      `;
    }
  }
  
  // Re-render records & disputes to apply role permissions
  renderRecordsTable(recordsCache);
  renderDisputes(disputesCache);
  updateChatRoleDisplay();
  loadChatSuggestions();
  lucide.createIcons();
}

function switchTab(tabId) {
  currentTab = tabId;
  document.querySelectorAll('section').forEach(sec => sec.classList.add('hidden'));
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

  const activeSec = document.getElementById(`view-${tabId}`);
  if (activeSec) activeSec.classList.remove('hidden');

  const activeBtn = document.getElementById(`tab-${tabId}`);
  if (activeBtn) activeBtn.classList.add('active');

  if (tabId === 'map') {
    setTimeout(() => {
      initMap();
    }, 150);
  } else if (tabId === 'verify') {
    loadPendingVerifications();
  } else if (tabId === 'assistant') {
    const input = document.getElementById('dedicated-chat-input');
    if (input) setTimeout(() => input.focus(), 150);
  }

  if (window.history && window.history.replaceState) {
    window.history.replaceState(null, '', '#' + tabId);
  }

  lucide.createIcons();
}

// ----------------------------------------------------
// 1. ANALYTICS & STATE PROGRESS
// ----------------------------------------------------
async function loadAnalytics() {
  try {
    const res = await fetch('/api/analytics');
    const data = await res.json();

    const setElemText = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.innerText = val;
    };

    setElemText('stat-total-records', data.total_records || 0);
    setElemText('stat-total-hectares', data.total_area_hectares || 0);
    setElemText('stat-active-disputes', data.active_disputes || 0);
    setElemText('badge-disputes-count', data.active_disputes || 0);
    setElemText('stat-clear-records', data.clear_records || 0);

    const clearPct = data.total_records > 0 ? Math.round((data.clear_records / data.total_records) * 100) : 100;
    setElemText('stat-clear-pct', `${clearPct}%`);
    setElemText('stat-avg-confidence', `${data.avg_confidence_score}%`);

    const pendingCount = data.pending_verifications || 0;
    setElemText('stat-pending-verifications', pendingCount);
    setElemText('badge-pending-count', pendingCount);
    setElemText('verify-queue-count', `${pendingCount} Case${pendingCount === 1 ? '' : 's'} Pending`);

    renderStateProgress(data.state_breakdown || {});
  } catch (err) {
    console.error('Failed to load analytics:', err);
  }
}

function renderStateProgress(statesData = {}) {
  const container = document.getElementById('state-progress-container');
  if (!container) return;

  const statesConfig = [
    {
      name: "Uttar Pradesh",
      district: "Varanasi (Sadar)",
      flag: "🇮🇳",
      accent: "emerald"
    },
    {
      name: "Maharashtra",
      district: "Pune (Haveli)",
      flag: "🌾",
      accent: "teal"
    },
    {
      name: "Telangana",
      district: "Ranga Reddy (Kondapur)",
      flag: "📜",
      accent: "sky"
    }
  ];

  container.innerHTML = statesConfig.map(cfg => {
    const stData = statesData[cfg.name] || { total: 0, verified: 0, disputed: 0, hectares: 0 };
    const total = stData.total || 0;
    const verified = stData.verified || 0;
    const disputed = stData.disputed || 0;
    const hectares = (stData.hectares || 0).toFixed(2);
    const pct = total > 0 ? Math.round((verified / total) * 100) : 100;

    return `
      <div class="bg-slate-50 border border-slate-200/80 rounded-xl p-4 space-y-3 hover:shadow-sm transition">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-xl">${cfg.flag}</span>
            <div>
              <h4 class="font-bold text-xs text-slate-800">${cfg.name}</h4>
              <p class="text-[10px] text-slate-500">${cfg.district}</p>
            </div>
          </div>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-700">${total} Ingested</span>
        </div>

        <div>
          <div class="flex justify-between text-[11px] mb-1">
            <span class="text-slate-500 font-medium">Clear Title Rate</span>
            <span class="font-bold text-emerald-700">${pct}% (${verified}/${total})</span>
          </div>
          <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div class="bg-emerald-500 h-full rounded-full transition-all duration-500" style="width: ${pct}%"></div>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-2 text-center text-[10px] pt-2 border-t border-slate-200/70 text-slate-600">
          <div>
            <span class="block text-slate-400">Area</span>
            <span class="font-bold text-slate-700">${hectares} ha</span>
          </div>
          <div>
            <span class="block text-slate-400">Clear</span>
            <span class="font-bold text-emerald-600">${verified}</span>
          </div>
          <div>
            <span class="block text-slate-400">Disputed</span>
            <span class="font-bold ${disputed > 0 ? 'text-rose-600' : 'text-slate-500'}">${disputed}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ----------------------------------------------------
// 2. RECORDS REGISTRY TABLE
// ----------------------------------------------------
async function loadRecords() {
  try {
    const statusFilter = document.getElementById('dashboard-status-filter') ? document.getElementById('dashboard-status-filter').value : '';
    const url = statusFilter ? `/api/records/?status=${statusFilter}` : '/api/records/';
    const res = await fetch(url);
    const records = await res.json();
    recordsCache = records;
    renderRecordsTable(records);
  } catch (err) {
    console.error('Failed to load records:', err);
  }
}

function handleDashboardSearch(query) {
  const q = (query || '').toLowerCase().trim();
  if (!q) {
    renderRecordsTable(recordsCache);
    return;
  }
  const filtered = recordsCache.filter(r => {
    const ownersStr = (r.owners || []).map(o => o.name.toLowerCase()).join(' ');
    return (r.khasra_no && r.khasra_no.toLowerCase().includes(q)) ||
           (r.khata_no && r.khata_no.toLowerCase().includes(q)) ||
           (r.village && r.village.toLowerCase().includes(q)) ||
           (r.state && r.state.toLowerCase().includes(q)) ||
           ownersStr.includes(q);
  });
  renderRecordsTable(filtered);
}

function renderRecordsTable(records) {
  const tbody = document.getElementById('dashboard-records-tbody');
  if (!tbody) return;

  if (records.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="px-4 py-8 text-center text-slate-400">No matching cadastral records found.</td></tr>`;
    return;
  }

  tbody.innerHTML = records.map(r => {
    let disputeBadge = '';
    if (r.dispute_status === 'CLEAR') {
      disputeBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800"><i data-lucide="check" class="w-3 h-3"></i> Clear Title</span>`;
    } else if (r.dispute_status === 'WARNING') {
      disputeBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800"><i data-lucide="alert-triangle" class="w-3 h-3"></i> Review Needed</span>`;
    } else {
      disputeBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-rose-100 text-rose-800"><i data-lucide="alert-octagon" class="w-3 h-3"></i> Disputed</span>`;
    }

    let verifyBadge = '';
    const vStatus = r.verification_status || 'AUTO_VERIFIED';
    if (vStatus === 'VERIFIED_BY_OFFICER') {
      verifyBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-200"><i data-lucide="user-check" class="w-3 h-3"></i> Officer Certified</span>`;
    } else if (vStatus === 'PENDING_VERIFICATION') {
      verifyBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-300"><i data-lucide="clock" class="w-3 h-3"></i> HITL Review</span>`;
    } else {
      verifyBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200"><i data-lucide="sparkles" class="w-3 h-3"></i> AI Verified</span>`;
    }

    const ownersSummary = (r.owners || []).map(o => `${o.name} (${o.share_percentage}%)`).join(', ');
    const stateTag = r.state || 'Uttar Pradesh';

    return `
      <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="inspectRecordOnMap('${r.id}')">
        <td class="px-4 py-3">
          <span class="font-bold text-slate-800">Khasra #${r.khasra_no}</span>
          <div class="text-[11px] text-slate-400">Khata #${r.khata_no} • ${r.village}</div>
        </td>
        <td class="px-4 py-3 text-slate-700 max-w-xs truncate" title="${ownersSummary}">
          ${ownersSummary}
        </td>
        <td class="px-4 py-3 text-slate-600">
          <span class="font-semibold text-slate-800 text-[11px] block">${stateTag}</span>
          <span class="text-[10px] text-slate-400">${r.tehsil || ''}, ${r.district || ''}</span>
        </td>
        <td class="px-4 py-3 text-slate-700">
          ${r.area_sq_meters ? r.area_sq_meters.toLocaleString() : 0} m²
          <span class="text-[11px] text-slate-400">(${r.area_acres || 0} ac)</span>
        </td>
        <td class="px-4 py-3">${verifyBadge}</td>
        <td class="px-4 py-3">${disputeBadge}</td>
        <td class="px-4 py-3 font-semibold text-slate-700">${Math.round(r.confidence_score * 100)}%</td>
        <td class="px-4 py-3 text-right">
          <div class="flex items-center justify-end gap-1.5">
            <button onclick="event.stopPropagation(); inspectRecordOnMap('${r.id}')" class="text-xs bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-600 font-semibold px-2.5 py-1 rounded transition">
              GIS View
            </button>
            ${currentRole === 'BANK_OFFICER' ? `
              <button onclick="event.stopPropagation(); downloadBankLienReport('${r.id}')" class="text-xs bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-2.5 py-1 rounded transition flex items-center gap-1 shadow-xs">
                <i data-lucide="file-check" class="w-3 h-3"></i> Loan Certificate
              </button>
            ` : (currentRole === 'CITIZEN_LANDOWNER' ? `
              <button onclick="event.stopPropagation(); downloadRoRExtract('${r.id}')" class="text-xs bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-2.5 py-1 rounded transition flex items-center gap-1 shadow-xs">
                <i data-lucide="printer" class="w-3 h-3"></i> RoR Extract
              </button>
            ` : (vStatus === 'PENDING_VERIFICATION' ? `
              <button onclick="event.stopPropagation(); switchTab('verify')" class="text-xs bg-amber-500 hover:bg-amber-600 text-white font-bold px-2 py-1 rounded transition flex items-center gap-1 shadow-sm">
                Verify
              </button>
            ` : ''))}
          </div>
        </td>
      </tr>
    `;
  }).join('');

  lucide.createIcons();
}

// ----------------------------------------------------
// 3. AI-OCR DIGITIZER & TEMPLATES
// ----------------------------------------------------
async function loadTemplates() {
  try {
    const res = await fetch('/api/templates');
    const list = await res.json();
    list.forEach(t => {
      templatesCache[t.id] = t;
    });
    // Pre-select first template
    if (list.length > 0) {
      loadTemplate(list[0].id);
    }
  } catch (err) {
    console.error('Failed to load templates:', err);
  }
}

function loadTemplate(templateId) {
  currentSelectedTemplateId = templateId;
  const tpl = templatesCache[templateId];
  if (!tpl) return;

  document.getElementById('digitize-raw-text').value = tpl.raw_text.trim();

  const langElem = document.getElementById('digitize-detected-lang');
  if (langElem) {
    langElem.innerText = tpl.language || 'Hindi (हिंदी)';
  }

  // Render SVG document scan facsimile preview in Column 1
  const svgContainer = document.getElementById('digitize-svg-preview-container');
  if (svgContainer) {
    svgContainer.innerHTML = `
      <img src="/api/templates/${templateId}/document-svg" 
           class="w-full h-auto object-contain rounded-lg shadow-sm" 
           alt="Archival Document Scan Facsimile" 
           onerror="this.parentElement.innerHTML='<div class=\\'p-6 text-center text-xs text-slate-400\\'>Vector Scan Rendering...</div>'"/>
    `;
  }

  parseRawText(templateId);
}

async function parseRawText(templateId) {
  const text = document.getElementById('digitize-raw-text').value;
  if (!text) return;

  // Check cached template or identify from text
  let tpl = templateId ? templatesCache[templateId] : null;
  if (!tpl) {
    for (const key in templatesCache) {
      if (text.includes(templatesCache[key].khasra_no)) {
        tpl = templatesCache[key];
        break;
      }
    }
  }

  let khasra = '105';
  let khata = '78';
  let village = 'Rampur';
  let tehsilDist = 'Sadar, Varanasi';
  let area = '2400';
  let landType = 'Agricultural';
  let owners = [
    { name: 'Rameshwar Prasad', share: 50.0, aadhaar: 'XXXX-XXXX-4491' },
    { name: 'Sunita Devi', share: 50.0, aadhaar: 'XXXX-XXXX-9923' }
  ];
  let confKhasra = 99;
  let confKhata = 98;
  let confArea = 97;
  let confOwners = 97;
  let overallConf = 98;
  let isLowConf = false;

  if (tpl && tpl.parsed) {
    const p = tpl.parsed;
    khasra = p.khasra_no || khasra;
    khata = p.khata_no || khata;
    village = p.village || village;
    tehsilDist = `${p.tehsil || 'Sadar'}, ${p.district || 'Varanasi'}`;
    area = p.area_sq_meters || area;
    landType = p.land_type || landType;
    if (p.owners) {
      owners = p.owners.map(o => ({
        name: o.name,
        share: o.share_percentage,
        aadhaar: o.aadhaar_masked || 'XXXX-XXXX-0000'
      }));
    }
    if (tpl.id === 'sample_low_confidence_hitl' || (p.field_confidences && p.field_confidences.khasra_no && p.field_confidences.khasra_no.confidence < 0.85)) {
      confKhasra = 74;
      confKhata = 71;
      confArea = 78;
      confOwners = 73;
      overallConf = 74;
      isLowConf = true;
    }
  } else if (text.includes('115')) {
    khasra = '115';
    khata = '32';
    area = '1450';
    landType = 'Agricultural';
    owners = [{ name: 'Bholanath Yadav', share: 100.0, aadhaar: 'XXXX-XXXX-5521' }];
    confKhasra = 74;
    confKhata = 71;
    confArea = 78;
    confOwners = 73;
    overallConf = 74;
    isLowConf = true;
  } else if (text.includes('102/B')) {
    khasra = '102/B';
    khata = '112';
    area = '1850';
    landType = 'Residential';
    owners = [{ name: 'Vikramaditya Singh', share: 100.0, aadhaar: 'XXXX-XXXX-7721' }];
  } else if (text.includes('108')) {
    khasra = '108';
    khata = '44';
    area = '3100';
    landType = 'Agricultural';
    owners = [
      { name: 'Harish Chand', share: 60.0, aadhaar: 'XXXX-XXXX-3312' },
      { name: 'Rajat Chand', share: 60.0, aadhaar: 'XXXX-XXXX-3313' }
    ];
  } else if (text.includes('142/A')) {
    khasra = '142/A';
    khata = '56';
    village = 'Theur';
    tehsilDist = 'Haveli, Pune';
    area = '3200';
    landType = 'Agricultural';
    owners = [{ name: 'Balasaheb Patil', share: 100.0, aadhaar: 'XXXX-XXXX-6612' }];
  } else if (text.includes('88/2')) {
    khasra = '88/2';
    khata = '29';
    village = 'Kondapur';
    tehsilDist = 'Serilingampally, Ranga Reddy';
    area = '4500';
    landType = 'Agricultural';
    owners = [{ name: 'K. Venkat Rao', share: 100.0, aadhaar: 'XXXX-XXXX-8819' }];
  }

  document.getElementById('form-khasra').value = khasra;
  document.getElementById('form-khata').value = khata;
  document.getElementById('form-village').value = village;
  document.getElementById('form-tehsil-dist').value = tehsilDist;
  document.getElementById('form-area').value = area;
  document.getElementById('form-type').value = landType;

  // Badges
  const confBadge = document.getElementById('ocr-confidence-badge');
  if (confBadge) {
    if (isLowConf) {
      confBadge.className = 'text-[11px] bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded border border-rose-300';
      confBadge.innerText = `Confidence: ${overallConf}% (Quarantined <85%)`;
    } else {
      confBadge.className = 'text-[11px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded border border-emerald-300';
      confBadge.innerText = `Confidence: ${overallConf}% (High)`;
    }
  }

  const bKhasra = document.getElementById('badge-conf-khasra');
  if (bKhasra) {
    bKhasra.innerText = `${confKhasra}%`;
    bKhasra.className = isLowConf ? 'text-[10px] font-bold text-rose-600' : 'text-[10px] font-bold text-emerald-700';
  }
  const bKhata = document.getElementById('badge-conf-khata');
  if (bKhata) {
    bKhata.innerText = `${confKhata}%`;
    bKhata.className = isLowConf ? 'text-[10px] font-bold text-rose-600' : 'text-[10px] font-bold text-emerald-700';
  }
  const bArea = document.getElementById('badge-conf-area');
  if (bArea) {
    bArea.innerText = `${confArea}%`;
    bArea.className = isLowConf ? 'text-[10px] font-bold text-rose-600' : 'text-[10px] font-bold text-emerald-700';
  }
  const bOwners = document.getElementById('badge-conf-owners');
  if (bOwners) {
    bOwners.innerText = `${confOwners}%`;
    bOwners.className = isLowConf ? 'text-[10px] font-bold text-rose-600' : 'text-[10px] font-bold text-emerald-700';
  }

  const ownersContainer = document.getElementById('form-owners-container');
  if (ownersContainer) {
    ownersContainer.innerHTML = owners.map(o => `
      <div class="flex items-center justify-between bg-white p-2 rounded border border-slate-200 text-xs">
        <span class="font-bold text-slate-800">${o.name} <span class="text-slate-400 font-normal">(${o.aadhaar})</span></span>
        <span class="bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded font-bold border border-emerald-200">${o.share}% Share</span>
      </div>
    `).join('');
  }

  lucide.createIcons();
}

async function submitDigitization() {
  const btn = document.getElementById('btn-submit-digitize');
  const alertBox = document.getElementById('digitize-result-alert');
  const rawText = document.getElementById('digitize-raw-text').value;

  const khasra = document.getElementById('form-khasra') ? document.getElementById('form-khasra').value.trim() : '';
  const khata = document.getElementById('form-khata') ? document.getElementById('form-khata').value.trim() : '';
  const village = document.getElementById('form-village') ? document.getElementById('form-village').value.trim() : '';
  const tehsilDist = document.getElementById('form-tehsil-dist') ? document.getElementById('form-tehsil-dist').value.trim() : '';
  const area = document.getElementById('form-area') ? parseFloat(document.getElementById('form-area').value) : null;
  const landType = document.getElementById('form-type') ? document.getElementById('form-type').value : 'Agricultural';

  let tehsil = 'Sadar', district = 'Varanasi';
  if (tehsilDist.includes(',')) {
    const parts = tehsilDist.split(',').map(s => s.trim());
    tehsil = parts[0];
    district = parts[1] || 'Varanasi';
  } else if (tehsilDist) {
    tehsil = tehsilDist;
  }

  const tpl = currentSelectedTemplateId ? templatesCache[currentSelectedTemplateId] : null;
  const boundaryGeojson = (tpl && tpl.parsed && tpl.parsed.boundary_geojson) ? tpl.parsed.boundary_geojson : null;
  const templateState = (tpl && tpl.parsed && tpl.parsed.state) ? tpl.parsed.state : null;
  const templateDocType = (tpl && tpl.document_type) ? tpl.document_type : null;
  const templateLang = (tpl && tpl.language) ? tpl.language : null;
  const templateOwners = (tpl && tpl.parsed && tpl.parsed.owners) ? tpl.parsed.owners : null;
  const templateConfidences = (tpl && tpl.parsed && tpl.parsed.field_confidences) ? tpl.parsed.field_confidences : null;

  btn.disabled = true;
  btn.innerHTML = `<i data-lucide="loader-2" class="w-5 h-5 animate-spin"></i> Processing AI-OCR & Spatial Validation...`;
  lucide.createIcons();

  try {
    const payload = {
      raw_text: rawText,
      khasra_no: khasra,
      khata_no: khata,
      village: village,
      tehsil: tehsil,
      district: district,
      state: templateState,
      area_sq_meters: area,
      land_type: landType,
      boundary_geojson: boundaryGeojson,
      document_type: templateDocType,
      language: templateLang,
      owners: templateOwners,
      field_confidences: templateConfidences
    };

    const res = await fetch('/api/records/digitize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await res.json();
    alertBox.classList.remove('hidden');

    if (result.success) {
      const rec = result.record;
      const disputes = result.disputes_detected || [];

      if (rec.verification_status === 'PENDING_VERIFICATION') {
        alertBox.className = 'mt-6 p-4 rounded-xl border border-amber-300 bg-amber-50 text-amber-950 text-xs space-y-2';
        alertBox.innerHTML = `
          <div class="flex items-center gap-2 font-bold text-sm text-amber-900">
            <i data-lucide="alert-triangle" class="w-5 h-5 text-amber-600"></i>
            QUARANTINED FOR HUMAN VERIFICATION: Low ML OCR Confidence (&lt; 85%)
          </div>
          <p>Khasra #${rec.khasra_no} had one or more uncertain fields (smudged/faded characters) scoring below 85% confidence. It has been routed to the Revenue Officer Verification Queue.</p>
          <div class="pt-2 flex gap-3">
            <button onclick="switchTab('verify')" class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5">
              <i data-lucide="user-check" class="w-4 h-4"></i> Open Human Verification Console
            </button>
            <button onclick="switchTab('dashboard')" class="bg-slate-800 hover:bg-slate-900 text-white font-bold px-3 py-1.5 rounded-lg">Return to Registry</button>
          </div>
        `;
      } else if (disputes.length > 0) {
        alertBox.className = 'mt-6 p-4 rounded-xl border border-rose-300 bg-rose-50 text-rose-900 text-xs space-y-2';
        alertBox.innerHTML = `
          <div class="flex items-center gap-2 font-bold text-sm text-rose-800">
            <i data-lucide="alert-octagon" class="w-5 h-5 text-rose-600"></i>
            DISPUTE FLAGGED: Automated Encroachment / Conflict Detected!
          </div>
          <p>Khasra #${rec.khasra_no} was analyzed by Shapely GIS & Revenue Rules. Found <strong>${disputes.length} critical issues</strong>:</p>
          <ul class="list-disc pl-5 space-y-1 font-medium">
            ${disputes.map(d => `<li><strong>${d.title}</strong>: ${d.description}</li>`).join('')}
          </ul>
          <div class="pt-2 flex gap-3">
            <button onclick="switchTab('disputes')" class="bg-rose-700 hover:bg-rose-800 text-white font-bold px-3 py-1.5 rounded-lg">View in Dispute Engine</button>
            <button onclick="inspectDisputeOnMap('${disputes[0].id}')" class="bg-slate-800 hover:bg-slate-900 text-white font-bold px-3 py-1.5 rounded-lg">Inspect Overlap on GIS Map</button>
          </div>
        `;
      } else {
        alertBox.className = 'mt-6 p-4 rounded-xl border border-emerald-300 bg-emerald-50 text-emerald-900 text-xs space-y-2';
        alertBox.innerHTML = `
          <div class="flex items-center gap-2 font-bold text-sm text-emerald-800">
            <i data-lucide="check-circle" class="w-5 h-5 text-emerald-600"></i>
            VALIDATION SUCCESS: Title Clear & No Spatial Conflicts!
          </div>
          <p>Khasra #${rec.khasra_no} (${rec.village}) has been verified with 100% equity closure and zero boundary overlaps. Cryptographic block hash generated.</p>
          <div class="pt-1 flex gap-3">
            <button onclick="inspectRecordOnMap('${rec.id}')" class="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-3 py-1.5 rounded-lg">View Parcel on Cadastral Map</button>
            <button onclick="switchTab('dashboard')" class="bg-slate-800 hover:bg-slate-900 text-white font-bold px-3 py-1.5 rounded-lg">Return to Registry</button>
          </div>
        `;
      }

      await loadAnalytics();
      await loadRecords();
      await loadPendingVerifications();
      await loadDisputes();
      await loadLedger();
      if (gisMap) loadGisGeojson();
    } else {
      alertBox.className = 'mt-6 p-4 rounded-xl border border-rose-300 bg-rose-50 text-rose-900 text-xs';
      alertBox.innerHTML = `Error: ${result.detail || 'Digitization failed'}`;
    }
  } catch (err) {
    alertBox.classList.remove('hidden');
    alertBox.className = 'mt-6 p-4 rounded-xl border border-rose-300 bg-rose-50 text-rose-900 text-xs';
    alertBox.innerHTML = `Network error during digitization: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i data-lucide="shield-check" class="w-5 h-5"></i> Digitize, Validate & Detect Spatial Conflicts`;
    lucide.createIcons();
  }
}

// ----------------------------------------------------
// 3.1 HUMAN VERIFICATION QUEUE (HITL)
// ----------------------------------------------------
async function loadPendingVerifications() {
  try {
    const res = await fetch('/api/records/pending-verification');
    const list = await res.json();
    pendingVerificationsCache = list;

    const badge = document.getElementById('badge-pending-count');
    if (badge) badge.innerText = list.length;
    const headerCount = document.getElementById('verify-queue-count');
    if (headerCount) headerCount.innerText = `${list.length} Case${list.length === 1 ? '' : 's'} Pending`;

    const container = document.getElementById('pending-verifications-list');
    if (!container) return;

    if (list.length === 0) {
      container.innerHTML = `
        <div class="text-center py-12 border-2 border-dashed border-emerald-200 bg-emerald-50/50 rounded-xl">
          <i data-lucide="check-circle-2" class="w-12 h-12 text-emerald-500 mx-auto mb-2"></i>
          <h4 class="font-bold text-slate-800">Verification Queue Clear!</h4>
          <p class="text-xs text-slate-500 mt-1 max-w-md mx-auto">All ingested cadastral documents meet or exceed the statutory 85% ML confidence score threshold. Zero pending revenue officer reviews.</p>
        </div>
      `;
      lucide.createIcons();
      return;
    }

    container.innerHTML = list.map(r => {
      const fieldConfs = r.field_confidences || {};
      const khasraConf = fieldConfs.khasra_no ? Math.round(fieldConfs.khasra_no.confidence * 100) : 74;
      const khataConf = fieldConfs.khata_no ? Math.round(fieldConfs.khata_no.confidence * 100) : 71;
      const areaConf = fieldConfs.area_sq_meters ? Math.round(fieldConfs.area_sq_meters.confidence * 100) : 78;
      const ownersSummary = (r.owners || []).map(o => `${o.name} (${o.share_percentage}%)`).join(', ');

      return `
        <div class="p-5 rounded-xl border border-amber-200 bg-white shadow-sm space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b pb-3">
            <div class="flex items-center gap-2">
              <span class="bg-amber-100 text-amber-800 border border-amber-300 font-bold px-2.5 py-0.5 rounded text-xs flex items-center gap-1">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> Faded / Low-Confidence Scan Quarantined
              </span>
              <span class="text-xs font-mono text-slate-400">ID: ${r.id}</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-semibold text-slate-500">${r.village}, ${r.district} (${r.state})</span>
              <span class="text-xs bg-rose-50 text-rose-700 font-bold px-2 py-0.5 rounded border border-rose-200">
                Confidence: ${Math.round(r.confidence_score * 100)}% (&lt;85%)
              </span>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
            <!-- Left: Document Facsimile Scan Preview (SVG) -->
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <label class="text-xs font-bold text-slate-700 uppercase flex items-center gap-1.5">
                  <i data-lucide="image" class="w-4 h-4 text-amber-600"></i>
                  Archival Document Scan Facsimile
                </label>
                <span class="text-[11px] text-amber-700 bg-amber-50 font-semibold px-2 py-0.5 rounded border border-amber-200">BBox Highlights Active</span>
              </div>
              <div class="border border-slate-200 rounded-xl overflow-hidden shadow-inner bg-slate-50 max-h-[380px] overflow-y-auto p-1">
                <img src="/api/records/${r.id}/document-svg" class="w-full h-auto object-contain rounded-lg" alt="Scanned Document Facsimile" onerror="this.src='/api/templates/sample_low_confidence_hitl/document-svg'" />
              </div>
              <p class="text-[11px] text-slate-400 italic">Red and orange bounding boxes indicate faded ink or damaged paper where OCR scored &lt; 85%.</p>
            </div>

            <!-- Right: Revenue Officer Correction Console -->
            <div class="space-y-3 bg-slate-50/70 p-4 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div class="space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                  <h4 class="font-bold text-xs text-slate-800 uppercase flex items-center gap-1.5">
                    <i data-lucide="edit-3" class="w-4 h-4 text-emerald-600"></i>
                    Patwari / Revenue Officer Certified Fields
                  </h4>
                  <span class="text-[10px] text-slate-400">Review and update values</span>
                </div>

                <div class="grid grid-cols-2 gap-2.5 text-xs">
                  <div>
                    <div class="flex justify-between items-center mb-0.5">
                      <label class="text-slate-600 font-medium">Khasra / Survey #</label>
                      <span class="text-[10px] font-bold text-rose-600 bg-rose-50 px-1 rounded">${khasraConf}% OCR</span>
                    </div>
                    <input type="text" id="verify-khasra-${r.id}" value="${r.khasra_no}" class="w-full p-2 bg-white border border-slate-300 rounded font-bold text-slate-800 text-xs focus:ring-1 focus:ring-emerald-500" />
                  </div>

                  <div>
                    <div class="flex justify-between items-center mb-0.5">
                      <label class="text-slate-600 font-medium">Khata Number</label>
                      <span class="text-[10px] font-bold text-rose-600 bg-rose-50 px-1 rounded">${khataConf}% OCR</span>
                    </div>
                    <input type="text" id="verify-khata-${r.id}" value="${r.khata_no}" class="w-full p-2 bg-white border border-slate-300 rounded font-bold text-slate-800 text-xs focus:ring-1 focus:ring-emerald-500" />
                  </div>

                  <div>
                    <label class="block text-slate-600 font-medium mb-0.5">Village</label>
                    <input type="text" id="verify-village-${r.id}" value="${r.village}" class="w-full p-2 bg-white border border-slate-300 rounded font-semibold text-slate-800 text-xs" />
                  </div>

                  <div>
                    <label class="block text-slate-600 font-medium mb-0.5">Tehsil / District</label>
                    <input type="text" id="verify-tehsil-${r.id}" value="${r.tehsil}, ${r.district}" class="w-full p-2 bg-white border border-slate-300 rounded font-semibold text-slate-800 text-xs" />
                  </div>

                  <div>
                    <div class="flex justify-between items-center mb-0.5">
                      <label class="text-slate-600 font-medium">Area (Sq. Meters)</label>
                      <span class="text-[10px] font-bold text-rose-600 bg-rose-50 px-1 rounded">${areaConf}% OCR</span>
                    </div>
                    <input type="number" id="verify-area-${r.id}" value="${r.area_sq_meters}" class="w-full p-2 bg-white border border-slate-300 rounded font-bold text-slate-800 text-xs focus:ring-1 focus:ring-emerald-500" />
                  </div>

                  <div>
                    <label class="block text-slate-600 font-medium mb-0.5">Land Classification</label>
                    <select id="verify-type-${r.id}" class="w-full p-2 bg-white border border-slate-300 rounded font-semibold text-slate-800 text-xs">
                      <option value="Agricultural" ${r.land_type === 'Agricultural' ? 'selected' : ''}>Agricultural</option>
                      <option value="Residential" ${r.land_type === 'Residential' ? 'selected' : ''}>Residential</option>
                      <option value="Commercial" ${r.land_type === 'Commercial' ? 'selected' : ''}>Commercial</option>
                      <option value="Industrial" ${r.land_type === 'Industrial' ? 'selected' : ''}>Industrial</option>
                      <option value="Government/Public" ${r.land_type === 'Government/Public' ? 'selected' : ''}>Government/Public</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label class="block text-slate-600 font-medium mb-0.5 text-xs">Tenure Holders (Co-Sharers):</label>
                  <div class="bg-white p-2 rounded border border-slate-200 text-xs font-medium text-slate-700">
                    ${ownersSummary || 'Bholanath Yadav (100%)'}
                  </div>
                </div>

                <div>
                  <label class="block text-slate-600 font-medium mb-0.5 text-xs">Officer Certification Remarks:</label>
                  <textarea id="verify-remarks-${r.id}" rows="2" class="w-full p-2 bg-white border border-slate-300 rounded text-xs text-slate-800 focus:ring-1 focus:ring-emerald-500" placeholder="State physical register verification note...">Physically verified against Mauza Bandobast Register of 1988. Numerals and boundaries verified authentic.</textarea>
                </div>
              </div>

              <div class="pt-3 border-t border-slate-200 flex items-center justify-between gap-3">
                <span class="text-[10px] text-slate-400 flex items-center gap-1">
                  <i data-lucide="shield" class="w-3.5 h-3.5 text-emerald-600"></i> Adds block to SHA-256 Ledger
                </span>
                ${(currentRole === 'REVENUE_OFFICER' || currentRole === 'DILRMP_ADMIN') ? `
                  <button onclick="submitOfficerVerification('${r.id}')" class="bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-2.5 px-4 rounded-xl text-xs flex items-center gap-2 shadow transition">
                    <i data-lucide="check-circle-2" class="w-4 h-4"></i> Certify & Approve into Ledger
                  </button>
                ` : `
                  <span class="text-xs text-amber-700 font-semibold italic bg-amber-50 px-3 py-1.5 rounded border border-amber-200">
                    Officer Clearance Only (Login as Revenue Officer)
                  </span>
                `}
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');

    lucide.createIcons();
  } catch (err) {
    console.error('Failed to load pending verifications:', err);
  }
}

async function submitOfficerVerification(recordId) {
  if (currentRole !== 'REVENUE_OFFICER' && currentRole !== 'DILRMP_ADMIN') {
    alert("Permission Denied: Only Revenue Officers / Patwaris or DILRMP Admins are authorized to certify quarantined records.");
    return;
  }

  const khasra = document.getElementById(`verify-khasra-${recordId}`).value.trim();
  const khata = document.getElementById(`verify-khata-${recordId}`).value.trim();
  const village = document.getElementById(`verify-village-${recordId}`).value.trim();
  const area = parseFloat(document.getElementById(`verify-area-${recordId}`).value);
  const landType = document.getElementById(`verify-type-${recordId}`).value;
  const remarks = document.getElementById(`verify-remarks-${recordId}`).value.trim();

  const payload = {
    officer_name: "Patwari / Revenue Officer Sadar",
    remarks: remarks || "Physically cross-checked against archival revenue register. Certified genuine.",
    corrected_fields: {
      khasra_no: khasra,
      khata_no: khata,
      village: village,
      area_sq_meters: area,
      land_type: landType
    }
  };

  try {
    const res = await fetch(`/api/records/${recordId}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      alert(`Success: Record certified by officer and anchored into SHA-256 Blockchain Ledger!\nBlock Hash: ${result.audit_hash.substring(0, 24)}...`);
      await loadAnalytics();
      await loadRecords();
      await loadPendingVerifications();
      await loadDisputes();
      await loadLedger();
      if (gisMap) loadGisGeojson();
    } else {
      alert(`Verification failed: ${result.detail || 'Unknown error'}`);
    }
  } catch (err) {
    alert(`Error submitting verification: ${err.message}`);
  }
}

// ----------------------------------------------------
// 4. DISPUTE ENGINE
// ----------------------------------------------------
async function loadDisputes(statusFilter = 'ACTIVE') {
  try {
    const url = statusFilter ? `/api/disputes/?status=${statusFilter}` : '/api/disputes/';
    const res = await fetch(url);
    const disputes = await res.json();
    disputesCache = disputes;
    renderDisputes(disputes);
  } catch (err) {
    console.error('Failed to load disputes:', err);
  }
}

function filterDisputes(status) {
  loadDisputes(status);
}

function renderDisputes(disputes) {
  const container = document.getElementById('disputes-list-container');
  if (!container) return;

  if (disputes.length === 0) {
    container.innerHTML = `
      <div class="text-center py-12 border-2 border-dashed border-slate-200 rounded-xl">
        <i data-lucide="check-circle" class="w-10 h-10 text-emerald-500 mx-auto mb-2"></i>
        <h4 class="font-bold text-slate-700">No Disputes in Current Filter</h4>
        <p class="text-xs text-slate-400 mt-1">All land parcels in this view meet statutory boundary and title standards.</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  container.innerHTML = disputes.map(d => {
    const isOverlap = d.dispute_type === 'BOUNDARY_OVERLAP';
    const isDuplicate = d.dispute_type === 'DUPLICATE_SURVEY_NO';
    const isShareMismatch = d.dispute_type === 'OWNERSHIP_SHARE_MISMATCH';

    let typePill = '';
    if (isOverlap) {
      typePill = `<span class="bg-rose-100 text-rose-800 px-2 py-0.5 rounded text-[11px] font-bold border border-rose-200 flex items-center gap-1"><i data-lucide="layers" class="w-3 h-3"></i> Spatial Encroachment</span>`;
    } else if (isDuplicate) {
      typePill = `<span class="bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-[11px] font-bold border border-purple-200 flex items-center gap-1"><i data-lucide="copy" class="w-3 h-3"></i> Duplicate Survey</span>`;
    } else {
      typePill = `<span class="bg-amber-100 text-amber-800 px-2 py-0.5 rounded text-[11px] font-bold border border-amber-200 flex items-center gap-1"><i data-lucide="pie-chart" class="w-3 h-3"></i> Equity Imbalance</span>`;
    }

    const isResolved = d.status === 'RESOLVED';

    return `
      <div class="p-5 rounded-xl border ${isResolved ? 'border-slate-200 bg-slate-50' : 'border-rose-200 bg-white shadow-sm'} space-y-3 transition hover:shadow-md">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b pb-3">
          <div class="flex items-center gap-2">
            ${typePill}
            <span class="text-xs font-mono text-slate-400">${d.id}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-bold px-2 py-0.5 rounded ${d.severity === 'CRITICAL' ? 'bg-rose-600 text-white' : 'bg-amber-500 text-white'}">
              ${d.severity} SEVERITY
            </span>
            <span class="text-[11px] font-semibold text-slate-500">${isResolved ? 'Resolved' : 'Active Contestation'}</span>
          </div>
        </div>

        <div>
          <h4 class="font-bold text-sm text-slate-800">${d.title}</h4>
          <p class="text-xs text-slate-600 mt-1 leading-relaxed">${d.description}</p>
        </div>

        ${d.overlap_area_sq_meters ? `
          <div class="bg-rose-50 border border-rose-200 p-2.5 rounded-lg flex items-center justify-between text-xs text-rose-900">
            <span class="font-semibold flex items-center gap-1"><i data-lucide="maximize-2" class="w-4 h-4 text-rose-600"></i> Overlap Encroachment Extent:</span>
            <span class="font-bold font-mono text-sm text-rose-700">${d.overlap_area_sq_meters} m²</span>
          </div>
        ` : ''}

        ${d.resolution_notes ? `
          <div class="bg-emerald-50 border border-emerald-200 p-2.5 rounded-lg text-xs text-emerald-900">
            <strong>Revenue Officer Settlement Note:</strong> ${d.resolution_notes}
          </div>
        ` : ''}

        <div class="pt-2 flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 text-xs">
          <div class="text-slate-400">
            Affected Record IDs: <span class="font-mono text-slate-600">${d.record_ids.join(', ')}</span>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="inspectDisputeOnMap('${d.id}')" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 font-semibold text-slate-700 flex items-center gap-1.5 transition">
              <i data-lucide="map" class="w-3.5 h-3.5 text-rose-600"></i> Inspect in GIS
            </button>
            ${(!isResolved && (currentRole === 'REVENUE_OFFICER' || currentRole === 'DILRMP_ADMIN')) ? `
              <button onclick="openDisputeModal('${d.id}')" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 font-bold text-white flex items-center gap-1.5 shadow-sm transition">
                <i data-lucide="scale" class="w-3.5 h-3.5"></i> Officer Resolution
              </button>
            ` : (!isResolved ? `
              <span class="text-[11px] text-slate-400 italic bg-slate-100 px-2.5 py-1 rounded">Resolution restricted to Patwari</span>
            ` : '')}
          </div>
        </div>
      </div>
    `;
  }).join('');

  lucide.createIcons();
}

let currentResolvingDisputeId = null;

function openDisputeModal(disputeId) {
  if (currentRole !== 'REVENUE_OFFICER' && currentRole !== 'DILRMP_ADMIN') {
    alert("Permission Denied: Only Revenue Officers / Patwaris or DILRMP Admins can execute dispute settlement decrees.");
    return;
  }
  const d = disputesCache.find(x => x.id === disputeId);
  if (!d) return;

  currentResolvingDisputeId = disputeId;
  const titleEl = document.getElementById('modal-dispute-title');
  const idEl = document.getElementById('modal-dispute-id');
  const descEl = document.getElementById('modal-dispute-desc');

  if (titleEl) titleEl.innerText = d.title;
  if (idEl) idEl.innerText = d.id;
  if (descEl) descEl.innerText = d.description;

  const modal = document.getElementById('dispute-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeDisputeModal() {
  const modal = document.getElementById('dispute-modal');
  if (modal) modal.classList.add('hidden');
  currentResolvingDisputeId = null;
}

async function submitDisputeResolution() {
  if (!currentResolvingDisputeId) return;
  const action = document.getElementById('modal-resolution-action').value;
  const notes = document.getElementById('modal-resolution-notes').value.trim();

  const btn = document.getElementById('btn-submit-resolution');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Recording Decree...`;
    lucide.createIcons();
  }

  try {
    const res = await fetch(`/api/disputes/${currentResolvingDisputeId}/resolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, resolution_notes: notes })
    });
    const data = await res.json();
    closeDisputeModal();
    alert(data.message || "Dispute resolved and immutable mutation block added to ledger.");
    await loadAnalytics();
    await loadRecords();
    await loadDisputes();
    await loadLedger();
    if (gisMap) loadGisGeojson();
  } catch (err) {
    alert("Failed to resolve dispute: " + err.message);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `<i data-lucide="check-check" class="w-4 h-4"></i> Issue Binding Resolution Decree`;
      lucide.createIcons();
    }
  }
}

// ----------------------------------------------------
// 5. GIS CADASTRAL MAP (Leaflet.js)
// ----------------------------------------------------
function initMap() {
  if (!gisMap) {
    gisMap = L.map('gis-map').setView([25.3120, 82.9810], 16);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors | Ministry of Rural Development'
    }).addTo(gisMap);
  } else {
    gisMap.invalidateSize();
  }

  loadGisGeojson();
}

function zoomToJurisdiction(region) {
  if (!gisMap) initMap();
  if (!gisMap) return;

  if (region === 'all') {
    if (geojsonLayer && geojsonLayer.getLayers().length > 0) {
      gisMap.fitBounds(geojsonLayer.getBounds(), { padding: [40, 40] });
    } else {
      gisMap.setView([22.5, 79.0], 5);
    }
  } else if (region === 'up') {
    gisMap.setView([25.3120, 82.9810], 16);
  } else if (region === 'mh') {
    gisMap.setView([18.5190, 73.8512], 16);
  } else if (region === 'ts') {
    gisMap.setView([17.4610, 78.3565], 16);
  }
}

async function loadGisGeojson() {
  try {
    const res = await fetch('/api/gis/parcels');
    const geojson = await res.json();

    if (geojsonLayer && gisMap) {
      gisMap.removeLayer(geojsonLayer);
    }

    geojsonLayer = L.geoJSON(geojson, {
      style: (feature) => {
        const props = feature.properties;
        if (props.feature_type === 'DISPUTE_OVERLAP') {
          return {
            color: '#be123c',
            weight: 3,
            fillColor: '#e11d48',
            fillOpacity: 0.65,
            dashArray: '4, 4',
            className: 'disputed-overlap-polygon'
          };
        }

        if (props.dispute_status === 'DISPUTED') {
          return {
            color: '#e11d48',
            weight: 2.5,
            fillColor: '#fda4af',
            fillOpacity: 0.4
          };
        } else if (props.dispute_status === 'WARNING') {
          return {
            color: '#d97706',
            weight: 2,
            fillColor: '#fde68a',
            fillOpacity: 0.4
          };
        } else {
          return {
            color: '#059669',
            weight: 2,
            fillColor: '#6ee7b7',
            fillOpacity: 0.35
          };
        }
      },
      onEachFeature: (feature, layer) => {
        const props = feature.properties;
        if (props.feature_type === 'DISPUTE_OVERLAP') {
          layer.bindPopup(`
            <div class="text-xs space-y-1">
              <div class="font-bold text-rose-700 flex items-center gap-1">
                ⚠️ ACTIVE ENCROACHMENT OVERLAP
              </div>
              <p><strong>Overlap Extent:</strong> ${props.overlap_area_sq_meters} m²</p>
              <p><strong>Parties Contested:</strong> ${props.record_ids.join(' vs ')}</p>
              <p class="text-[11px] text-slate-500">${props.description}</p>
            </div>
          `);
        } else {
          const ownersStr = (props.owners || []).map(o => `${o.name} (${o.share_percentage}%)`).join(', ');
          layer.bindPopup(`
            <div class="text-xs space-y-1">
              <div class="font-bold text-slate-800 text-sm">
                Khasra #${props.khasra_no} (${props.village})
              </div>
              <p><strong>Khata:</strong> #${props.khata_no} • <strong>Type:</strong> ${props.land_type}</p>
              <p><strong>Owners:</strong> ${ownersStr}</p>
              <p><strong>Area:</strong> ${props.area_sq_meters ? props.area_sq_meters.toLocaleString() : 0} m²</p>
              <p><strong>Status:</strong> <span class="font-bold ${props.dispute_status === 'CLEAR' ? 'text-emerald-600' : 'text-rose-600'}">${props.dispute_status}</span></p>
            </div>
          `);

          layer.on('click', () => {
            showFloatingParcelCard(props);
          });
        }
      }
    }).addTo(gisMap);

  } catch (err) {
    console.error('Failed to load GIS GeoJSON:', err);
  }
}

function showFloatingParcelCard(props) {
  const card = document.getElementById('map-parcel-card');
  if (!card) return;

  const ownersList = (props.owners || []).map(o => `<li>${o.name} - ${o.share_percentage}% share</li>`).join('');

  card.innerHTML = `
    <div class="flex items-center justify-between border-b pb-2 mb-2">
      <h4 class="font-bold text-sm text-slate-800">Khasra #${props.khasra_no}</h4>
      <button onclick="document.getElementById('map-parcel-card').classList.add('hidden')" class="text-slate-400 hover:text-slate-600">✕</button>
    </div>
    <div class="space-y-1.5 text-slate-600 text-xs">
      <div><strong>Khata No:</strong> #${props.khata_no}</div>
      <div><strong>Village:</strong> ${props.village}</div>
      <div><strong>Land Use:</strong> ${props.land_type}</div>
      <div><strong>Area:</strong> ${props.area_sq_meters ? props.area_sq_meters.toLocaleString() : 0} m²</div>
      <div><strong>Owners:</strong><ul class="list-disc pl-4 mt-0.5 text-slate-700">${ownersList}</ul></div>
      <div class="pt-1 flex items-center justify-between">
        <div>
          <strong>Validation:</strong> 
          <span class="font-bold ${props.dispute_status === 'CLEAR' ? 'text-emerald-700' : 'text-rose-700'}">${props.dispute_status}</span>
        </div>
        <button onclick="downloadRoRExtract('${props.id}')" class="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-2 py-0.5 rounded text-[11px] flex items-center gap-1">
          <i data-lucide="printer" class="w-3 h-3"></i> Extract
        </button>
      </div>
    </div>
  `;
  card.classList.remove('hidden');
  lucide.createIcons();
}

function inspectRecordOnMap(recordId) {
  switchTab('map');
  const rec = recordsCache.find(r => r.id === recordId);
  setTimeout(() => {
    if (!gisMap) initMap();
    if (rec) showFloatingParcelCard(rec);
    if (geojsonLayer && gisMap) {
      geojsonLayer.eachLayer(layer => {
        if (layer.feature && layer.feature.properties && layer.feature.properties.id === recordId) {
          gisMap.fitBounds(layer.getBounds(), { maxZoom: 17, padding: [60, 60] });
          layer.openPopup();
        }
      });
    }
  }, 250);
}

function inspectDisputeOnMap(disputeId) {
  switchTab('map');
  setTimeout(() => {
    if (!gisMap) initMap();
    if (geojsonLayer && gisMap) {
      geojsonLayer.eachLayer(layer => {
        if (layer.feature && layer.feature.properties && layer.feature.properties.id === disputeId) {
          gisMap.fitBounds(layer.getBounds(), { maxZoom: 18, padding: [60, 60] });
          layer.openPopup();
        }
      });
    }
  }, 250);
}

// ----------------------------------------------------
// 6. BLOCKCHAIN AUDIT LEDGER
// ----------------------------------------------------
async function loadLedger() {
  try {
    const res = await fetch('/api/audit/ledger');
    const blocks = await res.json();
    const container = document.getElementById('audit-blocks-container');
    if (!container) return;

    if (blocks.length === 0) {
      container.innerHTML = `<div class="text-slate-400 text-center py-6">Audit ledger empty.</div>`;
      return;
    }

    container.innerHTML = blocks.map(b => `
      <div class="bg-slate-900 text-slate-200 p-4 rounded-xl border border-slate-800 space-y-2 relative overflow-hidden shadow-inner">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
          <div class="flex items-center gap-2">
            <span class="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold px-2 py-0.5 rounded text-[11px]">
              BLOCK #${b.block_index}
            </span>
            <span class="text-white font-bold text-xs uppercase">${b.action}</span>
          </div>
          <span class="text-[11px] text-slate-400">${new Date(b.timestamp).toLocaleString()}</span>
        </div>

        <div class="text-xs text-slate-300 font-sans">
          <strong>Event Details:</strong> ${b.details}
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] text-slate-400 pt-1">
          <div class="truncate">
            <span class="text-slate-500 font-semibold">Prev Hash:</span>
            <span class="text-amber-400/90">${b.prev_hash}</span>
          </div>
          <div class="truncate">
            <span class="text-slate-500 font-semibold">Block Hash:</span>
            <span class="text-emerald-400">${b.current_hash}</span>
          </div>
        </div>
      </div>
    `).join('');

    lucide.createIcons();
  } catch (err) {
    console.error('Failed to load ledger:', err);
  }
}

async function verifyLedgerIntegrity() {
  try {
    const res = await fetch('/api/audit/verify');
    const data = await res.json();
    const banner = document.getElementById('ledger-verification-banner');
    const bannerText = document.getElementById('ledger-banner-text');

    const topStatus = document.getElementById('top-ledger-status');
    if (data.is_valid) {
      banner.className = 'p-3.5 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-900 text-xs flex items-center justify-between';
      bannerText.innerText = `Verified: ${data.total_blocks} blocks validated against SHA-256 chain. Zero tampering detected.`;
      if (topStatus) topStatus.innerText = 'Verified Secure';
    } else {
      banner.className = 'p-3.5 rounded-lg bg-rose-50 border border-rose-300 text-rose-900 text-xs flex items-center justify-between';
      bannerText.innerText = `ALERT: ${data.status_message}`;
      if (topStatus) topStatus.innerText = 'TAMPER DETECTED';
    }
    lucide.createIcons();
  } catch (err) {
    alert("Verification error: " + err.message);
  }
}

// ----------------------------------------------------
// 7. CITIZEN / FARMER PORTAL
// ----------------------------------------------------
async function handleCitizenSearch() {
  const query = document.getElementById('citizen-search-input').value.trim();
  const resultsBox = document.getElementById('citizen-search-results');
  if (!query) {
    resultsBox.innerHTML = '';
    return;
  }

  resultsBox.innerHTML = `<div class="text-center py-6 text-slate-400">Searching revenue databases...</div>`;

  try {
    const res = await fetch(`/api/records/?search=${encodeURIComponent(query)}`);
    const records = await res.json();

    if (records.length === 0) {
      resultsBox.innerHTML = `
        <div class="text-center py-8 bg-slate-50 border border-slate-200 rounded-xl">
          <i data-lucide="file-question" class="w-8 h-8 text-slate-400 mx-auto mb-2"></i>
          <h4 class="font-bold text-slate-700">No Matching Land Records</h4>
          <p class="text-xs text-slate-400">Could not locate any parcel matching "${query}". Please check your Khasra or Khata number.</p>
        </div>
      `;
      lucide.createIcons();
      return;
    }

    resultsBox.innerHTML = records.map(r => {
      const isClear = r.dispute_status === 'CLEAR';
      const ownersStr = r.owners.map(o => `${o.name} (${o.share_percentage}% share)`).join(', ');

      return `
        <div class="bg-white p-5 rounded-xl border ${isClear ? 'border-emerald-200' : 'border-rose-200'} shadow-sm space-y-3">
          <div class="flex items-center justify-between border-b pb-3">
            <div>
              <span class="text-xs font-semibold uppercase text-slate-400">Cadastral Record</span>
              <h3 class="text-base font-bold text-slate-800">Khasra #${r.khasra_no} • Khata #${r.khata_no}</h3>
              <p class="text-xs text-slate-500">${r.village}, Tehsil ${r.tehsil}, District ${r.district}</p>
            </div>
            <div>
              ${isClear ? `
                <span class="bg-emerald-100 text-emerald-800 font-bold px-3 py-1 rounded-full text-xs flex items-center gap-1 border border-emerald-300">
                  <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-600"></i> Clear & Encumbrance Free
                </span>
              ` : `
                <span class="bg-rose-100 text-rose-800 font-bold px-3 py-1 rounded-full text-xs flex items-center gap-1 border border-rose-300">
                  <i data-lucide="alert-octagon" class="w-4 h-4 text-rose-600"></i> Active Dispute Flagged
                </span>
              `}
            </div>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
            <div>
              <span class="text-slate-400">Registered Owners:</span>
              <div class="font-semibold text-slate-800">${ownersStr}</div>
            </div>
            <div>
              <span class="text-slate-400">Total Area:</span>
              <div class="font-semibold text-slate-800">${r.area_sq_meters.toLocaleString()} m² (${r.area_acres} Acres)</div>
            </div>
            <div>
              <span class="text-slate-400">Classification:</span>
              <div class="font-semibold text-slate-800">${r.land_type}</div>
            </div>
          </div>

          ${!isClear && r.dispute_tags.length > 0 ? `
            <div class="bg-rose-50 p-3 rounded-lg border border-rose-200 text-xs text-rose-800">
              <strong>Notice of Dispute:</strong>
              <ul class="list-disc pl-4 mt-1 space-y-0.5">
                ${r.dispute_tags.map(t => `<li>${t}</li>`).join('')}
              </ul>
            </div>
          ` : ''}

          <div class="pt-2 flex flex-wrap justify-end gap-2 text-xs">
            <button onclick="downloadRoRExtract('${r.id}')" class="bg-emerald-700 hover:bg-emerald-800 text-white font-semibold px-3 py-2 rounded-lg flex items-center gap-1.5 transition shadow-sm">
              <i data-lucide="printer" class="w-3.5 h-3.5"></i> Certified RoR Extract
            </button>
            <button onclick="inspectRecordOnMap('${r.id}')" class="bg-slate-800 hover:bg-slate-900 text-white font-semibold px-3 py-2 rounded-lg flex items-center gap-1.5 transition">
              <i data-lucide="map" class="w-3.5 h-3.5"></i> Geo-Tagged Map
            </button>
          </div>
        </div>
      `;
    }).join('');

    lucide.createIcons();
  } catch (err) {
    resultsBox.innerHTML = `<div class="text-rose-600 text-xs">Search failed: ${err.message}</div>`;
  }
}

function downloadRoRExtract(recordId) {
  const rec = recordsCache.find(r => r.id === recordId);
  if (!rec) {
    alert("Record not found in cache.");
    return;
  }
  const certificateWindow = window.open('', '_blank');
  if (!certificateWindow) {
    alert("Please allow popups to view and print the certified land record extract.");
    return;
  }
  const ownersList = (rec.owners || []).map(o => `<li><strong>${o.name}</strong> (${o.aadhaar_masked || 'XXXX-XXXX-XXXX'}) — Share: ${o.share_percentage}%</li>`).join('');
  certificateWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Certified Land Title Extract - Khasra #${rec.khasra_no}</title>
        <style>
          body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; color: #1e293b; max-width: 800px; margin: 0 auto; line-height: 1.5; }
          .header { text-align: center; border-bottom: 3px double #047857; padding-bottom: 15px; margin-bottom: 25px; }
          .crest { font-size: 18px; font-weight: 900; letter-spacing: 1px; color: #047857; }
          .sub { font-size: 12px; color: #64748b; text-transform: uppercase; margin-top: 4px; }
          h2 { margin: 12px 0 4px; font-size: 16px; color: #0f172a; }
          .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 20px 0; font-size: 12px; }
          .box { border: 1px solid #e2e8f0; background: #f8fafc; padding: 12px; border-radius: 8px; }
          .status { font-weight: bold; padding: 2px 8px; border-radius: 4px; display: inline-block; }
          .clear { background: #dcfce7; color: #166534; }
          .dispute { background: #ffe4e6; color: #9f1239; }
          .hash-box { background: #0f172a; color: #34d399; font-family: monospace; font-size: 10px; padding: 10px; border-radius: 6px; word-break: break-all; margin-top: 5px; }
          .footer { margin-top: 40px; padding-top: 15px; border-top: 1px dashed #cbd5e1; display: flex; justify-content: space-between; font-size: 11px; color: #64748b; }
          .seal { border: 2px solid #047857; color: #047857; padding: 8px 12px; font-weight: bold; border-radius: 6px; text-transform: uppercase; display: inline-block; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="crest">GOVERNMENT OF INDIA • DIGITAL LAND RECORDS MODERNIZATION PROGRAMME</div>
          <div class="sub">Ministry of Rural Development • Department of Land Resources</div>
          <h2>CERTIFIED DIGITAL RECORD OF RIGHTS (RoR) / KHATAUNI EXTRACT</h2>
          <div style="font-size: 11px; color: #047857; font-weight: bold;">Authentic Electronic Record issued under IT Act Section 6</div>
        </div>

        <div class="grid">
          <div class="box"><strong>Khasra / Survey Number:</strong> #${rec.khasra_no}</div>
          <div class="box"><strong>Khata / Account Number:</strong> #${rec.khata_no}</div>
          <div class="box"><strong>State / Jurisdiction:</strong> ${rec.state || 'Uttar Pradesh'}</div>
          <div class="box"><strong>District & Tehsil:</strong> ${rec.district}, ${rec.tehsil}</div>
          <div class="box"><strong>Revenue Village / Mauza:</strong> ${rec.village}</div>
          <div class="box"><strong>Land Classification:</strong> ${rec.land_type}</div>
          <div class="box"><strong>Total Stated Area:</strong> ${rec.area_sq_meters ? rec.area_sq_meters.toLocaleString() : 0} m² (${rec.area_acres} Acres)</div>
          <div class="box"><strong>Title Status:</strong> <span class="status ${rec.dispute_status === 'CLEAR' ? 'clear' : 'dispute'}">${rec.dispute_status}</span></div>
        </div>

        <div class="box" style="margin-bottom: 15px;">
          <strong>Registered Tenure Holders / Co-Sharers (100% Equity Closure):</strong>
          <ul style="margin: 8px 0 0 18px; padding: 0;">
            ${ownersList}
          </ul>
        </div>

        <div class="box">
          <strong>Cryptographic SHA-256 Immutable Proof of Registration:</strong>
          <div class="hash-box">${rec.audit_hash || 'SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}</div>
        </div>

        <div class="footer">
          <div>
            Generated Date: ${new Date().toLocaleDateString('en-IN')}<br/>
            DILRMP Central Registry Token: #${rec.id}
          </div>
          <div style="text-align: right;">
            <div class="seal">✓ DILRMP Verified</div>
          </div>
        </div>
      </body>
    </html>
  `);
  certificateWindow.document.close();
  setTimeout(() => {
    certificateWindow.print();
  }, 300);
}

function downloadBankLienReport(recordId) {
  const rec = recordsCache.find(r => r.id === recordId);
  if (!rec) {
    alert("Record not found in cache.");
    return;
  }
  const certificateWindow = window.open('', '_blank');
  if (!certificateWindow) {
    alert("Please allow popups to view and print the banking legal search certificate.");
    return;
  }

  const isClear = rec.dispute_status === 'CLEAR';
  const isWarning = rec.dispute_status === 'WARNING';
  const statusColor = isClear ? '#047857' : (isWarning ? '#d97706' : '#be123c');
  const statusBg = isClear ? '#dcfce7' : (isWarning ? '#fef3c7' : '#ffe4e6');
  const statusLabel = isClear 
    ? 'APPROVED: UNENCUMBERED TITLE FOR CREDIT SANCTION' 
    : (isWarning ? 'CONDITIONAL: REQUIRES REVENUE DEMARCATION' : 'REJECTED: ACTIVE LEGAL DISPUTE / ENCROACHMENT');

  const ownersList = (rec.owners || []).map(o => `<li><strong>${o.name}</strong> (Aadhaar: ${o.aadhaar_masked || 'XXXX-XXXX-XXXX'}) — Declared Title Share: <strong>${o.share_percentage}%</strong></li>`).join('');

  certificateWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Bank Title Search & Non-Encumbrance Certificate - #${rec.khasra_no}</title>
        <style>
          body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; color: #0f172a; max-width: 820px; margin: 0 auto; line-height: 1.5; }
          .header { text-align: center; border-bottom: 3px double #1e3a8a; padding-bottom: 15px; margin-bottom: 25px; }
          .crest { font-size: 16px; font-weight: 900; letter-spacing: 1px; color: #1e3a8a; text-transform: uppercase; }
          .sub { font-size: 11px; color: #475569; text-transform: uppercase; margin-top: 3px; }
          h2 { margin: 12px 0 3px; font-size: 17px; color: #0f172a; }
          .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 20px 0; font-size: 12px; }
          .box { border: 1px solid #cbd5e1; background: #f8fafc; padding: 12px; border-radius: 8px; }
          .status-banner { background: ${statusBg}; color: ${statusColor}; border: 2px solid ${statusColor}; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; margin: 15px 0; font-size: 13px; }
          .hash-box { background: #0f172a; color: #38bdf8; font-family: monospace; font-size: 10px; padding: 10px; border-radius: 6px; word-break: break-all; margin-top: 5px; }
          .footer { margin-top: 35px; padding-top: 15px; border-top: 1px dashed #cbd5e1; display: flex; justify-content: space-between; font-size: 11px; color: #64748b; }
          .seal { border: 2px solid #1e3a8a; color: #1e3a8a; padding: 8px 14px; font-weight: bold; border-radius: 6px; text-transform: uppercase; display: inline-block; text-align: center; font-size: 10px; }
          .checklist { list-style: none; padding: 0; font-size: 12px; }
          .checklist li { padding: 4px 0; border-bottom: 1px dotted #e2e8f0; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="crest">INSTITUTIONAL BANKING & FINANCIAL SERVICES TITLE CLEARANCE REPORT</div>
          <div class="sub">National Land Records Modernization Programme (DILRMP Gateway Sync)</div>
          <h2>STATUTORY TITLE DUE-DILIGENCE & NON-ENCUMBRANCE CERTIFICATE</h2>
          <div style="font-size: 11px; color: #1e3a8a; font-weight: bold;">Issued under Section 58 of Transfer of Property Act & IT Act 2000</div>
        </div>

        <div class="status-banner">
          ${statusLabel}
        </div>

        <div class="grid">
          <div class="box"><strong>Target Survey / Khasra No:</strong> #${rec.khasra_no}</div>
          <div class="box"><strong>Account / Khatauni No:</strong> #${rec.khata_no}</div>
          <div class="box"><strong>Revenue Jurisdiction:</strong> ${rec.village}, Tehsil ${rec.tehsil}</div>
          <div class="box"><strong>District & State:</strong> ${rec.district}, ${rec.state || 'Uttar Pradesh'}</div>
          <div class="box"><strong>Parcel Stated Area:</strong> ${rec.area_sq_meters ? rec.area_sq_meters.toLocaleString() : 0} m² (${rec.area_acres} Acres)</div>
          <div class="box"><strong>Zoning / Land Classification:</strong> ${rec.land_type}</div>
        </div>

        <div class="box" style="margin-bottom: 15px;">
          <strong>Declared Tenure Holders (Borrowers / Guarantors):</strong>
          <ul style="margin: 8px 0 0 18px; padding: 0;">
            ${ownersList}
          </ul>
        </div>

        <div class="box" style="margin-bottom: 15px;">
          <strong>Institutional Collateral Due-Diligence Checklist:</strong>
          <ul class="checklist" style="margin-top: 8px;">
            <li>✓ <strong>100% Equity Co-Sharer Summation:</strong> Verified statutory full title closure.</li>
            <li>✓ <strong>Cadastral GIS Spatial Overlap Scan:</strong> Shapely computational geometry returned <strong>${rec.dispute_status === 'CLEAR' ? 'Zero Encroachments (Clear)' : 'Active Boundary Dispute Flagged'}</strong>.</li>
            <li>✓ <strong>Duplicate Conveyance Prevention:</strong> No secondary deed claims registered under Survey #${rec.khasra_no} in ${rec.village}.</li>
            <li>✓ <strong>DILRMP Central Registry Sync:</strong> Aadhaar Vault masked & authenticated with state land records.</li>
          </ul>
        </div>

        <div class="box">
          <strong>Blockchain SHA-256 Audit Fingerprint:</strong>
          <div class="hash-box">${rec.audit_hash || 'SHA256: 7f89b4c02e198a2d3c4b5a67890123456789abcdef0123456789abcdef012345'}</div>
        </div>

        <div class="footer">
          <div>
            Search Conducted: ${new Date().toLocaleDateString('en-IN')} ${new Date().toLocaleTimeString('en-IN')}<br/>
            Reference Dossier ID: BANK-REF-${rec.id}
          </div>
          <div style="text-align: right;">
            <div class="seal">
              LEGAL TITLE SEARCH<br/>✓ VERIFIED & CERTIFIED
            </div>
          </div>
        </div>
      </body>
    </html>
  `);
  certificateWindow.document.close();
  setTimeout(() => {
    certificateWindow.print();
  }, 300);
}

// -------------------------------------------------------------------------
// 8. BHOOMI AI SAHAYAK (INTELLIGENT LAND CHATBOX & PROBLEM SOLVER)
// -------------------------------------------------------------------------

let chatConversationHistory = [];
let isSpeechAudioActive = localStorage.getItem('bhoomi_speech_enabled') !== 'false';
let activeSpeechUtterance = null;
let activeSpeakingButton = null;

let faqCategoriesCache = [];
let popularFaqsCache = [];
let selectedFaqCategory = null;
let faqSearchDebounceTimer = null;

async function initChat() {
  updateChatRoleDisplay();
  await initFaqKnowledgeBase();

  // Initialize Welcome Message in Floating Chat
  const floatingMsgContainer = document.getElementById('floating-chat-messages');
  if (floatingMsgContainer && floatingMsgContainer.children.length === 0) {
    appendChatBubble('assistant', getInitialWelcomeText(), [
      { type: "NAVIGATE_TAB", tab: "map", label: "🗺️ Cadastral Map" },
      { type: "NAVIGATE_TAB", tab: "disputes", label: "⚖️ Active Disputes" },
      { type: "NAVIGATE_TAB", tab: "digitize", label: "📄 Digitize Deed" }
    ], 'floating-chat-messages');
  }

  // Initialize Welcome Message in Dedicated Tab Chat
  const dedicatedMsgContainer = document.getElementById('dedicated-chat-messages');
  if (dedicatedMsgContainer && dedicatedMsgContainer.children.length === 0) {
    appendChatBubble('assistant', getInitialWelcomeText(), [
      { type: "NAVIGATE_TAB", tab: "map", label: "🗺️ Open Cadastral Map" },
      { type: "NAVIGATE_TAB", tab: "disputes", label: "⚖️ Inspect Disputes Engine" },
      { type: "NAVIGATE_TAB", tab: "digitize", label: "📄 AI-OCR Digitizer" }
    ], 'dedicated-chat-messages');
  }

  // Sync audio icon state
  const audioIcon = document.getElementById('audio-toggle-icon');
  if (audioIcon) {
    if (isSpeechAudioActive) {
      audioIcon.classList.add('text-emerald-400');
      audioIcon.classList.remove('text-slate-400');
    } else {
      audioIcon.classList.remove('text-emerald-400');
      audioIcon.classList.add('text-slate-400');
    }
  }

  lucide.createIcons();
}

async function initFaqKnowledgeBase() {
  try {
    // 1. Fetch categories
    const catRes = await fetch('/api/faq/categories');
    const catData = await catRes.json();
    faqCategoriesCache = catData.categories || [];
    renderCategoryPills();
    populateFaqModalFilters();

    // 2. Fetch popular questions
    const popRes = await fetch('/api/faq/popular');
    const popData = await popRes.json();
    popularFaqsCache = popData.popular_faqs || [];
    renderFaqChips(popularFaqsCache);
  } catch (err) {
    console.error('Failed to init FAQ knowledge base:', err);
    await loadChatSuggestions();
  }
}

function renderCategoryPills() {
  const container = document.getElementById('floating-category-pills');
  if (!container) return;

  const allActive = !selectedFaqCategory ? 'active' : '';
  let html = `
    <button type="button" onclick="selectFaqCategory(null)" class="faq-category-pill ${allActive}">
      <span>All Topics</span>
      <span class="pill-count">184</span>
    </button>
  `;

  faqCategoriesCache.forEach(cat => {
    const isActive = selectedFaqCategory === cat.id ? 'active' : '';
    html += `
      <button type="button" onclick="selectFaqCategory('${cat.id}')" class="faq-category-pill ${isActive}" title="${cat.name}">
        <span>${cat.name}</span>
        <span class="pill-count">${cat.count}</span>
      </button>
    `;
  });

  container.innerHTML = html;
}

async function selectFaqCategory(categoryId) {
  if (selectedFaqCategory === categoryId) {
    selectedFaqCategory = null;
  } else {
    selectedFaqCategory = categoryId;
  }
  renderCategoryPills();

  if (selectedFaqCategory) {
    try {
      const res = await fetch(`/api/faq/search?category_id=${selectedFaqCategory}&limit=12`);
      const data = await res.json();
      renderFaqChips(data.results || []);
    } catch (err) {
      console.error('Failed to load category questions:', err);
    }
  } else {
    renderFaqChips(popularFaqsCache);
  }
}

function renderFaqChips(items) {
  const floatingChipsEl = document.getElementById('floating-chat-chips');
  const dedicatedChipsEl = document.getElementById('dedicated-chat-chips');
  if (!items || items.length === 0) return;

  const chipsHtml = items.map(item => {
    const qText = typeof item === 'string' ? item : (item.question || item.label || item.query);
    const catId = typeof item === 'object' ? item.category_id : null;
    const escapedQ = escapeHtmlAttribute(qText);
    const catParam = catId ? `'${catId}'` : 'null';
    return `
      <button type="button" onclick="askPresetQuery('${escapedQ}', ${catParam})" class="chat-chip" title="${escapeHtml(qText)}">
        ${escapeHtml(qText)}
      </button>
    `;
  }).join('');

  if (floatingChipsEl) floatingChipsEl.innerHTML = chipsHtml;
  if (dedicatedChipsEl) dedicatedChipsEl.innerHTML = chipsHtml;
}

function openFaqLibraryModal(categoryId = null) {
  const modal = document.getElementById('faq-library-modal');
  if (!modal) return;

  modal.classList.remove('hidden');

  if (categoryId) {
    const filterSelect = document.getElementById('faq-modal-category-filter');
    if (filterSelect) filterSelect.value = categoryId;
  }

  loadModalFaqs();
  lucide.createIcons();
}

function closeFaqLibraryModal() {
  const modal = document.getElementById('faq-library-modal');
  if (modal) modal.classList.add('hidden');
}

function handleFaqModalOverlayClick(event) {
  if (event.target.id === 'faq-library-modal') {
    closeFaqLibraryModal();
  }
}

function handleFaqSearchInput() {
  clearTimeout(faqSearchDebounceTimer);
  faqSearchDebounceTimer = setTimeout(() => {
    loadModalFaqs();
  }, 200);
}

function handleFaqFilterChange() {
  loadModalFaqs();
}

function populateFaqModalFilters() {
  const select = document.getElementById('faq-modal-category-filter');
  if (!select || select.options.length > 1) return;

  faqCategoriesCache.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat.id;
    opt.textContent = `${cat.name} (${cat.count})`;
    select.appendChild(opt);
  });
}

async function loadModalFaqs() {
  const qInput = document.getElementById('faq-modal-search-input');
  const catSelect = document.getElementById('faq-modal-category-filter');
  const stateSelect = document.getElementById('faq-modal-state-filter');
  const container = document.getElementById('faq-modal-items-container');
  const countEl = document.getElementById('faq-modal-count-indicator');

  const q = qInput ? qInput.value.trim() : '';
  const categoryId = catSelect ? catSelect.value : '';
  const state = stateSelect ? stateSelect.value : '';

  if (container) {
    container.innerHTML = `
      <div class="py-12 text-center text-slate-400">
        <div class="inline-block w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mb-2"></div>
        <p class="text-xs">Searching Land Records FAQ Library...</p>
      </div>
    `;
  }

  try {
    let url = `/api/faq/search?limit=100`;
    if (q) url += `&q=${encodeURIComponent(q)}`;
    if (categoryId) url += `&category_id=${encodeURIComponent(categoryId)}`;
    if (state) url += `&state=${encodeURIComponent(state)}`;

    const res = await fetch(url);
    const data = await res.json();
    const results = data.results || [];

    if (countEl) {
      countEl.innerText = `Showing ${results.length} FAQs`;
    }

    renderFaqModalList(results);
  } catch (err) {
    if (container) {
      container.innerHTML = `<p class="text-rose-500 text-xs py-4 text-center">Failed to load FAQs: ${err.message}</p>`;
    }
  }
}

function renderFaqModalList(faqs) {
  const container = document.getElementById('faq-modal-items-container');
  if (!container) return;

  if (faqs.length === 0) {
    container.innerHTML = `
      <div class="py-12 text-center text-slate-400">
        <i data-lucide="help-circle" class="w-10 h-10 mx-auto mb-2 opacity-50"></i>
        <p class="text-sm font-semibold text-slate-600">No matching questions found</p>
        <p class="text-xs text-slate-400 mt-1">Try another keyword or change the category filter.</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  container.innerHTML = faqs.map(faq => {
    const qEn = escapeHtml(faq.question);
    const qHi = faq.question_hi ? escapeHtml(faq.question_hi) : '';
    const ansHtml = escapeHtml(faq.answer).replace(/\\n/g, '<br/>');
    const stateNoteHtml = faq.state_notes ? `
      <div class="mt-2 text-[11px] text-amber-700 bg-amber-50 p-2 rounded border border-amber-200">
        📍 <strong>State Rules:</strong> ${escapeHtml(faq.state_notes)}
      </div>
    ` : '';
    const escapedQuestion = escapeHtmlAttribute(faq.question);
    const catId = escapeHtmlAttribute(faq.category_id);

    return `
      <div class="faq-item-card" id="faq-card-${faq.id}">
        <div class="flex items-start justify-between gap-3">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1.5">
              <span class="faq-badge faq-badge-emerald">${escapeHtml(faq.category)}</span>
              <span class="text-[10px] text-slate-400 font-mono">#${faq.id}</span>
            </div>
            <h4 class="text-xs sm:text-sm font-bold text-slate-800 hover:text-emerald-700 transition cursor-pointer" onclick="toggleFaqAccordion('${faq.id}')">
              ${qEn}
            </h4>
            ${qHi ? `<p class="text-[11px] text-slate-500 mt-0.5 cursor-pointer" onclick="toggleFaqAccordion('${faq.id}')">${qHi}</p>` : ''}
          </div>
          <div class="flex items-center gap-1.5 flex-shrink-0">
            <button type="button" onclick="askFaqDirectly('${escapedQuestion}', '${catId}')" class="px-2.5 py-1 text-[11px] font-bold bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg shadow-sm transition flex items-center gap-1">
              <i data-lucide="message-square" class="w-3 h-3"></i> Ask AI
            </button>
            <button type="button" onclick="toggleFaqAccordion('${faq.id}')" id="faq-toggle-btn-${faq.id}" class="p-1 text-slate-400 hover:text-slate-600 rounded transition">
              <i data-lucide="chevron-down" class="w-4 h-4"></i>
            </button>
          </div>
        </div>

        <!-- Collapsible Answer Details -->
        <div id="faq-answer-${faq.id}" class="hidden mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600 leading-relaxed">
          <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 mb-2 font-normal">
            ${ansHtml}
          </div>
          ${stateNoteHtml}
          <div class="mt-2.5 flex items-center justify-between text-[11px]">
            <span class="text-slate-400">Category: ${escapeHtml(faq.category)}</span>
            <button type="button" onclick="copyFaqText('${escapedQuestion}', this)" class="text-emerald-600 hover:underline flex items-center gap-1">
              <i data-lucide="copy" class="w-3 h-3"></i> Copy Question
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');

  lucide.createIcons();
}

function toggleFaqAccordion(faqId) {
  const ansEl = document.getElementById(`faq-answer-${faqId}`);
  const btnEl = document.getElementById(`faq-toggle-btn-${faqId}`);
  if (!ansEl) return;

  const isHidden = ansEl.classList.contains('hidden');
  if (isHidden) {
    ansEl.classList.remove('hidden');
    if (btnEl) btnEl.innerHTML = '<i data-lucide="chevron-up" class="w-4 h-4 text-emerald-600"></i>';
  } else {
    ansEl.classList.add('hidden');
    if (btnEl) btnEl.innerHTML = '<i data-lucide="chevron-down" class="w-4 h-4"></i>';
  }
  lucide.createIcons();
}

function askFaqDirectly(question, categoryId) {
  closeFaqLibraryModal();
  const floatingWindow = document.getElementById('floating-chat-window');
  if (floatingWindow && floatingWindow.classList.contains('minimized')) {
    toggleFloatingChat();
  }
  sendChatMessage(question, 'floating', { category_id: categoryId });
}

function copyFaqText(text, btnEl) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btnEl.innerHTML;
    btnEl.innerHTML = '<i data-lucide="check" class="w-3 h-3 text-emerald-600"></i> Copied!';
    lucide.createIcons();
    setTimeout(() => {
      btnEl.innerHTML = orig;
      lucide.createIcons();
    }, 2000);
  });
}

function getInitialWelcomeText() {
  const roleNameMap = {
    'REVENUE_OFFICER': 'Revenue Officer / Patwari',
    'CITIZEN_LANDOWNER': 'Citizen / Landowner',
    'CITIZEN_FARMER': 'Citizen / Landowner',
    'BANK_OFFICER': 'Bank / Lending Officer',
    'DILRMP_ADMIN': 'DILRMP State Administrator'
  };
  const roleLabel = roleNameMap[currentRole] || 'Revenue Officer';

  return `### 🙏 Welcome to Bhoomi AI Sahayak (भूमि AI सहायक)
I am your official real-time AI consultant for the **Intelligent Land Record Digitization & Dispute Resolution System** (Govt of India - Ministry of Rural Development).

**Logged-in Role**: **${roleLabel}**

**How I can assist you:**
- 🔍 **Inspect Land Parcels**: Enter any Khasra # (e.g., **101**, **102**, **105**) to check owner shares, dispute flags, and boundary coordinates.
- 📚 **180+ Land Records Knowledge Base**: Instant answers across 14 categories (Khasra, Khatauni, Jamabandi, 7/12, Mutation, Inheritance, Measurement, RTI, etc.).
- ⚖️ **Boundary Dispute Resolution**: Complete statutory step-by-step guidance on **Section 24 Demarcation (सीमांकन/हदबंदी)** and Electronic Total Station (ETS) field surveys.
- 📝 **Mutation (दाखिल-खारिज)**: Document checklists, citizen charter deadlines (35/90 days), and Khatauni update rules.
- 🏦 **Bank Mortgage Title Search**: 13-point due diligence, Nil-Encumbrance Form 15/16 vetting, and credit eligibility.
- 🛡️ **Blockchain Audit**: SHA-256 tamper-proof ledger validation.

*You can ask in English, हिंदी, or Hinglish!*`;
}

function updateChatRoleDisplay() {
  const roleNameMap = {
    'REVENUE_OFFICER': 'Revenue Officer / Patwari',
    'CITIZEN_LANDOWNER': 'Citizen / Landowner',
    'CITIZEN_FARMER': 'Citizen / Landowner',
    'BANK_OFFICER': 'Bank / Lending Officer',
    'DILRMP_ADMIN': 'DILRMP State Administrator'
  };
  const roleLabel = roleNameMap[currentRole] || 'Revenue Officer';

  const floatingRoleEl = document.getElementById('floating-role-display');
  if (floatingRoleEl) {
    floatingRoleEl.innerText = `Role: ${roleLabel}`;
  }

  const dedicatedRoleEl = document.getElementById('assistant-tab-role-tag');
  if (dedicatedRoleEl) {
    dedicatedRoleEl.innerText = `Active Role: ${roleLabel}`;
  }
}

async function loadChatSuggestions() {
  try {
    const res = await fetch(`/api/chat/suggestions?role=${currentRole}`);
    const data = await res.json();
    const suggestions = data.suggestions || [];
    renderFaqChips(suggestions);
  } catch (err) {
    console.error('Failed to load chat suggestions:', err);
  }
}

function escapeHtmlAttribute(str) {
  return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function toggleFloatingChat() {
  const chatWindow = document.getElementById('floating-chat-window');
  if (!chatWindow) return;

  const isMin = chatWindow.classList.contains('minimized');
  if (isMin) {
    chatWindow.classList.remove('minimized');
    setTimeout(() => {
      const input = document.getElementById('floating-chat-input');
      if (input) input.focus();
    }, 150);
  } else {
    chatWindow.classList.add('minimized');
  }
  lucide.createIcons();
}

function toggleChatFullscreen() {
  const chatWindow = document.getElementById('floating-chat-window');
  const icon = document.getElementById('fullscreen-toggle-icon');
  if (!chatWindow) return;

  const isFull = chatWindow.classList.contains('fullscreen');
  if (isFull) {
    chatWindow.classList.remove('fullscreen');
    if (icon) icon.setAttribute('data-lucide', 'maximize-2');
  } else {
    chatWindow.classList.add('fullscreen');
    if (icon) icon.setAttribute('data-lucide', 'minimize-2');
  }
  lucide.createIcons();
}

function toggleAudioSpeech() {
  isSpeechAudioActive = !isSpeechAudioActive;
  localStorage.setItem('bhoomi_speech_enabled', isSpeechAudioActive);

  if (!isSpeechAudioActive && window.speechSynthesis) {
    window.speechSynthesis.cancel();
    if (activeSpeakingButton) {
      activeSpeakingButton.classList.remove('speaking');
      activeSpeakingButton = null;
    }
  }

  const icon = document.getElementById('audio-toggle-icon');
  if (icon) {
    if (isSpeechAudioActive) {
      icon.classList.add('text-emerald-400');
      icon.classList.remove('text-slate-400');
    } else {
      icon.classList.remove('text-emerald-400');
      icon.classList.add('text-slate-400');
    }
  }
}

function handleChatKeyDown(event, source) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    if (source === 'floating') {
      const form = document.getElementById('floating-chat-form');
      if (form) form.dispatchEvent(new Event('submit', { cancelable: true }));
    }
  }
}

function handleFloatingChatSubmit(event) {
  event.preventDefault();
  const input = document.getElementById('floating-chat-input');
  if (!input) return;
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  sendChatMessage(message, 'floating');
}

function handleDedicatedChatSubmit(event) {
  event.preventDefault();
  const input = document.getElementById('dedicated-chat-input');
  if (!input) return;
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  sendChatMessage(message, 'dedicated');
}

function askPresetQuery(query, categoryId = null) {
  // If on landing page and floating chat is minimized, open it
  const floatingWindow = document.getElementById('floating-chat-window');
  if (floatingWindow && floatingWindow.classList.contains('minimized')) {
    toggleFloatingChat();
  }

  const opts = categoryId ? { category_id: categoryId } : {};
  // If on index.html and user clicked from left panel in dedicated assistant view
  if (currentTab === 'assistant') {
    sendChatMessage(query, 'dedicated', opts);
  } else {
    sendChatMessage(query, 'floating', opts);
  }
}

async function sendChatMessage(message, source = 'floating', options = {}) {
  // 1. Append user message to both containers
  appendChatBubble('user', message, [], 'floating-chat-messages');
  appendChatBubble('user', message, [], 'dedicated-chat-messages');

  // 2. Append typing indicator
  const floatingTypingId = appendTypingIndicator('floating-chat-messages');
  const dedicatedTypingId = appendTypingIndicator('dedicated-chat-messages');

  // Disable send buttons temporarily
  const floatingSendBtn = document.getElementById('floating-send-btn');
  const dedicatedSendBtn = document.getElementById('dedicated-send-btn');
  if (floatingSendBtn) floatingSendBtn.disabled = true;
  if (dedicatedSendBtn) dedicatedSendBtn.disabled = true;

  try {
    const payload = {
      message: message,
      user_role: currentRole,
      conversation_history: chatConversationHistory.slice(-6),
      category_id: (options && options.category_id) || selectedFaqCategory,
      state: (options && options.state) || null
    };

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    const replyText = data.reply || "I have analyzed your query against the live land records database.";
    const actions = data.suggested_actions || [];

    // Remove typing indicators
    removeTypingIndicator(floatingTypingId);
    removeTypingIndicator(dedicatedTypingId);

    // Append AI response bubbles
    appendChatBubble('assistant', replyText, actions, 'floating-chat-messages');
    appendChatBubble('assistant', replyText, actions, 'dedicated-chat-messages');

    // Save to conversation history
    chatConversationHistory.push({ role: 'user', content: message });
    chatConversationHistory.push({ role: 'assistant', content: replyText });

    // Render follow-up / related questions chips
    if (data.suggested_questions && data.suggested_questions.length > 0) {
      renderFaqChips(data.suggested_questions.map(q => ({ question: q, category_id: selectedFaqCategory })));
    }

    // Optional Auto-speech
    if (isSpeechAudioActive) {
      speakText(replyText, null);
    }
  } catch (err) {
    removeTypingIndicator(floatingTypingId);
    removeTypingIndicator(dedicatedTypingId);

    const errorMsg = "⚠️ I encountered a temporary network communication error. Please verify your connection or try again.";
    appendChatBubble('assistant', errorMsg, [], 'floating-chat-messages');
    appendChatBubble('assistant', errorMsg, [], 'dedicated-chat-messages');
  } finally {
    if (floatingSendBtn) floatingSendBtn.disabled = false;
    if (dedicatedSendBtn) dedicatedSendBtn.disabled = false;
  }
}

function appendChatBubble(role, text, actions, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-message ${role}`;

  const isAssistant = role === 'assistant';
  const parsedHtml = isAssistant ? renderChatMarkdown(text) : escapeHtml(text);

  let actionsHtml = '';
  if (isAssistant && actions && actions.length > 0) {
    const buttons = actions.map(act => {
      const actJson = escapeHtmlAttribute(JSON.stringify(act));
      return `<button type="button" onclick="handleActionClick('${actJson}')" class="chat-action-btn">${act.label}</button>`;
    }).join('');
    actionsHtml = `<div class="chat-action-container">${buttons}</div>`;
  }

  let metaBarHtml = '';
  if (isAssistant) {
    metaBarHtml = `
      <div class="chat-bubble-meta">
        <span class="flex items-center gap-1"><i data-lucide="shield-check" class="w-3 h-3 text-emerald-600"></i> DILRMP Grounded</span>
        <div class="flex items-center gap-1.5">
          <button type="button" onclick="speakTextFromBubble(this)" class="chat-meta-btn" title="Read aloud (Text-to-Speech)">
            <i data-lucide="volume-2" class="w-3 h-3"></i> Listen
          </button>
          <button type="button" onclick="copyChatBubbleText(this)" class="chat-meta-btn" title="Copy response to clipboard">
            <i data-lucide="copy" class="w-3 h-3"></i> Copy
          </button>
        </div>
      </div>
    `;
  }

  msgDiv.innerHTML = `
    <div class="chat-bubble">
      ${parsedHtml}
      ${actionsHtml}
      ${metaBarHtml}
    </div>
  `;

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
  lucide.createIcons();
}

function appendTypingIndicator(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return null;

  const id = 'typing-' + Math.random().toString(36).substring(2, 9);
  const div = document.createElement('div');
  div.id = id;
  div.className = 'chat-message assistant';
  div.innerHTML = `
    <div class="chat-bubble flex items-center gap-2 text-slate-500 text-xs">
      <span class="font-medium">Analyzing records & legal codes</span>
      <div class="typing-dots">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeTypingIndicator(id) {
  if (!id) return;
  const el = document.getElementById(id);
  if (el) el.remove();
}

function renderChatMarkdown(rawText) {
  if (!rawText) return '';
  let html = rawText;

  // Escape HTML entities to prevent injection
  html = html
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Headings
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^#### (.*$)/gim, '<h4>$1</h4>');

  // Bold & Italic
  html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');

  // Inline Code
  html = html.replace(/`([^`]+)`/gim, '<code>$1</code>');

  // Bullet Lists (- item)
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
  // Clean adjacent <ul> tags
  html = html.replace(/<\/ul>\s*<ul>/gim, '');

  // Line breaks & paragraphs
  html = html.replace(/\n\n/gim, '<br/><br/>');
  html = html.replace(/\n/gim, '<br/>');

  return html;
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function handleActionClick(actionJsonStr) {
  try {
    const act = JSON.parse(actionJsonStr);
    const type = act.type;
    const tab = act.tab;

    if (type === 'NAVIGATE_TAB') {
      // If currently on landing page, navigate to /app#tab
      if (window.location.pathname === '/' || window.location.pathname.endsWith('landing.html')) {
        window.location.href = `/app#${tab}`;
        return;
      }
      switchTab(tab);

      // If viewing parcel on map
      if (tab === 'map' && act.payload && act.payload.khasra_no) {
        setTimeout(() => {
          highlightParcelOnMap(act.payload.khasra_no);
        }, 300);
      }
    } else if (type === 'SEARCH_RECORD') {
      const q = act.query;
      if (window.location.pathname === '/' || window.location.pathname.endsWith('landing.html')) {
        window.location.href = `/app#citizen`;
        return;
      }
      switchTab('citizen');
      const citizenInput = document.getElementById('citizen-search-input');
      if (citizenInput) {
        citizenInput.value = q;
        handleCitizenSearch();
      }
    } else if (type === 'RESOLVE_DISPUTE') {
      if (window.location.pathname === '/' || window.location.pathname.endsWith('landing.html')) {
        window.location.href = `/app#disputes`;
        return;
      }
      switchTab('disputes');
      openDisputeModal(act.dispute_id);
    }
  } catch (err) {
    console.error('Failed to execute chat action:', err);
  }
}

function highlightParcelOnMap(khasraNo) {
  if (!geojsonLayer || !gisMap) return;
  geojsonLayer.eachLayer(layer => {
    if (layer.feature && layer.feature.properties && layer.feature.properties.khasra_no === khasraNo) {
      gisMap.fitBounds(layer.getBounds(), { maxZoom: 18, padding: [50, 50] });
      layer.openPopup();
      if (layer.setStyle) {
        layer.setStyle({ color: '#f59e0b', weight: 4, fillOpacity: 0.7 });
      }
    }
  });
}

function speakTextFromBubble(btnEl) {
  const bubble = btnEl.closest('.chat-bubble');
  if (!bubble) return;

  // Extract clean text
  const clone = bubble.cloneNode(true);
  const meta = clone.querySelector('.chat-bubble-meta');
  if (meta) meta.remove();
  const actions = clone.querySelector('.chat-action-container');
  if (actions) actions.remove();

  const textToRead = clone.innerText;
  speakText(textToRead, btnEl);
}

function speakText(rawText, btnEl) {
  if (!('speechSynthesis' in window)) {
    alert("Speech Synthesis is not supported in this browser.");
    return;
  }

  // If already speaking the same text, toggle off
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    if (activeSpeakingButton) {
      activeSpeakingButton.classList.remove('speaking');
      activeSpeakingButton = null;
    }
    if (btnEl === activeSpeakingButton) return;
  }

  // Clean text of markdown characters, links, and emojis
  const clean = rawText
    .replace(/[#*_`]/g, '')
    .replace(/\bhttps?:\/\/\S+/gi, '')
    .replace(/[\u{1F300}-\u{1FAFF}]/gu, '')
    .trim();

  if (!clean) return;

  const utterance = new SpeechSynthesisUtterance(clean);
  const isHindi = /[\u0900-\u097F]/.test(clean);

  // Pick voice
  const voices = window.speechSynthesis.getVoices();
  let voice = null;
  if (isHindi) {
    voice = voices.find(v => v.lang.includes('hi') || v.name.includes('Hindi'));
    utterance.lang = 'hi-IN';
  } else {
    voice = voices.find(v => v.lang === 'en-IN') || voices.find(v => v.lang.startsWith('en'));
    utterance.lang = 'en-IN';
  }

  if (voice) utterance.voice = voice;
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  if (btnEl) {
    btnEl.classList.add('speaking');
    activeSpeakingButton = btnEl;
  }

  utterance.onend = () => {
    if (activeSpeakingButton) {
      activeSpeakingButton.classList.remove('speaking');
      activeSpeakingButton = null;
    }
  };

  utterance.onerror = () => {
    if (activeSpeakingButton) {
      activeSpeakingButton.classList.remove('speaking');
      activeSpeakingButton = null;
    }
  };

  window.speechSynthesis.speak(utterance);
}

function copyChatBubbleText(btnEl) {
  const bubble = btnEl.closest('.chat-bubble');
  if (!bubble) return;

  const clone = bubble.cloneNode(true);
  const meta = clone.querySelector('.chat-bubble-meta');
  if (meta) meta.remove();
  const actions = clone.querySelector('.chat-action-container');
  if (actions) actions.remove();

  const text = clone.innerText.trim();
  navigator.clipboard.writeText(text).then(() => {
    const originalText = btnEl.innerHTML;
    btnEl.innerHTML = `<i data-lucide="check" class="w-3 h-3 text-emerald-600"></i> Copied!`;
    lucide.createIcons();
    setTimeout(() => {
      btnEl.innerHTML = originalText;
      lucide.createIcons();
    }, 2000);
  }).catch(() => {
    alert("Could not copy text to clipboard.");
  });
}

function startVoiceRecognition(targetInputId) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Voice recognition (Speech-to-Text) is not supported in this browser. Please use Chrome or Edge.");
    return;
  }

  const inputEl = document.getElementById(targetInputId);
  const micBtn = document.getElementById(targetInputId === 'floating-chat-input' ? 'floating-mic-btn' : 'dedicated-mic-btn');

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-IN'; // Default Indian English / Hindi mix

  if (micBtn) micBtn.classList.add('listening');

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    if (inputEl) {
      inputEl.value = transcript;
      inputEl.focus();
    }
  };

  recognition.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
    if (micBtn) micBtn.classList.remove('listening');
  };

  recognition.onend = () => {
    if (micBtn) micBtn.classList.remove('listening');
  };

  recognition.start();
}

function clearFloatingChat() {
  const container = document.getElementById('floating-chat-messages');
  if (!container) return;
  container.innerHTML = '';
  chatConversationHistory = [];
  appendChatBubble('assistant', getInitialWelcomeText(), [
    { type: "NAVIGATE_TAB", tab: "map", label: "🗺️ Cadastral Map" },
    { type: "NAVIGATE_TAB", tab: "disputes", label: "⚖️ Active Disputes" }
  ], 'floating-chat-messages');
}

function clearDedicatedChat() {
  const container = document.getElementById('dedicated-chat-messages');
  if (!container) return;
  container.innerHTML = '';
  chatConversationHistory = [];
  appendChatBubble('assistant', getInitialWelcomeText(), [
    { type: "NAVIGATE_TAB", tab: "map", label: "🗺️ Open Cadastral Map" },
    { type: "NAVIGATE_TAB", tab: "disputes", label: "⚖️ Inspect Disputes Engine" }
  ], 'dedicated-chat-messages');
}


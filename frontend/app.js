// Land Dispute Manager - Frontend Application Logic

let currentTab = 'dashboard';
let gisMap = null;
let geojsonLayer = null;
let templatesCache = {};
let recordsCache = [];
let disputesCache = [];

document.addEventListener('DOMContentLoaded', async () => {
  await initApp();
});

async function initApp() {
  await loadTemplates();
  await loadAnalytics();
  await loadRecords();
  await loadDisputes();
  await loadLedger();
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
  }

  lucide.createIcons();
}

// ----------------------------------------------------
// 1. ANALYTICS & DASHBOARD
// ----------------------------------------------------
async function loadAnalytics() {
  try {
    const res = await fetch('/api/analytics');
    const data = await res.json();

    document.getElementById('stat-total-records').innerText = data.total_records || 0;
    document.getElementById('stat-total-hectares').innerText = data.total_area_hectares || 0;
    document.getElementById('stat-active-disputes').innerText = data.active_disputes || 0;
    document.getElementById('badge-disputes-count').innerText = data.active_disputes || 0;
    document.getElementById('stat-clear-records').innerText = data.clear_records || 0;

    const clearPct = data.total_records > 0 ? Math.round((data.clear_records / data.total_records) * 100) : 100;
    document.getElementById('stat-clear-pct').innerText = `${clearPct}%`;
    document.getElementById('stat-avg-confidence').innerText = `${data.avg_confidence_score}%`;
  } catch (err) {
    console.error('Failed to load analytics:', err);
  }
}

// ----------------------------------------------------
// 2. RECORDS REGISTRY TABLE
// ----------------------------------------------------
async function loadRecords() {
  try {
    const res = await fetch('/api/records/');
    const records = await res.json();
    recordsCache = records;

    const tbody = document.getElementById('dashboard-records-tbody');
    if (!tbody) return;

    if (records.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="px-4 py-8 text-center text-slate-400">No land records registered yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = records.map(r => {
      let statusBadge = '';
      if (r.dispute_status === 'CLEAR') {
        statusBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800"><i data-lucide="check" class="w-3 h-3"></i> Clear Title</span>`;
      } else if (r.dispute_status === 'WARNING') {
        statusBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800"><i data-lucide="alert-triangle" class="w-3 h-3"></i> Review Needed</span>`;
      } else {
        statusBadge = `<span class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded bg-rose-100 text-rose-800"><i data-lucide="alert-octagon" class="w-3 h-3"></i> Disputed</span>`;
      }

      const ownersSummary = r.owners.map(o => `${o.name} (${o.share_percentage}%)`).join(', ');

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
            <span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-semibold">${r.land_type}</span>
          </td>
          <td class="px-4 py-3 text-slate-700">
            ${r.area_sq_meters.toLocaleString()} m²
            <span class="text-[11px] text-slate-400">(${r.area_acres} ac)</span>
          </td>
          <td class="px-4 py-3">${statusBadge}</td>
          <td class="px-4 py-3 font-semibold text-slate-700">${Math.round(r.confidence_score * 100)}%</td>
          <td class="px-4 py-3 text-right">
            <button onclick="event.stopPropagation(); inspectRecordOnMap('${r.id}')" class="text-xs bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-600 font-semibold px-2.5 py-1 rounded transition">
              GIS View
            </button>
          </td>
        </tr>
      `;
    }).join('');

    lucide.createIcons();
  } catch (err) {
    console.error('Failed to load records:', err);
  }
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
  const tpl = templatesCache[templateId];
  if (!tpl) return;

  document.getElementById('digitize-raw-text').value = tpl.raw_text.trim();
  parseRawText();
}

async function parseRawText() {
  const text = document.getElementById('digitize-raw-text').value;
  if (!text) return;

  // Simple heuristic parser on client to match backend
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

  if (text.includes('102/B')) {
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
  }

  document.getElementById('form-khasra').value = khasra;
  document.getElementById('form-khata').value = khata;
  document.getElementById('form-village').value = village;
  document.getElementById('form-tehsil-dist').value = tehsilDist;
  document.getElementById('form-area').value = area;
  document.getElementById('form-type').value = landType;

  const ownersContainer = document.getElementById('form-owners-container');
  ownersContainer.innerHTML = owners.map((o, idx) => `
    <div class="flex items-center justify-between bg-white p-2 rounded border border-slate-200 text-xs">
      <span class="font-bold text-slate-800">${o.name} <span class="text-slate-400 font-normal">(${o.aadhaar})</span></span>
      <span class="bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded font-bold border border-emerald-200">${o.share}% Share</span>
    </div>
  `).join('');

  lucide.createIcons();
}

async function submitDigitization() {
  const btn = document.getElementById('btn-submit-digitize');
  const alertBox = document.getElementById('digitize-result-alert');
  const rawText = document.getElementById('digitize-raw-text').value;

  btn.disabled = true;
  btn.innerHTML = `<i data-lucide="loader-2" class="w-5 h-5 animate-spin"></i> Processing AI-OCR & Spatial Validation...`;
  lucide.createIcons();

  try {
    const res = await fetch('/api/records/digitize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text: rawText })
    });

    const result = await res.json();
    alertBox.classList.remove('hidden');

    if (result.success) {
      const rec = result.record;
      const disputes = result.disputes_detected || [];

      if (disputes.length > 0) {
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
            <button onclick="switchTab('map')" class="bg-slate-800 hover:bg-slate-900 text-white font-bold px-3 py-1.5 rounded-lg">Inspect Overlap on GIS Map</button>
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
            <button onclick="switchTab('map')" class="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-3 py-1.5 rounded-lg">View Parcel on Cadastral Map</button>
            <button onclick="switchTab('dashboard')" class="bg-slate-800 hover:bg-slate-900 text-white font-bold px-3 py-1.5 rounded-lg">Return to Registry</button>
          </div>
        `;
      }

      await loadAnalytics();
      await loadRecords();
      await loadDisputes();
      await loadLedger();
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
            <button onclick="switchTab('map')" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 font-semibold text-slate-700 flex items-center gap-1.5">
              <i data-lucide="map" class="w-3.5 h-3.5"></i> Inspect in GIS
            </button>
            ${!isResolved ? `
              <button onclick="resolveDisputePrompt('${d.id}')" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 font-bold text-white flex items-center gap-1.5 shadow-sm">
                <i data-lucide="check" class="w-3.5 h-3.5"></i> Officer Resolution
              </button>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  }).join('');

  lucide.createIcons();
}

async function resolveDisputePrompt(disputeId) {
  const notes = prompt("Enter Revenue Officer demarcation / settlement decree notes:", "Resolved pursuant to field survey demarcation and mutually agreed boundary line.");
  if (!notes) return;

  try {
    const res = await fetch(`/api/disputes/${disputeId}/resolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'RESOLVED', resolution_notes: notes })
    });
    const data = await res.json();
    alert(data.message || "Dispute resolved and immutable mutation block added to ledger.");
    await loadAnalytics();
    await loadRecords();
    await loadDisputes();
    await loadLedger();
  } catch (err) {
    alert("Failed to resolve dispute: " + err.message);
  }
}

// ----------------------------------------------------
// 5. GIS CADASTRAL MAP (Leaflet.js)
// ----------------------------------------------------
function initMap() {
  if (!gisMap) {
    // Center at Rampur village coordinates [25.3120, 82.9810]
    gisMap = L.map('gis-map').setView([25.3120, 82.9810], 16);

    // OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors | Ministry of Rural Development'
    }).addTo(gisMap);
  } else {
    gisMap.invalidateSize();
  }

  loadGisGeojson();
}

async function loadGisGeojson() {
  try {
    const res = await fetch('/api/gis/parcels');
    const geojson = await res.json();

    if (geojsonLayer) {
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

    // Zoom bounds to include all parcels
    if (geojson.features.length > 0) {
      gisMap.fitBounds(geojsonLayer.getBounds(), { padding: [30, 30] });
    }
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
      <div class="pt-1">
        <strong>Validation Status:</strong> 
        <span class="font-bold ${props.dispute_status === 'CLEAR' ? 'text-emerald-700' : 'text-rose-700'}">${props.dispute_status}</span>
      </div>
    </div>
  `;
  card.classList.remove('hidden');
}

function inspectRecordOnMap(recordId) {
  switchTab('map');
  const rec = recordsCache.find(r => r.id === recordId);
  if (rec && gisMap) {
    setTimeout(() => {
      showFloatingParcelCard(rec);
    }, 200);
  }
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

    if (data.is_valid) {
      banner.className = 'p-3.5 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-900 text-xs flex items-center justify-between';
      bannerText.innerText = `Verified: ${data.total_blocks} blocks validated against SHA-256 chain. Zero tampering detected.`;
      document.getElementById('top-ledger-status').innerText = 'Verified Secure';
    } else {
      banner.className = 'p-3.5 rounded-lg bg-rose-50 border border-rose-300 text-rose-900 text-xs flex items-center justify-between';
      bannerText.innerText = `ALERT: ${data.status_message}`;
      document.getElementById('top-ledger-status').innerText = 'TAMPER DETECTED';
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

          <div class="pt-2 flex justify-end gap-3 text-xs">
            <button onclick="inspectRecordOnMap('${r.id}')" class="bg-slate-800 hover:bg-slate-900 text-white font-semibold px-4 py-2 rounded-lg flex items-center gap-1.5 transition">
              <i data-lucide="map" class="w-3.5 h-3.5"></i> View Geo-Tagged Parcel Map
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

// Admin Dashboard JS
let diseaseChart, forecastChart, mapInstance;

document.addEventListener('DOMContentLoaded', function() {
  loadAdminStats();
  loadDiseaseChart();
  loadForecastChart();
});

function adminSection(name) {
  document.querySelectorAll('[id^="admin-section-"]').forEach(el => el.style.display = 'none');
  const sec = document.getElementById(`admin-section-${name}`);
  if (sec) sec.style.display = '';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  if (event && event.currentTarget) event.currentTarget.classList.add('active');
  if (name === 'approvals') loadApprovals();
  if (name === 'phcs') loadPHCs();
  if (name === 'disease') loadDiseaseReports();
  if (name === 'outbreak') loadOutbreakPrediction();
  if (name === 'forecast') loadForecastDetails();
  if (name === 'map') initMap();
  if (name === 'digital-twin') loadDigitalTwin(1);
  if (name === 'recommendations') loadRecommendations();
}

async function loadAdminStats() {
  try {
    const res = await fetch('/api/admin/stats');
    const d = await res.json();
    document.getElementById('a-citizens').textContent = d.total_citizens;
    document.getElementById('a-employees').textContent = d.total_employees;
    document.getElementById('a-pending').textContent = d.pending_approvals;
    document.getElementById('a-phcs').textContent = d.total_phcs;
    document.getElementById('a-disease').textContent = d.total_disease_reports;
    document.getElementById('a-camps').textContent = d.health_camps;
  } catch(e) {}
}

async function loadDiseaseChart() {
  try {
    const res = await fetch('/api/charts/disease-trend');
    const d = await res.json();
    const ctx = document.getElementById('disease-chart');
    if (!ctx) return;
    if (diseaseChart) diseaseChart.destroy();
    diseaseChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: d.labels,
        datasets: d.datasets.map(ds => ({
          label: ds.label, data: ds.data, borderColor: ds.color,
          backgroundColor: ds.color + '20', tension: 0.4, fill: true,
          pointBackgroundColor: ds.color, pointRadius: 4
        }))
      },
      options: { responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'top' } },
        scales: { y: { beginAtZero: true } } }
    });
  } catch(e) {}
}

async function loadForecastChart() {
  try {
    const res = await fetch('/api/charts/resource-forecast');
    const d = await res.json();
    const ctx = document.getElementById('forecast-chart');
    if (!ctx) return;
    if (forecastChart) forecastChart.destroy();
    forecastChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: d.labels,
        datasets: [
          { label: 'Predicted Patients', data: d.predicted_patients, backgroundColor: '#3b82f680', borderColor: '#3b82f6', borderWidth: 1.5 },
          { label: 'Bed Demand', data: d.bed_demand, backgroundColor: '#f9731680', borderColor: '#f97316', borderWidth: 1.5 }
        ]
      },
      options: { responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'top' } },
        scales: { y: { beginAtZero: true } } }
    });
  } catch(e) {}
}

async function loadApprovals() {
  try {
    const res = await fetch('/api/admin/pending-employees');
    const employees = await res.json();
    const el = document.getElementById('approvals-list');
    if (!el) return;
    if (!employees.length) {
      el.innerHTML = '<div style="text-align:center;padding:40px;color:#64748b;">✅ No pending approvals</div>';
      return;
    }
    el.innerHTML = `
      <table class="data-table">
        <thead><tr><th>Name</th><th>Email</th><th>Designation</th><th>Center</th><th>District</th><th>Submitted</th><th>Actions</th></tr></thead>
        <tbody>${employees.map(e => `
          <tr>
            <td style="font-weight:600;">${e.name}</td>
            <td>${e.email}</td>
            <td><span style="background:#ede9fe;color:#7c3aed;padding:3px 10px;border-radius:12px;font-size:12px;">${e.designation || 'N/A'}</span></td>
            <td>${e.healthcare_center || 'N/A'}</td>
            <td>${e.district || 'N/A'}</td>
            <td>${e.submitted}</td>
            <td style="display:flex;gap:6px;">
              <button class="btn btn-primary btn-sm" onclick="approveEmployee(${e.id})">✅ Approve</button>
              <button class="btn btn-danger btn-sm" onclick="rejectEmployee(${e.id})">✕ Reject</button>
            </td>
          </tr>`).join('')}
        </tbody>
      </table>`;
  } catch(e) {}
}

async function approveEmployee(id) {
  try {
    const res = await fetch(`/api/admin/approve-employee/${id}`, { method: 'POST' });
    const d = await res.json();
    showToast('✅ Employee approved!', 'success');
    loadApprovals();
    loadAdminStats();
  } catch(e) { showToast('Error approving employee', 'error'); }
}

async function rejectEmployee(id) {
  if (!confirm('Reject this employee registration?')) return;
  try {
    const res = await fetch(`/api/admin/reject-employee/${id}`, { method: 'POST' });
    showToast('Employee rejected', 'warning');
    loadApprovals();
  } catch(e) {}
}

async function loadPHCs() {
  try {
    const res = await fetch('/api/admin/phcs');
    const phcs = await res.json();
    const el = document.getElementById('phcs-grid');
    if (!el) return;
    el.innerHTML = phcs.map(p => {
      const scoreColor = p.health_score >= 75 ? '#16a34a' : p.health_score >= 50 ? '#eab308' : p.health_score >= 30 ? '#f97316' : '#ef4444';
      const bedPct = p.beds > 0 ? Math.round((p.beds - p.available_beds) / p.beds * 100) : 0;
      return `<div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">
          <div><div style="font-weight:700;font-size:15px;">${p.name}</div>
          <div style="font-size:12px;color:#64748b;">${p.village}, ${p.district}</div></div>
          <div style="font-size:22px;font-weight:800;color:${scoreColor};">${p.health_score}</div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px;">
          <div>👨‍⚕️ Doctors: <b>${p.doctors}</b></div>
          <div>👩‍⚕️ Nurses: <b>${p.nurses}</b></div>
          <div>🛏️ Beds: <b>${p.available_beds}/${p.beds}</b></div>
          <div>💊 Stock: <b>${p.medicine_stock}%</b></div>
        </div>
        <div style="margin-top:12px;">
          <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;">
            <span>Bed Occupancy</span><span>${bedPct}%</span>
          </div>
          <div class="progress-bar"><div class="progress-fill ${bedPct > 80 ? 'red' : bedPct > 60 ? 'yellow' : 'green'}" style="width:${bedPct}%"></div></div>
        </div>
        <div style="margin-top:10px;">
          <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;">
            <span>Medicine Stock</span><span>${p.medicine_stock}%</span>
          </div>
          <div class="progress-bar"><div class="progress-fill ${p.medicine_stock < 40 ? 'red' : p.medicine_stock < 60 ? 'yellow' : 'green'}" style="width:${p.medicine_stock}%"></div></div>
        </div>
        <button class="btn btn-secondary btn-sm btn-full" style="margin-top:12px;" onclick="loadDigitalTwin(${p.id});adminSection('digital-twin')">🔬 View Digital Twin</button>
      </div>`;
    }).join('');
  } catch(e) {}
}

async function loadDiseaseReports() {
  try {
    const res = await fetch('/api/admin/disease-reports');
    const reports = await res.json();
    const tbody = document.getElementById('disease-table');
    if (!tbody) return;
    tbody.innerHTML = reports.map(r => `
      <tr>
        <td style="font-weight:600;">${r.disease}</td>
        <td><b>${r.cases}</b></td>
        <td>${r.village}</td>
        <td>${r.district}</td>
        <td>${riskBadge(r.risk_level)}</td>
        <td>${r.date}</td>
      </tr>`).join('');
  } catch(e) {}
}

async function loadOutbreakPrediction() {
  try {
    const res = await fetch('/api/ai/outbreak-prediction');
    const d = await res.json();
    const el = document.getElementById('outbreak-cards');
    if (!el) return;
    el.innerHTML = d.predictions.map(p => `
      <div class="card" style="border-top:4px solid ${p.risk_level==='critical'?'#ef4444':p.risk_level==='high'?'#f97316':'#eab308'};">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
          <div>
            <div style="font-size:18px;font-weight:800;">${p.disease}</div>
            <div style="font-size:13px;color:#64748b;">${p.total_cases} active cases</div>
          </div>
          ${riskBadge(p.risk_level)}
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:13px;margin-bottom:12px;">
          <div style="background:#f8fafc;border-radius:8px;padding:10px;">
            <div style="color:#64748b;font-size:11px;">Outbreak Probability</div>
            <div style="font-size:20px;font-weight:800;color:${p.outbreak_probability > 0.7 ? '#ef4444' : '#f97316'};">${Math.round(p.outbreak_probability * 100)}%</div>
          </div>
          <div style="background:#f8fafc;border-radius:8px;padding:10px;">
            <div style="color:#64748b;font-size:11px;">AI Confidence</div>
            <div style="font-size:20px;font-weight:800;color:#16a34a;">${Math.round(p.confidence * 100)}%</div>
          </div>
          <div style="background:#f8fafc;border-radius:8px;padding:10px;">
            <div style="color:#64748b;font-size:11px;">Predicted 7d Cases</div>
            <div style="font-size:18px;font-weight:700;">${p.predicted_cases_7d}</div>
          </div>
          <div style="background:#f8fafc;border-radius:8px;padding:10px;">
            <div style="color:#64748b;font-size:11px;">Days to Peak</div>
            <div style="font-size:18px;font-weight:700;">${p.days_to_peak} days</div>
          </div>
        </div>
        <div style="background:#fff7ed;border-radius:8px;padding:12px;">
          <div style="font-size:12px;font-weight:700;color:#ea580c;margin-bottom:6px;">🤖 Why AI Predicts This:</div>
          ${p.explanation.map(e => `<div style="font-size:12px;color:#64748b;margin-bottom:3px;">• ${e}</div>`).join('')}
        </div>
        <div style="display:flex;gap:8px;margin-top:12px;font-size:12px;flex-wrap:wrap;">
          <span>💊 Medicines: <b>${p.estimated_medicine_demand}</b></span>
          <span>🛏️ Beds: <b>${p.estimated_beds}</b></span>
          <span>👨‍⚕️ Doctors: <b>${p.estimated_doctors}</b></span>
        </div>
      </div>`).join('');
  } catch(e) {}
}

async function loadForecastDetails() {
  try {
    const res = await fetch('/api/ai/demand-forecast');
    const d = await res.json();
    const el = document.getElementById('forecast-details');
    if (!el) return;
    const alertColors = { warning: '#ffedd5', info: '#dbeafe', alert: '#fee2e2' };
    el.innerHTML = `
      <div style="display:flex;gap:12px;margin-bottom:18px;flex-wrap:wrap;">
        ${d.top_alerts.map(a => `<div style="flex:1;background:${alertColors[a.type]||'#f8fafc'};border-radius:10px;padding:12px;font-size:13px;min-width:200px;">${a.message}</div>`).join('')}
      </div>
      <div class="card">
        <div class="card-title">7-Day Demand Forecast</div>
        <table class="data-table">
          <thead><tr><th>Day</th><th>Patients</th><th>Beds Needed</th><th>ORS</th><th>Malaria Kits</th><th>Doctors</th><th>Confidence</th></tr></thead>
          <tbody>
            ${d.forecast.map(f => `<tr>
              <td><b>${f.date}</b><br><span style="font-size:11px;color:#64748b;">${f.day}</span></td>
              <td><b>${f.predicted_patients}</b></td>
              <td>${f.bed_demand}</td>
              <td>${f.ors_demand}</td>
              <td>${f.malaria_kit_demand}</td>
              <td>${f.doctor_requirement}</td>
              <td><span style="color:#16a34a;font-weight:600;">${Math.round(f.confidence * 100)}%</span></td>
            </tr>`).join('')}
          </tbody>
        </table>
      </div>`;
  } catch(e) {}
}

function initMap() {
  if (mapInstance) { setTimeout(() => mapInstance.invalidateSize(), 100); return; }
  mapInstance = L.map('phc-map').setView([20.5937, 78.9629], 5); // Centre of India
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors', maxZoom: 18
  }).addTo(mapInstance);
  loadMapPHCs();
  // Populate state filter
  fetch('/api/india/states').then(r => r.json()).then(states => {
    const sel = document.getElementById('map-state-filter');
    if (!sel) return;
    states.forEach(s => { const o = document.createElement('option'); o.value = s; o.textContent = s; sel.appendChild(o); });
  });
}

function handleStateChange(state) {
  // Reset district filter
  const districtSel = document.getElementById('map-district-filter');
  if (districtSel) {
    districtSel.innerHTML = '<option value="">All Districts</option>';
  }
  // Filter by state
  filterMapByState(state);
  // If state selected, populate district filter with unique districts from that state's PHCs
  if (state) {
    const phcs = window._allPHCs || [];
    const districts = [...new Set(phcs.filter(p => p.state === state).map(p => p.district))].sort();
    if (districtSel) {
      districts.forEach(d => {
        if (d) {
          const o = document.createElement('option');
          o.value = d;
          o.textContent = d;
          districtSel.appendChild(o);
        }
      });
    }
  }
}

let allMapMarkers = [];

async function loadMapPHCs() {
  try {
    const res = await fetch('/api/map/phc-locations');
    const phcs = await res.json();
    window._allPHCs = phcs;
    renderMapMarkers(phcs);
    const countEl = document.getElementById('map-phc-count');
    if (countEl) countEl.textContent = `Showing ${phcs.length} PHC/CHC locations across India`;
  } catch(e) { console.log('Map error:', e); }
}

function renderMapMarkers(phcs) {
  // Remove old markers
  allMapMarkers.forEach(m => m.remove());
  allMapMarkers = [];
  const colors = { good: '#16a34a', medium: '#eab308', high: '#f97316', critical: '#ef4444' };
  phcs.forEach(p => {
    if (!p.lat || !p.lng) return;
    const color = colors[p.risk] || '#16a34a';
    const score = p.health_score;
    const scoreColor = score >= 75 ? '#16a34a' : score >= 50 ? '#eab308' : score >= 30 ? '#f97316' : '#ef4444';
    const marker = L.circleMarker([p.lat, p.lng], {
      radius: p.health_score >= 75 ? 9 : p.health_score >= 50 ? 10 : 12,
      fillColor: color, color: 'white', weight: 2, opacity: 1, fillOpacity: 0.9
    }).addTo(mapInstance);
    marker.bindPopup(`
      <div style="min-width:220px;font-family:sans-serif;">
        <div style="font-weight:800;font-size:14px;margin-bottom:4px;color:#0f172a;">${p.name}</div>
        <div style="font-size:12px;color:#64748b;margin-bottom:8px;">📍 ${p.district}, ${p.state}</div>
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
          <span style="font-size:12px;font-weight:600;color:${scoreColor};">Health Score: ${p.health_score}/100</span>
          <span style="background:${color}20;color:${color};padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700;">${p.risk.toUpperCase()}</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:12px;background:#f8fafc;border-radius:6px;padding:8px;">
          <div>👨‍⚕️ Doctors: <b>${p.doctors}</b></div>
          <div>🛏️ Beds: <b>${p.available_beds}/${p.beds}</b></div>
          <div>💊 Stock: <b>${p.medicine_stock}%</b></div>
          <div>📊 Score: <b>${p.health_score}</b></div>
        </div>
      </div>`);
    allMapMarkers.push(marker);
  });
}

function filterMapByState(state) {
  const phcs = window._allPHCs || [];
  const district = document.getElementById('map-district-filter')?.value || '';
  let filtered = phcs;
  if (state) filtered = filtered.filter(p => p.state === state);
  if (district) filtered = filtered.filter(p => p.district === district);
  renderMapMarkers(filtered);
  const countEl = document.getElementById('map-phc-count');
  let label = ' across India';
  if (state && district) label = ` in ${district}, ${state}`;
  else if (state) label = ` in ${state}`;
  else if (district) label = ` in ${district}`;
  if (countEl) countEl.textContent = `Showing ${filtered.length} PHC/CHC locations${label}`;
  if (filtered.length > 0 && filtered[0].lat) {
    mapInstance.setView([filtered[0].lat, filtered[0].lng], state ? 7 : 5);
  }
}

function filterMapByDistrict(district) {
  const phcs = window._allPHCs || [];
  const state = document.getElementById('map-state-filter')?.value || '';
  let filtered = phcs;
  if (state) filtered = filtered.filter(p => p.state === state);
  if (district) filtered = filtered.filter(p => p.district === district);
  renderMapMarkers(filtered);
  const countEl = document.getElementById('map-phc-count');
  let label = ' across India';
  if (state && district) label = ` in ${district}, ${state}`;
  else if (state) label = ` in ${state}`;
  else if (district) label = ` in ${district}`;
  if (countEl) countEl.textContent = `Showing ${filtered.length} PHC/CHC locations${label}`;
  if (filtered.length > 0 && filtered[0].lat) {
    mapInstance.setView([filtered[0].lat, filtered[0].lng], state ? 7 : 5);
  }
}

async function loadDigitalTwin(id) {
  try {
    const res = await fetch(`/api/ai/digital-twin/${id}`);
    const d = await res.json();
    const el = document.getElementById('digital-twin-data');
    if (!el) return;
    const s = d.current_status;
    const p = d.predictions;
    const scoreColor = d.phc.health_score >= 75 ? '#16a34a' : d.phc.health_score >= 50 ? '#eab308' : '#ef4444';
    el.innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px;">
        ${[
          ['👥', 'Patients Today', s.patients_today, '#3b82f6'],
          ['⏳', 'Waiting', s.patients_waiting, '#f97316'],
          ['⏱️', 'Avg Wait', s.avg_wait_time, '#8b5cf6'],
          ['🛏️', 'Beds Available', `${s.beds_available}/${s.beds_total}`, '#16a34a'],
        ].map(([icon, label, val, color]) => `
          <div class="card" style="text-align:center;">
            <div style="font-size:24px;margin-bottom:6px;">${icon}</div>
            <div style="font-size:12px;color:#64748b;">${label}</div>
            <div style="font-size:20px;font-weight:800;color:${color};">${val}</div>
          </div>`).join('')}
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:18px;">
        ${[['Next 24h', p.next_24h], ['Next 3 Days', p.next_3d], ['Next 7 Days', p.next_7d]].map(([label, pred]) => `
          <div class="card">
            <div class="card-title" style="font-size:14px;">${label} Prediction</div>
            <div style="font-size:13px;display:flex;flex-direction:column;gap:6px;">
              <div>👥 Expected patients: <b>${pred.expected_patients}</b></div>
              <div>💊 Medicine shortage: ${riskBadge(pred.medicine_shortage_risk.toLowerCase())}</div>
              <div>🛏️ Bed shortage: ${riskBadge(pred.bed_shortage_risk.toLowerCase())}</div>
              <div style="color:#16a34a;font-size:12px;">Confidence: ${Math.round(pred.confidence * 100)}%</div>
            </div>
          </div>`).join('')}
      </div>
      <div class="card">
        <div class="card-title">🚨 Active Alerts</div>
        ${d.alerts.map(a => `<div style="background:${a.level==='critical'?'#fee2e2':a.level==='warning'?'#ffedd5':'#f0fdf4'};border-radius:8px;padding:10px;margin-bottom:8px;font-size:13px;">${a.message}</div>`).join('')}
      </div>`;
  } catch(e) {}
}

async function runSimulation(scenario) {
  const el = document.getElementById('simulation-result');
  if (el) el.innerHTML = '<div style="text-align:center;padding:30px;color:#64748b;">🤖 Running AI simulation...</div>';
  const form = new FormData();
  form.append('scenario', scenario);
  try {
    const res = await fetch('/api/ai/simulate', { method: 'POST', body: form });
    const d = await res.json();
    if (!el) return;
    const alertColors = { Critical: '#ef4444', High: '#f97316', Medium: '#eab308' };
    el.innerHTML = `
      <div class="card" style="border-top:4px solid ${alertColors[d.alert_level]||'#ef4444'};">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
          <div style="font-size:18px;font-weight:800;">${d.scenario}</div>
          <span class="risk-badge risk-${d.alert_level.toLowerCase()}">${d.alert_level} Alert</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
          ${Object.entries(d.predictions).map(([k, v]) => `
            <div style="background:#f8fafc;border-radius:8px;padding:10px;">
              <div style="font-size:12px;color:#64748b;">${k.replace(/_/g,' ').toUpperCase()}</div>
              <div style="font-size:16px;font-weight:700;">${v}</div>
            </div>`).join('')}
        </div>
        <div class="card-title">🎯 Recommended Actions</div>
        ${d.recommended_actions.map(a => `<div style="padding:8px 0;border-bottom:1px solid #e2e8f0;font-size:13px;">✅ ${a}</div>`).join('')}
        <div style="margin-top:12px;font-size:12px;color:#16a34a;font-weight:600;">AI Confidence: ${Math.round(d.confidence * 100)}%</div>
      </div>`;
  } catch(e) {}
}

async function loadRecommendations() {
  try {
    const res = await fetch('/api/ai/recommendations');
    const d = await res.json();
    const el = document.getElementById('recommendations-list');
    if (!el) return;
    const priorityColors = { critical: '#ef4444', high: '#f97316', medium: '#eab308' };
    el.innerHTML = d.recommendations.map(r => `
      <div class="card" style="border-left:4px solid ${priorityColors[r.priority]||'#eab308'};margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
          <div>
            <div style="font-weight:700;font-size:15px;">${r.title}</div>
            <div style="font-size:13px;color:#64748b;margin-top:2px;">${r.description}</div>
          </div>
          <span class="risk-badge risk-${r.priority}">${r.priority.toUpperCase()}</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:12px;margin-bottom:12px;">
          <div style="background:#f8fafc;border-radius:6px;padding:8px;">
            <div style="color:#64748b;">📦 Items</div><div style="font-weight:600;">${r.items}</div>
          </div>
          <div style="background:#f8fafc;border-radius:6px;padding:8px;">
            <div style="color:#64748b;">⏱️ Time</div><div style="font-weight:600;">${r.estimated_time}</div>
          </div>
          <div style="background:#f8fafc;border-radius:6px;padding:8px;">
            <div style="color:#64748b;">❤️ Benefited</div><div style="font-weight:600;">${r.lives_benefited} people</div>
          </div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span style="font-size:13px;color:#16a34a;font-weight:600;">Confidence: ${Math.round(r.confidence * 100)}%</span>
          <button class="btn btn-primary btn-sm">Execute Transfer</button>
        </div>
      </div>`).join('');
  } catch(e) {}
}

// Add disease report form
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('add-report-form');
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const fd = new FormData(this);
      try {
        const res = await fetch('/api/admin/add-disease-report', { method: 'POST', body: fd });
        const d = await res.json();
        if (res.ok) {
          showToast(`Report added. Risk level: ${d.risk_level}`, 'success');
          form.reset();
        } else { showToast('Failed to add report', 'error'); }
      } catch(e) { showToast('Error', 'error'); }
    });
  }
});

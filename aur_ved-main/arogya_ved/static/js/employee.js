// Employee Dashboard JS
document.addEventListener('DOMContentLoaded', function() {
  loadEmpStock();
  loadEmpRecommendations();
  loadStatesForPatient();
  setupPatientForm();
});

function empSection(name) {
  document.querySelectorAll('[id^="emp-section-"]').forEach(el => el.style.display = 'none');
  const sec = document.getElementById(`emp-section-${name}`);
  if (sec) sec.style.display = '';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  if (event && event.currentTarget) event.currentTarget.classList.add('active');
  if (name === 'medicine') loadFullStock();
  if (name === 'ai-recs') loadEmpRecsFull();
  if (name === 'patients') loadPatients();
}

async function loadEmpStock() {
  try {
    const res = await fetch('/api/employee/medicine-stock');
    const stocks = await res.json();
    window._stocks = stocks;
    renderStockOverview(stocks);
    renderFullStock(stocks);
  } catch(e) {}
}

async function reloadStock() {
  const res = await fetch('/api/employee/medicine-stock');
  const stocks = await res.json();
  window._stocks = stocks;
  renderStockOverview(stocks);
  renderFullStock(stocks);
}

function renderStockOverview(stocks) {
  const el = document.getElementById('emp-stock-list');
  if (!el) return;
  const statusColors = { adequate: '#16a34a', moderate: '#eab308', low: '#f97316', critical: '#ef4444' };
  el.innerHTML = stocks.slice(0, 8).map(s => `
    <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid #e2e8f0;">
      <span style="font-size:13.5px;font-weight:500;">${s.medicine}</span>
      <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-weight:700;font-size:14px;">${s.quantity} <span style="font-size:11px;color:#64748b;">${s.unit}</span></span>
        <span style="background:${statusColors[s.status]+'22'};color:${statusColors[s.status]};padding:2px 9px;border-radius:10px;font-size:11px;font-weight:700;">${s.status.toUpperCase()}</span>
      </div>
    </div>`).join('');
}

function renderFullStock(stocks) {
  const el = document.getElementById('full-stock-list');
  if (!el) return;
  const statusColors = { adequate: '#16a34a', moderate: '#eab308', low: '#f97316', critical: '#ef4444' };
  el.innerHTML = stocks.map(s => {
    const max = s.status === 'adequate' ? 100 : s.status === 'moderate' ? 60 : s.status === 'low' ? 35 : 15;
    const pct = Math.min(100, Math.round((s.quantity / (s.quantity > 500 ? s.quantity : 500)) * 100));
    const barColor = s.status === 'adequate' ? 'green' : s.status === 'moderate' ? 'yellow' : 'red';
    return `<div style="margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px;">
        <span style="font-weight:600;">${s.medicine}</span>
        <span style="color:${statusColors[s.status]};font-weight:700;">${s.quantity} ${s.unit}
          <span style="background:${statusColors[s.status]}22;padding:1px 7px;border-radius:8px;font-size:11px;margin-left:4px;">${s.status}</span>
        </span>
      </div>
      <div class="progress-bar"><div class="progress-fill ${barColor}" style="width:${pct}%"></div></div>
    </div>`;
  }).join('') || '<div style="color:#64748b;text-align:center;padding:20px;">No stock data</div>';
}

async function loadFullStock() {
  const stocks = window._stocks || [];
  const el = document.getElementById('full-stock-list');
  if (!el) return;
  const statusColors = { adequate: '#16a34a', moderate: '#eab308', low: '#f97316', critical: '#ef4444' };
  el.innerHTML = stocks.map(s => {
    const pct = Math.min(100, Math.round((s.quantity / (s.quantity > 500 ? s.quantity : 500)) * 100));
    const barColor = s.status === 'adequate' ? 'green' : s.status === 'moderate' ? 'yellow' : 'red';
    return `<div style="margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px;">
        <span style="font-weight:600;">${s.medicine}</span>
        <span style="color:${statusColors[s.status]};font-weight:700;">${s.quantity} ${s.unit}
          <span style="background:${statusColors[s.status]}22;padding:1px 7px;border-radius:8px;font-size:11px;margin-left:4px;">${s.status}</span>
        </span>
      </div>
      <div class="progress-bar"><div class="progress-fill ${barColor}" style="width:${pct}%"></div></div>
    </div>`;
  }).join('') || '<div style="color:#64748b;text-align:center;padding:20px;">No stock data</div>';
}

async function loadEmpRecommendations() {
  try {
    const res = await fetch('/api/ai/recommendations');
    const d = await res.json();
    window._recs = d;
  } catch(e) {}
}

async function loadEmpRecsFull() {
  const d = window._recs;
  const el = document.getElementById('emp-recs-list');
  if (!el || !d) return;
  const priorityColors = { critical: '#ef4444', high: '#f97316', medium: '#eab308' };
  el.innerHTML = d.recommendations.map(r => `
    <div class="card" style="border-left:4px solid ${priorityColors[r.priority]||'#eab308'};margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
        <div style="font-weight:700;font-size:15px;">${r.title}</div>
        <span class="risk-badge risk-${r.priority}">${r.priority.toUpperCase()}</span>
      </div>
      <div style="font-size:13px;color:#64748b;margin-bottom:10px;">${r.description}</div>
      <div style="font-size:13px;margin-bottom:8px;">📦 <b>${r.items}</b></div>
      <div style="font-size:13px;color:#16a34a;font-weight:600;">Confidence: ${Math.round(r.confidence * 100)}%</div>
    </div>`).join('');
}

// Patient functions
async function loadStatesForPatient() {
  try {
    const res = await fetch('/api/india/states');
    const states = await res.json();
    const select = document.getElementById('patient-state-select');
    if (select) {
      select.innerHTML = '<option value="">Select State</option>';
      states.forEach(state => {
        const opt = document.createElement('option');
        opt.value = state;
        opt.textContent = state;
        select.appendChild(opt);
      });
    }
  } catch (e) { console.error(e); }
}

async function loadPatients() {
  try {
    const res = await fetch('/api/employee/patients');
    const patients = await res.json();
    renderPatients(patients);
  } catch (e) { console.error(e); }
}

function renderPatients(patients) {
  const el = document.getElementById('patients-list');
  if (!el) return;
  if (!patients.length) {
    el.innerHTML = '<div style="text-align:center;padding:30px;color:#64748b;">No patients added yet.</div>';
    return;
  }
  el.innerHTML = patients.map(p => `
    <div class="card" style="margin-bottom:12px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
        <div style="font-weight:700;font-size:14px;">${p.name} • ${p.age} yrs</div>
        <span style="background:#dbeafe;color:#1d4ed8;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;">${p.gender}</span>
      </div>
      <div style="font-size:12px;color:#64748b;margin-bottom:6px;">
        ${p.phone ? `📱 ${p.phone}<br>` : ''}
        ${p.disease ? `🏥 ${p.disease}<br>` : ''}
        ${p.medicines.length ? `💊 ${p.medicines.join(', ')}<br>` : ''}
        ${p.village || p.district || p.state ? `📍 ${[p.village, p.district, p.state].filter(x=>x).join(', ')}` : ''}
      </div>
      ${p.prescription_photo ? `
        <div style="margin-top:8px;">
          <a href="/uploads/${p.prescription_photo}" target="_blank" style="color:#16a34a;font-size:12px;text-decoration:none;font-weight:600;">
            📄 View Prescription
          </a>
        </div>` : ''}
    </div>
  `).join('');
}

function setupPatientForm() {
  const form = document.getElementById('patient-form');
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const btn = this.querySelector('button[type="submit"]');
      const origText = btn.textContent;
      btn.textContent = '⏳ Adding...';
      btn.disabled = true;
      try {
        const fd = new FormData(this);
        // Convert medicines to JSON array
        const medStr = fd.get('medicines') || '';
        const medArray = medStr.split(',').map(m => m.trim()).filter(m => m);
        fd.set('medicines', JSON.stringify(medArray));
        const res = await fetch('/api/employee/patients', { method: 'POST', body: fd });
        const d = await res.json();
        if (res.ok) {
          showToast(d.message, 'success');
          this.reset();
          await loadPatients();
        } else {
          showToast('Failed to add patient', 'error');
        }
      } catch (e) { showToast('Error adding patient', 'error'); }
      btn.textContent = origText;
      btn.disabled = false;
    });
  }
}

// Stock form
document.addEventListener('DOMContentLoaded', function() {
  const stockForm = document.getElementById('stock-form');
  if (stockForm) {
    stockForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      const fd = new FormData(this);
      const btn = this.querySelector('button[type=submit]');
      const origText = btn.textContent;
      btn.textContent = '⏳ Updating...';
      btn.disabled = true;
      try {
        const token = localStorage.getItem('token');
        const res = await fetch('/api/employee/update-stock', {
          method: 'POST', body: fd,
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const d = await res.json();
        if (res.ok) {
          showToast(`✅ ${d.message}`, 'success');
          this.reset();
          // Reload stock lists immediately
          await reloadStock();
          // Explicitly re-render both views to ensure they update
          if (window._stocks) {
            renderStockOverview(window._stocks);
            renderFullStock(window._stocks);
          }
        } else {
          showToast(d.detail || 'Failed to update stock', 'error');
        }
      } catch(e) { showToast('Error updating stock', 'error'); }
      btn.textContent = origText;
      btn.disabled = false;
    });
  }

  const diseaseForm = document.getElementById('disease-report-form');
  if (diseaseForm) {
    diseaseForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      const fd = new FormData(this);
      try {
        const token = localStorage.getItem('token');
        const res = await fetch('/api/employee/add-disease-report', {
          method: 'POST', body: fd,
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const d = await res.json();
        if (res.ok) {
          showToast(`✅ Disease report submitted. Risk: ${d.risk_level}`, 'success');
          this.reset();
        } else { showToast('Failed to submit report', 'error'); }
      } catch(e) { showToast('Error', 'error'); }
    });
  }
});

// Citizen Dashboard JS
document.addEventListener('DOMContentLoaded', function() {
  const name = localStorage.getItem('name') || 'Satya Prakash';
  const greet = document.getElementById('greeting');
  if (greet) greet.textContent = `Hello, ${name} 👋`;
  const avatar = document.getElementById('user-avatar');
  if (avatar) avatar.textContent = name.split(' ').map(n => n[0]).join('').substring(0,2).toUpperCase();
  loadProfile();
  loadCamps();
  loadNotifications();
});

function showSection(name) {
  document.querySelectorAll('[id^="section-"]').forEach(el => el.style.display = 'none');
  const sec = document.getElementById(`section-${name}`);
  if (sec) sec.style.display = '';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  event && event.currentTarget && event.currentTarget.classList.add('active');
  if (name === 'myhealth') loadProfileSection();
  if (name === 'camps') loadAllCamps();
  if (name === 'reminders') loadAllReminders();
  if (name === 'notifications') loadAllNotifications();
}

async function loadProfile() {
  try {
    const res = await api('/api/citizen/profile');
    if (!res.ok) return;
    const d = await res.json();
    // Update stats
    const scoreNum = document.getElementById('score-num');
    const statScore = document.getElementById('stat-score');
    const scoreLabel = document.getElementById('stat-score-label');
    const statBmi = document.getElementById('stat-bmi');
    const statConditions = document.getElementById('stat-conditions');
    const statCondList = document.getElementById('stat-cond-list');
    if (scoreNum) scoreNum.textContent = d.health_score;
    if (statScore) statScore.textContent = `${d.health_score}/100`;
    if (scoreLabel) {
      const labels = { 90: 'Excellent', 75: 'Good', 50: 'Moderate', 30: 'At Risk' };
      let label = 'Critical';
      if (d.health_score >= 90) label = 'Excellent';
      else if (d.health_score >= 75) label = 'Good';
      else if (d.health_score >= 50) label = 'Moderate';
      else if (d.health_score >= 30) label = 'At Risk';
      scoreLabel.textContent = label;
    }
    if (statBmi) statBmi.textContent = d.bmi;
    if (statConditions) statConditions.textContent = d.active_conditions || (d.medical_conditions || []).length;
    if (statCondList) statCondList.textContent = (d.medical_conditions || []).join(', ') || 'None';
    // Update health overview
    const bpVal = document.getElementById('bp-val');
    const sugarVal = document.getElementById('sugar-val');
    const weightVal = document.getElementById('weight-val');
    const lastCheckup = document.getElementById('last-checkup');
    const healthBar = document.getElementById('health-bar');
    const healthPct = document.getElementById('health-pct');
    if (bpVal) bpVal.textContent = d.blood_pressure;
    if (sugarVal) sugarVal.textContent = d.blood_sugar;
    if (weightVal) weightVal.textContent = d.weight;
    if (lastCheckup) lastCheckup.textContent = d.last_checkup;
    if (healthBar) healthBar.style.width = `${d.health_score}%`;
    if (healthPct) healthPct.textContent = `${d.health_score}%`;
    window._profile = d;
  } catch(e) { console.log('Profile load:', e); }
}

async function loadProfileSection() {
  const d = window._profile;
  if (!d) { await loadProfile(); return; }
  const fields = { 'p-name': d.name, 'p-age': d.age, 'p-gender': d.gender,
    'p-phone': d.phone, 'p-village': d.village, 'p-district': d.district,
    'p-phc': d.nearest_phc };
  for (const [id, val] of Object.entries(fields)) {
    const el = document.getElementById(id);
    if (el) el.textContent = val || 'Not set';
  }
  const condEl = document.getElementById('p-conditions');
  if (condEl) {
    condEl.innerHTML = (d.medical_conditions || []).map(c =>
      `<span style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:20px;font-size:13px;font-weight:600;">${c}</span>`
    ).join('') || '<span style="color:#64748b;">No conditions recorded</span>';
  }
  const rhs = document.getElementById('risk-health-score');
  const rhb = document.getElementById('risk-health-bar');
  const rds = document.getElementById('risk-disease-score');
  const rdb = document.getElementById('risk-disease-bar');
  if (rhs) rhs.textContent = `${d.health_score}%`;
  if (rhb) rhb.style.width = `${d.health_score}%`;
  if (rds) rds.textContent = `${d.risk_score}%`;
  if (rdb) rdb.style.width = `${d.risk_score}%`;
}

async function loadCamps() {
  try {
    const res = await fetch('/api/citizen/camps');
    const camps = await res.json();
    const campsList = document.getElementById('camps-list');
    if (!campsList) return;
    const icons = { Diabetes: 'diabetes', Eye: 'eye', 'Women Health': 'women' };
    const emojis = { Diabetes: '🩸', Eye: '👁️', 'Women Health': '👩', General: '🏥' };
    campsList.innerHTML = camps.slice(0, 3).map(c => `
      <div class="camp-item">
        <div class="camp-icon ${icons[c.type] || 'general'}">${emojis[c.type] || '🏥'}</div>
        <div>
          <div class="camp-name">${c.name}</div>
          <div class="camp-loc">${c.location} <span style="color: #16a34a; font-weight: 500;">(${c.distance_km} km away)</span></div>
        </div>
        <div class="camp-date">${fmtDate(c.date)}</div>
      </div>`).join('');
    window._camps = camps;
    // Update the main dashboard Book button to use real first camp id
    if (camps.length > 0) {
      const bookBtn = document.getElementById('book-btn');
      if (bookBtn) bookBtn.setAttribute('onclick', `bookAppointment(${camps[0].id})`);
    }
  } catch(e) {}
}

async function loadAllCamps() {
  const camps = window._camps || [];
  const el = document.getElementById('all-camps');
  if (!el) return;
  const emojis = { Diabetes: '🩸', Eye: '👁️', 'Women Health': '👩', General: '🏥' };
  el.innerHTML = camps.map(c => `
    <div class="card">
      <div style="font-size:28px;margin-bottom:10px;">${emojis[c.type] || '🏥'}</div>
      <div style="font-weight:700;font-size:15px;margin-bottom:6px;">${c.name}</div>
      <div style="font-size:13px;color:#64748b;margin-bottom:4px;">📍 ${c.location} <span style="color: #16a34a; font-weight: 500;">(${c.distance_km} km away)</span></div>
      <div style="font-size:13px;color:#64748b;margin-bottom:4px;">📅 ${fmtDate(c.date)}</div>
      <div style="font-size:13px;color:#64748b;margin-bottom:14px;">🕐 ${c.time}</div>
      <div style="font-size:12px;color:#64748b;margin-bottom:12px;">Organizer: ${c.organizer}</div>
      <button class="btn btn-primary btn-sm btn-full" onclick="bookAppointment(${c.id})">Book Appointment</button>
    </div>`).join('') || '<div style="color:#64748b;text-align:center;padding:30px;">No camps available</div>';
}

async function loadAllReminders() {
  try {
    const res = await fetch('/api/citizen/reminders');
    const reminders = await res.json();
    const el = document.getElementById('all-reminders');
    if (!el) return;
    el.innerHTML = reminders.map(r => `
      <div class="card" style="border-left:4px solid ${r.priority==='high'?'#ef4444':'#f97316'};">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
          <span style="font-size:24px;">${r.icon}</span>
          <div><div style="font-weight:700;font-size:15px;">${r.disease}</div>
          <span class="${r.priority==='high'?'risk-high':'risk-medium'} risk-badge">${r.priority.toUpperCase()}</span></div>
        </div>
        <p style="font-size:14px;color:#64748b;margin-bottom:12px;">${r.message}</p>
        <div style="font-size:13px;color:#64748b;margin-bottom:4px;">📍 ${r.location}</div>
        <div style="font-size:13px;color:#64748b;margin-bottom:14px;">📅 ${r.date}</div>
        ${r.camp_id ? `<button class="btn btn-primary" onclick="bookAppointment(${r.camp_id})">Book Now</button>` : ''}
      </div>`).join('');
  } catch(e) {}
}

async function loadNotifications() {
  try {
    const res = await api('/api/citizen/notifications');
    if (!res.ok) return;
    const notifs = await res.json();
    const el = document.getElementById('notif-list');
    if (!el) return;
    const count = document.getElementById('notif-count');
    if (count) count.textContent = notifs.filter(n => !n.read).length;
    el.innerHTML = notifs.slice(0, 5).map(n => `
      <div class="notif-item">
        <div class="notif-dot ${n.priority}"></div>
        <div class="notif-text">${n.title}</div>
        <div class="notif-time">${n.time_ago}</div>
      </div>`).join('') || '<div style="color:#64748b;padding:10px;text-align:center;">No notifications</div>';
    window._notifs = notifs;
  } catch(e) {}
}

async function loadAllNotifications() {
  const notifs = window._notifs || [];
  const el = document.getElementById('all-notifs-list');
  if (!el) return;
  el.innerHTML = notifs.map(n => `
    <div class="notif-item" style="padding:14px 0;">
      <div class="notif-dot ${n.priority}" style="width:10px;height:10px;"></div>
      <div>
        <div style="font-weight:600;font-size:14px;">${n.title}</div>
        <div style="font-size:13px;color:#64748b;margin-top:2px;">${n.message}</div>
      </div>
      <div class="notif-time">${n.time_ago}</div>
    </div>`).join('') || '<div style="text-align:center;padding:30px;color:#64748b;">No notifications</div>';
}

async function bookAppointment(campId) {
  if (!campId) { showToast('No camp selected', 'warning'); return; }
  const btn = event && event.target;
  const origText = btn ? btn.textContent : '';
  if (btn) { btn.textContent = '⏳ Booking...'; btn.disabled = true; }

  const form = new FormData();
  form.append('camp_id', campId);
  try {
    const res = await api('/api/citizen/book-appointment', { method: 'POST', body: form });
    const data = await res.json();
    if (res.ok) {
      if (data.status === 'already_booked') {
        showToast('You already have a booking at this camp!', 'warning');
        if (btn) { btn.textContent = '✅ Already Booked'; btn.style.background = '#0ea5e9'; }
        return;
      }
      // Show success modal
      showBookingSuccess(data);
      // Update the button
      if (btn) { btn.textContent = '✅ Appointment Booked!'; btn.style.background = '#16a34a'; btn.disabled = false; }
      const mainBtn = document.getElementById('book-btn');
      if (mainBtn) { mainBtn.textContent = '✅ Appointment Booked!'; mainBtn.style.background = '#16a34a'; }
    } else {
      showToast(data.detail || 'Booking failed. Please try again.', 'error');
      if (btn) { btn.textContent = origText; btn.disabled = false; }
    }
  } catch(e) {
    showToast('Connection error. Please try again.', 'error');
    if (btn) { btn.textContent = origText; btn.disabled = false; }
  }
}

function showBookingSuccess(data) {
  // Remove existing modal
  const old = document.getElementById('booking-modal');
  if (old) old.remove();

  const modal = document.createElement('div');
  modal.id = 'booking-modal';
  modal.style.cssText = `position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);
    z-index:9999;display:flex;align-items:center;justify-content:center;`;
  modal.innerHTML = `
    <div style="background:white;border-radius:20px;padding:36px;max-width:420px;width:90%;
                box-shadow:0 25px 60px rgba(0,0,0,0.2);text-align:center;animation:slideIn 0.3s ease;">
      <div style="width:70px;height:70px;background:#dcfce7;border-radius:50%;display:flex;
                  align-items:center;justify-content:center;font-size:36px;margin:0 auto 16px;">✅</div>
      <h2 style="font-size:20px;font-weight:800;color:#0f172a;margin-bottom:8px;">Appointment Confirmed!</h2>
      <p style="color:#64748b;font-size:14px;margin-bottom:20px;">Your slot has been successfully booked.</p>
      <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:16px;margin-bottom:20px;text-align:left;">
        <div style="display:flex;flex-direction:column;gap:8px;font-size:14px;">
          <div>🏥 <b>${data.message.replace('Appointment confirmed at ','')}</b></div>
          <div>📍 ${data.location || 'PHC Hanamkonda'}</div>
          <div>📅 ${fmtDate ? fmtDate(data.date) : data.date}</div>
          <div>🕐 ${data.time}</div>
        </div>
      </div>
      <div style="display:flex;gap:10px;justify-content:center;">
        <button onclick="document.getElementById('booking-modal').remove()"
          style="padding:10px 24px;background:#16a34a;color:white;border:none;border-radius:8px;
                 font-weight:700;font-size:14px;cursor:pointer;">Done</button>
        <button onclick="document.getElementById('booking-modal').remove();showSection('appointments')"
          style="padding:10px 24px;background:transparent;color:#16a34a;border:2px solid #16a34a;
                 border-radius:8px;font-weight:700;font-size:14px;cursor:pointer;">View Appointments</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
  modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });
}

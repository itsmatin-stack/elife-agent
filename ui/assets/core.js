// E LIFE Agent — Core JS v2
// Auto-detects: backend available hai toh API use karo, nahi toh localStorage

const GROQ_KEY = localStorage.getItem("elife_groq_key") || "";
const GROQ_MODEL = "llama-3.3-70b-versatile";
const API_BASE = "http://localhost:8000/api";
const SYSTEM_PROMPT = "Tu E LIFE Agent hai — ek smart aur helpful personal AI assistant. Tu Hindi, English aur Hinglish teeno mein baat kar sakta hai. User ki personal aur business life manage karne mein help kar. Short, clear aur useful replies de. Hinglish preferred.";

let USE_API = false;

// ── CHECK BACKEND ─────────────────────
async function checkBackend() {
  try {
    const r = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(2000) });
    USE_API = r.ok;
  } catch { USE_API = false; }
}
checkBackend();

// ── THEME ─────────────────────────────
let dark = localStorage.getItem('elife_theme') === 'dark';
function applyTheme() {
  document.body.classList.toggle('dark', dark);
  const tgl = document.getElementById('tgl');
  const icon = document.getElementById('themeIcon');
  const lbl = document.getElementById('themeLabel');
  if (tgl) tgl.classList.toggle('on', dark);
  if (icon) icon.className = dark ? 'ti ti-sun' : 'ti ti-moon';
  if (lbl) lbl.textContent = dark ? 'Light mode' : 'Dark mode';
}
function toggleTheme() {
  dark = !dark;
  localStorage.setItem('elife_theme', dark ? 'dark' : 'light');
  applyTheme();
}

// ── SIDEBAR ───────────────────────────
let sbOpen = localStorage.getItem('elife_sb') !== 'closed';
function applySidebar() {
  const sb = document.getElementById('sidebar');
  const icon = document.getElementById('toggleIcon');
  if (sb) sb.classList.toggle('collapsed', !sbOpen);
  if (icon) icon.className = sbOpen ? 'ti ti-layout-sidebar' : 'ti ti-layout-sidebar-right';
}
function toggleSidebar() {
  sbOpen = !sbOpen;
  localStorage.setItem('elife_sb', sbOpen ? 'open' : 'closed');
  applySidebar();
}

// ── TOAST ─────────────────────────────
function showToast(msg, type = 'info') {
  let t = document.getElementById('toast');
  if (!t) { t = document.createElement('div'); t.id = 'toast'; t.className = 'toast'; document.body.appendChild(t); }
  t.textContent = msg;
  t.className = `toast ${type} show`;
  setTimeout(() => t.classList.remove('show'), 2800);
}

// ── MODAL ─────────────────────────────
function openModal(id) { document.getElementById(id)?.classList.add('show'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('show'); }

// ── LOCAL STORAGE ─────────────────────
function saveData(key, data) {
  localStorage.setItem('elife_' + key, JSON.stringify(data));
}
function loadData(key, fallback = []) {
  try { return JSON.parse(localStorage.getItem('elife_' + key)) ?? fallback; }
  catch { return fallback; }
}

// ── API HELPER ────────────────────────
async function apiCall(method, path, body = null) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(`${API_BASE}${path}`, opts);
  return r.json();
}

// ── SMART DATA (API first, localStorage fallback) ─────
async function getData(key, apiPath) {
  if (USE_API) {
    try { return await apiCall('GET', apiPath); } catch {}
  }
  return loadData(key, []);
}

async function postData(key, apiPath, item, localData) {
  if (USE_API) {
    try { return await apiCall('POST', apiPath, item); } catch {}
  }
  const newItem = { ...item, id: genId(), created: new Date().toISOString() };
  localData.push(newItem);
  saveData(key, localData);
  return newItem;
}

async function deleteData(key, apiPath, id, localData) {
  if (USE_API) {
    try { await apiCall('DELETE', `${apiPath}/${id}`); return; } catch {}
  }
  const updated = localData.filter(i => i.id !== id);
  saveData(key, updated);
}

// ── GROQ API (direct) ─────────────────
async function groqChat(messages) {
  if (USE_API) {
    try {
      const r = await apiCall('POST', '/chat', { messages, model: GROQ_MODEL });
      return r.reply;
    } catch {}
  }
  return groqChatDirect(messages, GROQ_MODEL);
}

async function groqChatDirect(messages, model = GROQ_MODEL) {
  const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${GROQ_KEY}` },
    body: JSON.stringify({
      model,
      messages: [{ role: 'system', content: SYSTEM_PROMPT }, ...messages],
      max_tokens: 1024,
      temperature: 0.7
    })
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error.message);
  return data.choices[0].message.content;
}

// ── TIME HELPERS ──────────────────────
function timeNow() {
  return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}
function dateNow() {
  return new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}
function formatDate(iso) {
  if (!iso) return '';
  return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

// ── ID GENERATOR ──────────────────────
function genId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

// ── INIT ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  applyTheme();
  applySidebar();
  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);
  document.getElementById('sidebarToggle')?.addEventListener('click', toggleSidebar);
});

// ── REMINDER NOTIFICATIONS ────────────
function checkReminders() {
  if(!('Notification' in window) || Notification.permission !== 'granted') return;
  const reminders = loadData('reminders', []);
  const now = new Date();
  reminders.forEach(r => {
    if(!r.done && r.time) {
      const rt = new Date(r.time);
      const diff = rt - now;
      if(diff > 0 && diff < 60000) {
        new Notification('E LIFE Reminder', {
          body: r.title,
          icon: '/assets/logo.png'
        });
      }
    }
  });
}
setInterval(checkReminders, 30000);

// ── PROFILE CONTEXT FOR CHAT ──────────
function getProfileContext() {
  const p = loadData('profile', {});
  if(!p.name && !p.biz && !p.context) return '';
  return `\n\nUser info: Name: ${p.name||'Unknown'}, Business: ${p.biz||'N/A'}, City: ${p.city||'N/A'}. ${p.context||''}`;
}

# E LIFE Agent v0.1.0
> **Your AI-Powered Life** — Personal + Business AI Agent

---

## Quick Start

### Option 1 — Double Click (Easiest)
```
START.bat ko double click karo
```
Browser automatically khul jayega `http://localhost:8000` pe.

### Option 2 — PowerShell
```powershell
cd "D:\ELIFE_AGENT"
python -m uvicorn api.main:app --port 8000
```

### Option 3 — Browser only (no server)
```
ui/index.html directly browser mein kholo
```
LocalStorage use karega — sab kaam karega lekin data JSON files mein save nahi hoga.

---

## Folder Structure

```
E LIFE AGENT/
├── START.bat              ← Double click se start
├── api/
│   └── main.py            ← FastAPI backend
├── ui/
│   ├── index.html         ← Chat (main page)
│   ├── assets/
│   │   ├── core.css       ← Shared styles
│   │   └── core.js        ← Shared JS + API
│   └── pages/
│       ├── dashboard.html
│       ├── tasks.html
│       ├── notes.html
│       ├── customers.html
│       ├── orders.html
│       ├── analytics.html
│       ├── emails.html
│       ├── invoices.html
│       ├── calendar.html
│       ├── reminders.html
│       ├── files.html
│       ├── research.html
│       ├── code.html
│       ├── translate.html
│       ├── profile.html
│       ├── history.html
│       ├── vault.html
│       ├── notifications.html
│       ├── saved.html
│       ├── settings.html
│       ├── apikeys.html
│       └── about.html
├── core/                  ← Python agent core
├── modules/               ← Feature modules
├── config/                ← Settings JSON
├── data/local/            ← JSON data files
├── .env                   ← API keys
└── requirements.txt
```

---

## Features

| Feature | Status |
|---------|--------|
| AI Chat (Groq) | ✅ Working |
| Voice Input | ✅ Chrome mein |
| Photo Analysis | ✅ Working |
| Multi AI Model | ✅ 5 models |
| AI vs AI Debate | ✅ Working |
| Chat History | ✅ Working |
| Dashboard | ✅ Live stats |
| Tasks | ✅ Full CRUD |
| Notes | ✅ Grid view |
| Calendar | ✅ Events |
| Customers | ✅ Full CRUD |
| Orders | ✅ Status track |
| Invoices | ✅ Print ready |
| Analytics | ✅ AI insights |
| Emails | ✅ AI drafts |
| Files | ✅ AI analyze |
| Research | ✅ AI powered |
| Code Helper | ✅ AI generator |
| Translator | ✅ 10+ languages |
| Reminders | ✅ Browser notif |
| Private Vault | ✅ PIN locked |
| Profile | ✅ Agent memory |
| Settings | ✅ Full control |
| Data Export | ✅ JSON backup |
| Data Import | ✅ Restore |
| Dark/Light Mode | ✅ Persistent |
| FastAPI Backend | ✅ REST API |

---

## .env File
```
GROQ_API_KEY=gsk_your_key_here
APP_SECRET_KEY=elife_secret_123
VAULT_PASSWORD=your_vault_password
DEBUG=False
```

---

## API Endpoints
```
GET  /api/health
POST /api/chat
GET  /api/tasks        POST /api/tasks
GET  /api/notes        POST /api/notes
GET  /api/customers    POST /api/customers
GET  /api/orders       POST /api/orders
GET  /api/reminders    POST /api/reminders
GET  /api/invoices     POST /api/invoices
GET  /api/events       POST /api/events
GET  /api/profile      POST /api/profile
```

---

*E LIFE — Ek AI jo teri life samjhe.* 🚀

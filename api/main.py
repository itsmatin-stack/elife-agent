"""
E LIFE Agent — FastAPI Backend
Run: uvicorn api.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import json, os, uuid
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="E LIFE Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── GROQ CLIENT ──────────────────────────
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SYSTEM_PROMPT = "Tu E LIFE Agent hai — smart, helpful personal AI. Hinglish mein baat kar. Short, clear replies de."

# ── DATA STORAGE (JSON files) ─────────────
DATA_DIR = "data/local"
os.makedirs(DATA_DIR, exist_ok=True)

def read_data(key: str, default=None):
    path = f"{DATA_DIR}/{key}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default if default is not None else []

def write_data(key: str, data):
    with open(f"{DATA_DIR}/{key}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def gen_id():
    return str(uuid.uuid4())[:8]

# ── MODELS ───────────────────────────────
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "llama-3.3-70b-versatile"

class Task(BaseModel):
    title: str
    done: Optional[bool] = False

class Note(BaseModel):
    title: str
    content: Optional[str] = ""

class Customer(BaseModel):
    name: str
    phone: Optional[str] = ""
    email: Optional[str] = ""
    note: Optional[str] = ""

class Order(BaseModel):
    customer: str
    item: Optional[str] = ""
    amount: Optional[float] = 0
    status: Optional[str] = "pending"

class Reminder(BaseModel):
    title: str
    time: Optional[str] = ""
    note: Optional[str] = ""

class Invoice(BaseModel):
    client: str
    desc: Optional[str] = ""
    amount: Optional[float] = 0
    due: Optional[str] = ""

class CalEvent(BaseModel):
    title: str
    date: str
    time: Optional[str] = ""
    color: Optional[str] = "#534AB7"

# ── CHAT ─────────────────────────────────
@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        messages = [{"role": m.role, "content": m.content} for m in req.messages]
        resp = groq_client.chat.completions.create(
            model=req.model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages[-12:],
            max_tokens=1024,
            temperature=0.7,
        )
        reply = resp.choices[0].message.content
        return {"reply": reply, "model": req.model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── TASKS ────────────────────────────────
@app.get("/api/tasks")
def get_tasks():
    return read_data("tasks")

@app.post("/api/tasks")
def add_task(task: Task):
    tasks = read_data("tasks")
    new = {"id": gen_id(), "title": task.title, "done": False, "created": datetime.now().isoformat()}
    tasks.append(new)
    write_data("tasks", tasks)
    return new

@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    tasks = read_data("tasks")
    tasks = [t if t["id"] != task_id else {**t, "done": task.done, "title": task.title} for t in tasks]
    write_data("tasks", tasks)
    return {"ok": True}

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    tasks = [t for t in read_data("tasks") if t["id"] != task_id]
    write_data("tasks", tasks)
    return {"ok": True}

# ── NOTES ────────────────────────────────
@app.get("/api/notes")
def get_notes():
    return read_data("notes")

@app.post("/api/notes")
def add_note(note: Note):
    notes = read_data("notes")
    new = {"id": gen_id(), "title": note.title, "content": note.content, "created": datetime.now().isoformat()}
    notes.append(new)
    write_data("notes", notes)
    return new

@app.delete("/api/notes/{note_id}")
def delete_note(note_id: str):
    notes = [n for n in read_data("notes") if n["id"] != note_id]
    write_data("notes", notes)
    return {"ok": True}

# ── CUSTOMERS ────────────────────────────
@app.get("/api/customers")
def get_customers():
    return read_data("customers")

@app.post("/api/customers")
def add_customer(c: Customer):
    customers = read_data("customers")
    new = {"id": gen_id(), "name": c.name, "phone": c.phone, "email": c.email, "note": c.note, "created": datetime.now().isoformat()}
    customers.append(new)
    write_data("customers", customers)
    return new

@app.delete("/api/customers/{cid}")
def delete_customer(cid: str):
    customers = [c for c in read_data("customers") if c["id"] != cid]
    write_data("customers", customers)
    return {"ok": True}

# ── ORDERS ───────────────────────────────
@app.get("/api/orders")
def get_orders():
    return read_data("orders")

@app.post("/api/orders")
def add_order(o: Order):
    orders = read_data("orders")
    new = {"id": gen_id(), "customer": o.customer, "item": o.item, "amount": o.amount, "status": o.status, "created": datetime.now().isoformat()}
    orders.append(new)
    write_data("orders", orders)
    return new

@app.put("/api/orders/{oid}/status")
def update_order_status(oid: str, body: dict):
    orders = read_data("orders")
    orders = [o if o["id"] != oid else {**o, "status": body.get("status", o["status"])} for o in orders]
    write_data("orders", orders)
    return {"ok": True}

@app.delete("/api/orders/{oid}")
def delete_order(oid: str):
    orders = [o for o in read_data("orders") if o["id"] != oid]
    write_data("orders", orders)
    return {"ok": True}

# ── REMINDERS ────────────────────────────
@app.get("/api/reminders")
def get_reminders():
    return read_data("reminders")

@app.post("/api/reminders")
def add_reminder(r: Reminder):
    reminders = read_data("reminders")
    new = {"id": gen_id(), "title": r.title, "time": r.time, "note": r.note, "done": False, "created": datetime.now().isoformat()}
    reminders.append(new)
    write_data("reminders", reminders)
    return new

@app.put("/api/reminders/{rid}/done")
def toggle_reminder(rid: str):
    reminders = read_data("reminders")
    reminders = [r if r["id"] != rid else {**r, "done": not r.get("done", False)} for r in reminders]
    write_data("reminders", reminders)
    return {"ok": True}

@app.delete("/api/reminders/{rid}")
def delete_reminder(rid: str):
    reminders = [r for r in read_data("reminders") if r["id"] != rid]
    write_data("reminders", reminders)
    return {"ok": True}

# ── INVOICES ─────────────────────────────
@app.get("/api/invoices")
def get_invoices():
    return read_data("invoices")

@app.post("/api/invoices")
def add_invoice(inv: Invoice):
    invoices = read_data("invoices")
    count = read_data("inv_count", 1)
    new = {"id": gen_id(), "no": f"INV-{str(count).zfill(3)}", "client": inv.client, "desc": inv.desc, "amount": inv.amount, "due": inv.due, "status": "pending", "created": datetime.now().isoformat()}
    invoices.append(new)
    write_data("invoices", invoices)
    write_data("inv_count", count + 1)
    return new

@app.put("/api/invoices/{iid}/paid")
def mark_invoice_paid(iid: str):
    invoices = read_data("invoices")
    invoices = [i if i["id"] != iid else {**i, "status": "paid"} for i in invoices]
    write_data("invoices", invoices)
    return {"ok": True}

@app.delete("/api/invoices/{iid}")
def delete_invoice(iid: str):
    invoices = [i for i in read_data("invoices") if i["id"] != iid]
    write_data("invoices", invoices)
    return {"ok": True}

# ── CALENDAR ─────────────────────────────
@app.get("/api/events")
def get_events():
    return read_data("cal_events")

@app.post("/api/events")
def add_event(ev: CalEvent):
    events = read_data("cal_events")
    new = {"id": gen_id(), "title": ev.title, "date": ev.date, "time": ev.time, "color": ev.color}
    events.append(new)
    write_data("cal_events", events)
    return new

@app.delete("/api/events/{eid}")
def delete_event(eid: str):
    events = [e for e in read_data("cal_events") if e["id"] != eid]
    write_data("cal_events", events)
    return {"ok": True}

# ── PROFILE ──────────────────────────────
@app.get("/api/profile")
def get_profile():
    return read_data("profile", {})

@app.post("/api/profile")
def save_profile(profile: dict):
    write_data("profile", profile)
    return {"ok": True}

# ── HEALTH ───────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0", "agent": "E LIFE"}

# ── SERVE UI ─────────────────────────────
# Service worker needs specific headers
from fastapi.responses import FileResponse
from fastapi import Request

@app.get("/sw.js")
async def service_worker():
    return FileResponse("ui/sw.js", headers={
        "Cache-Control": "no-cache",
        "Content-Type": "application/javascript"
    })

@app.get("/manifest.json")
async def manifest():
    return FileResponse("ui/manifest.json", headers={
        "Content-Type": "application/manifest+json"
    })

app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

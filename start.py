"""
E LIFE Agent — Quick Start
Run: python start.py
"""
import subprocess, webbrowser, time, sys, os

print("=" * 40)
print("   E LIFE Agent v0.1.0")
print("   Starting...")
print("=" * 40)

server = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8000"],
    cwd=os.path.dirname(os.path.abspath(__file__))
)

print("\n[E LIFE] Server starting on http://localhost:8000")
print("[E LIFE] Browser mein khul raha hai...")
time.sleep(3)
webbrowser.open("http://localhost:8000")
print("[E LIFE] Ctrl+C se band karo\n")

try:
    server.wait()
except KeyboardInterrupt:
    print("\n[E LIFE] Alvida!")
    server.terminate()

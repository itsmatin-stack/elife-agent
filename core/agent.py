from core.groq_client import GroqClient
from core.router import Router
from core.memory import MemoryManager

class ELifeAgent:
    def __init__(self, config):
        self.config = config
        self.groq = GroqClient(config)
        self.memory = MemoryManager()
        self.router = Router(self.groq, self.memory)
        print("[E LIFE] Core initialized.")

    def start(self):
        print("[E LIFE] Agent ready. 'exit' likhke band karo.\n")
        while True:
            try:
                user_input = input("Tum: ").strip()
                if user_input.lower() in ["exit", "quit", "band karo"]:
                    print("[E LIFE] Alvida!")
                    break
                if not user_input:
                    continue
                response = self.router.handle(user_input)
                print(f"\nE LIFE: {response}\n")
            except KeyboardInterrupt:
                print("\n[E LIFE] Alvida!")
                break

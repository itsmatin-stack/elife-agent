import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

class GroqClient:
    def __init__(self, config):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = config.get("ai", {}).get("model", "llama-3.3-70b-versatile")
        self.max_tokens = config.get("ai", {}).get("max_tokens", 1024)
        self.temperature = config.get("ai", {}).get("temperature", 0.7)
        self.system_prompt = (
            "Tu E LIFE Agent hai — ek smart aur personal AI assistant. "
            "Tu Hindi, English aur Hinglish samajhta hai. "
            "User ki personal aur business life manage karne mein help kar. "
            "Short, clear aur useful replies de."
        )

    def chat(self, messages: list) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": self.system_prompt}] + messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[Error] Groq connect nahi hua: {e}"

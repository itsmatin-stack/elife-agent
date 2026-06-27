"""
E LIFE Agent v0.1.0 — Main Entry Point
Run: python main.py
"""
from config.loader import load_config
from core.agent import ELifeAgent

def main():
    print("=" * 40)
    print("   E LIFE Agent v0.1.0")
    print("   Your AI-Powered Life")
    print("=" * 40 + "\n")
    config = load_config()
    agent = ELifeAgent(config)
    agent.start()

if __name__ == "__main__":
    main()

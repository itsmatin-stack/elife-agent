from modules.chat.handler import ChatHandler

class Router:
    def __init__(self, groq_client, memory):
        self.chat = ChatHandler(groq_client, memory)

    def handle(self, user_input: str) -> str:
        return self.chat.handle(user_input)

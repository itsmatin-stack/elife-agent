class ChatHandler:
    def __init__(self, groq_client, memory):
        self.groq = groq_client
        self.memory = memory

    def handle(self, user_input: str) -> str:
        self.memory.add("user", user_input)
        messages = self.memory.get_messages(last_n=10)
        response = self.groq.chat(messages)
        self.memory.add("assistant", response)
        return response

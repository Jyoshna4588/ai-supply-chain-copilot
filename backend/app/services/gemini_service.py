from app.langchain.chains import build_chat_chain


class GeminiService:
    """
    Gemini service powered by LangChain.
    """

    def __init__(self):
        self.chain = build_chat_chain()

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using the LangChain chat pipeline.
        """

        return self.chain.invoke(
            {
                "question": prompt,
            }
        )
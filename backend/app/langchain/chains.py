from langchain_core.output_parsers import StrOutputParser

from app.langchain.model import get_llm
from app.langchain.prompts import GENERAL_CHAT_PROMPT


def build_chat_chain():
    """
    Builds the reusable chat pipeline.
    """

    llm = get_llm()

    return (
        GENERAL_CHAT_PROMPT
        | llm
        | StrOutputParser()
    )
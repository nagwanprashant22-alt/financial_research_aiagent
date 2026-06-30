from langchain_google_genai import ChatGoogleGenerativeAI

from configs.settings import settings


def get_llm() -> ChatGoogleGenerativeAI:
    """
    Create and return the configured Gemini LLM.
    """

    return ChatGoogleGenerativeAI(
        model=settings.DEFAULT_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=settings.TEMPERATURE,
        max_retries=settings.MAX_RETRIES,
        timeout=settings.TIMEOUT,
    )
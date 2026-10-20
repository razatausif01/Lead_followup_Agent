from langchain_groq import ChatGroq
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings


def get_llm(temperature: float = 0.3) -> ChatGroq:
    s = get_settings()
    return ChatGroq(
        model=s.LLM_MODEL,
        temperature=temperature,
        api_key=s.GROQ_API_KEY,
        max_retries=2,
    )


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def invoke_with_retry(llm, messages):
    return llm.invoke(messages)
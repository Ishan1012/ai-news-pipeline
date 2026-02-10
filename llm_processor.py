import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from config import OPENROUTER_API_KEY, LLM_MODELS

load_dotenv()

llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model=LLM_MODELS[0],
    temperature=0.3,
    max_tokens=400
)

prompt = PromptTemplate(
    input_variables=["text"],
    template="""
        You are a news summarization system.

        IMPORTANT:
        - Think briefly
        - DO NOT show your reasoning
        - OUTPUT ONLY the final answer

        Task:
        1. Summarize the article in 2 paragraph of 8-10 sentences.
        2. Classify domain: AI | Research | Medicine | Public Health

        Article:
        {text}

        FINAL ANSWER:
    """
)

def process_article(text: str) -> str:
    try:
        response = llm.invoke(prompt.format(text=text))
        return response.content.strip()
    except Exception as e:
        print("LLM error:", e)
        return "Summary unavailable"
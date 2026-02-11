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
        - Do not explain your reasoning
        - Do not include analysis, thoughts, or planning
        - Do not include phrases like "this article discusses" or "the article explains"
        - Output only the requested results

        TASK:
        1. Write a factual summary of the article in exactly 2 paragraphs.
        2. Each paragraph must contain 8-10 sentences.
        3. Maintain a neutral, journalistic tone.
        5. Classify the article into one domain from: AI, Research, Medicine, Public Health.

        ARTICLE:
        {text}

        FINAL ANSWER FORMAT:
        Paragraph 1 summary text.
        
        Paragraph 2 summary text.
        
        Domain: <one domain only>
    """
)

def process_article(text: str) -> str:
    try:
        response = llm.invoke(prompt.format(text=text))
        return response.content.strip()
    except Exception as e:
        print("LLM error:", e)
        return "Summary unavailable"
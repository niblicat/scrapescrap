# Creates an article summary using LLM

from openai import OpenAI
client = OpenAI()
from abc import ABC, abstractmethod

class LLMRequest(ABC):
    """
    Abstract base class that defines the responsibility of a single LLM Request
    """
    @staticmethod
    @abstractmethod
    def GenerateSummary(input: str):
        """
        Given some content passed as a string, create a summary
        """
        raise NotImplementedError("Implemented by subclass")

class OpenAIRequest(LLMRequest):
    def GenerateSummary(input: str) -> str:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a writer that summarises a provided satire article into up to 50 words."},
                {"role": "user", "content": f"Summarise the given article content: {input}"}
            ]
        )

        return completion.choices[0].message.content
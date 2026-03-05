import json
from openai import AsyncOpenAI
from app.config import settings
from app.llm.base import LLMProvider
from typing import Dict, Any

class OpenAIClient(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt + "\nIMPORTANT: You must output valid JSON."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content)

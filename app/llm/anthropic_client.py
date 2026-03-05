import json
from anthropic import AsyncAnthropic
from app.config import settings
from app.llm.base import LLMProvider
from typing import Dict, Any

class AnthropicClient(LLMProvider):
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-opus-20240229"

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2048,
            temperature=0.2
        )
        return response.content[0].text

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        # Claude does not have a strict JSON mode flag like OpenAI, but prefixing guidance helps.
        modified_system = system_prompt + "\n\nRespond ONLY with a valid JSON object. Do not include markdown formatting or explanation."
        text_response = await self.generate_text(modified_system, user_prompt)
        
        # Strip potential markdown formatting
        text_response = text_response.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
            text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
            
        return json.loads(text_response.strip())

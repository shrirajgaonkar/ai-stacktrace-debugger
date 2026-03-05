from app.config import settings
from app.llm.openai_client import OpenAIClient
from app.llm.anthropic_client import AnthropicClient
from typing import Dict, Any

class LLMRouter:
    def __init__(self):
        self.openai = OpenAIClient()
        self.anthropic = AnthropicClient()
        
    def get_provider_for_log(self, text: str):
        # Router mode: simple/short logs -> OpenAI. Long/multi-trace logs -> Anthropic Claude
        if len(text) > 5000:
            return self.anthropic
        return self.openai

    async def get_explanation(self, provider, system_prompt: str, user_prompt: str) -> str:
        return await provider.generate_text(system_prompt, user_prompt)
        
    async def get_json_structure(self, provider, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        return await provider.generate_json(system_prompt, user_prompt)

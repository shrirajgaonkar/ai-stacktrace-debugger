from typing import Dict, Any

class LLMProvider:
    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError
        
    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        raise NotImplementedError

"""
LM Studio API Client
Connects to LM Studio server via OpenAI-compatible API.
"""

import openai
from typing import Optional
import config


class LMStudioClient:
    def __init__(self, base_url: str = config.API_URL, api_key: str = config.API_KEY):
        self.base_url = base_url
        self.client = openai.OpenAI(base_url=base_url, api_key=api_key)
    
    def is_connected(self) -> bool:
        try:
            models = self.client.models.list()
            return True
        except Exception:
            return False
    
    def get_model_name(self) -> Optional[str]:
        try:
            models = self.client.models.list()
            if models.data:
                return models.data[0].id
            return None
        except Exception:
            return None
    
    def generate(self, prompt: str, system_prompt: str = "", 
                 max_tokens: int = config.MAX_TOKENS,
                 temperature: float = config.TEMPERATURE,
                 stop: Optional[list] = None) -> str:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop
        )
        
        return response.choices[0].message.content
    
    def generate_with_retry(self, prompt: str, system_prompt: str = "",
                           max_retries: int = 3, delay: float = 1.0) -> str:
        import time
        
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, system_prompt)
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise e


def create_client() -> LMStudioClient:
    return LMStudioClient()


def check_connection() -> dict:
    client = create_client()
    
    if client.is_connected():
        model_name = client.get_model_name()
        return {
            "status": "connected",
            "model": model_name,
            "url": config.API_URL
        }
    else:
        return {
            "status": "disconnected",
            "error": "Cannot connect to LM Studio server",
            "url": config.API_URL
        }

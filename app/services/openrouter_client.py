import httpx
from app.core.config import settings
from app.core.errors import ExternalServiceError

class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.model = settings.openrouter_model  
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json",
        }

    async def chat_completion(self, messages: list[dict[str, str]], temperature: float = 0.7) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,  
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if data["choices"] and data["choices"][0]["message"]["content"]:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise ExternalServiceError("Empty response")
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(f"OpenRouter API error: {e.response.status_code}") from e
            except httpx.RequestError as e:
                raise ExternalServiceError(f"OpenRouter network error: {str(e)}") from e
            except Exception as e:
                raise ExternalServiceError(f"Error from OpenRouter: {str(e)}") from e
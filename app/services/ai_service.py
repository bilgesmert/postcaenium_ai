import requests

from flask import current_app

class AIServiceError(Exception):
    pass


class AIService:
    def __init__(self):
        self.model = "openai/gpt-oss-20b"

    def yanit_uret(self, mesaj, gecmis=None):
        gecmis = gecmis or []

        api_key = current_app.config.get("GROQ_API_KEY")

        if not api_key:
            return "Demo modu: Mesajınız alındı. POSTCAENIUM hakkında size yardımcı olabilirim."

        messages = [
        {
            "role": "system",
            "content": current_app.config["BUSINESS_CONTEXT"]
        }
    ]

        messages.extend(gecmis)
        messages.append({"role": "user", "content": mesaj})

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "reasoning_effort": "low",
                    "max_completion_tokens": 250
                },
                timeout=30
            )

            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            raise AIServiceError(
                f"Yapay zeka servisine bağlanırken hata oluştu: {e}"
            )
ai_service = AIService()     
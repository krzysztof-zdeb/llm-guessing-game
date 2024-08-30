from openai import OpenAI
from config import Config
from prompts import build_guess_character_prompt
from typing import Any

def get_openai_client() -> OpenAI:
    return OpenAI(
        api_key=Config.API_KEY,
        base_url=Config.API_BASE,
    )

def send_prompt(client: OpenAI, model_name: str, prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error sending prompt: {e}")
        raise

def get_character_to_guess(client: OpenAI, model_name: str) -> str:
    prompt = build_guess_character_prompt()
    return send_prompt(client, model_name, prompt)

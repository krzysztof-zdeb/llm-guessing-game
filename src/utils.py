from openai import OpenAI
from config import config
from prompts import build_guess_character_prompt
from typing import Any
from logger import logger

def get_openai_client() -> OpenAI:
    """
    Create and return an OpenAI client instance.
    
    Returns:
        OpenAI: An instance of the OpenAI client.
    """
    return OpenAI(
        api_key=config.API_KEY,
        base_url=config.API_BASE,
    )

def send_prompt(client: OpenAI, model_name: str, prompt: str) -> str:
    """
    Send a prompt to the OpenAI API and return the response.
    
    Args:
        client (OpenAI): The OpenAI client instance.
        model_name (str): The name of the model to use.
        prompt (str): The prompt to send.
    
    Returns:
        str: The response from the API.
    
    Raises:
        Exception: If there's an error sending the prompt.
    """
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

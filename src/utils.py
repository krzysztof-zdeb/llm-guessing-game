from openai import OpenAI
from config import Config
from prompts import build_guess_character_prompt

def get_openai_client():
    client = OpenAI(
        api_key=Config.API_KEY,
        base_url=Config.API_BASE,
    )
    return client

def send_prompt(client, model_name, prompt):
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()


def get_character_to_guess(client, model_name):
    prompt = build_guess_character_prompt()
    response = send_prompt(client, model_name, prompt)
    return response

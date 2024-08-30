import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI API base URL
    API_BASE = "https://api.openai.com/v1"

    # API Key for Azure OpenAI service
    API_KEY = os.getenv("OPENAI_API_KEY")

    # List of models to use
    MODELS = {
        "judge": "gpt-4o",  # Specify the model for the judge
        "guessers": [
#            "gpt-4", # $30.00/1M input tokens, $60.00/1M output tokens
#            "gpt-4-turbo", # $10.00/1M input tokens, $30.00/1M output tokens
#            "gpt-4o", # $5.00/1M input tokens, $15.00/1M output tokens
#            "gpt-3.5-turbo", # $3.00/1M input tokens, $6.00/1M output tokens
            "gpt-4o-mini" # $0.15/1M input tokens, $0.50/1M output tokens
        ]
    }

    # Character to be guessed
    CHARACTER_TO_GUESS = "" #"Artemis Fowl"

    # Maximum number of questions allowed
    MAX_QUESTIONS = 30

    # Number of rounds to play (i.e. characters to guess)
    NUM_ROUNDS = 3


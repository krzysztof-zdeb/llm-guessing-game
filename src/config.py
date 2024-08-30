import os
from typing import Dict, List
import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        with open("src/config.yaml", "r") as config_file:
            self._config = yaml.safe_load(config_file)

        self.API_BASE: str = self._config["api"]["base_url"]
        self.API_KEY: str = os.getenv(self._config["api"]["key"].strip("${}"))
        self.MODELS: Dict[str, str | List[str]] = self._config["models"]
        self.CHARACTER_TO_GUESS: str = self._config["game"]["character_to_guess"]
        self.MAX_QUESTIONS: int = self._config["game"]["max_questions"]
        self.NUM_ROUNDS: int = self._config["game"]["num_rounds"]

config = Config()


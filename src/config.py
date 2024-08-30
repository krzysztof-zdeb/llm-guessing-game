import os
from typing import Dict, List
import yaml
from dotenv import load_dotenv

load_dotenv()

class Character:
    def __init__(self, primary: str, aliases: List[str]):
        self.primary = primary
        self.aliases = aliases

class Config:
    def __init__(self):
        with open("src/config.yaml", "r") as config_file:
            self._config = yaml.safe_load(config_file)

        self.API_BASE: str = self._config["api"]["base_url"]
        self.API_KEY: str = os.getenv(self._config["api"]["key"].strip("${}"))
        self.MODELS: Dict[str, str | List[str]] = self._config["models"]
        self.CHARACTERS_TO_GUESS: List[Character] = [
            Character(char["primary"], char.get("aliases", []))
            for char in self._config["game"]["characters_to_guess"]
        ]
        self.MAX_QUESTIONS: int = self._config["game"]["max_questions"]
        self.NUM_ROUNDS: int = self._config["game"]["num_rounds"]

config = Config()


from utils import get_openai_client, send_prompt, get_character_to_guess
from config import Config
from prompts import build_guesser_prompt, build_judge_prompt
from logger import logger
from typing import List, Tuple

class GuessingGame:

    def __init__(self):
        self.client = get_openai_client()
        self.judge_model: str = Config.MODELS["judge"]
        self.guesser_models: List[str] = Config.MODELS["guessers"]
        self.character: str = Config.CHARACTER_TO_GUESS or get_character_to_guess(self.client, self.judge_model)
        self.max_questions: int = Config.MAX_QUESTIONS
        self.num_rounds: int = Config.NUM_ROUNDS
        self.history: List[Tuple[str, str]] = []

    def play_game(self) -> None:
        for game_round in range(self.num_rounds):
            logger.info(f"--- Round {game_round + 1} ---")
            logger.info(f"The character is: {self.character}")

            for guesser_model in self.guesser_models:
                logger.info(f"\n{guesser_model} is now guessing:")
                question_count = 0
                self.history = []

                while question_count < self.max_questions:
                    question_count += 1
                    
                    # Generate question using the guesser model
                    guesser_prompt = build_guesser_prompt(self.history)
                    question = send_prompt(self.client, guesser_model, guesser_prompt)
                    logger.info(f"Q#{question_count}: {question}")

                    # Get answer from the judge
                    judge_prompt = build_judge_prompt(self.character, self.history, question)
                    answer = send_prompt(self.client, self.judge_model, judge_prompt)
                    
                    self.history.append((question, answer))
                    logger.info(f"A: {answer}")

                    if answer.lower() == "bravo":
                        logger.info(f"{guesser_model} has guessed correctly!")
                        break

                if question_count == self.max_questions:
                    logger.info(f"{guesser_model} has reached the maximum number of questions without guessing correctly.")

            if game_round < self.num_rounds - 1:
                self.character = get_character_to_guess(self.client, self.judge_model)
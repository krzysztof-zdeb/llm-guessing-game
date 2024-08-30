from typing import List, Tuple
from openai import OpenAI
from config import config
from prompts import build_guesser_prompt, build_judge_prompt
from utils import get_openai_client, send_prompt
from logger import logger

class GuessingGame:

    def __init__(self):
        self.client = get_openai_client()
        self.judge_model: str = config.MODELS["judge"]
        self.guesser_models: List[str] = config.MODELS["guessers"]
        self.characters: List[str] = config.CHARACTERS_TO_GUESS
        self.max_questions: int = config.MAX_QUESTIONS
        self.num_rounds: int = config.NUM_ROUNDS
        self.history: List[Tuple[str, str]] = []
        self.last_dunno: str = ""

    def play_game(self) -> None:
        """
        Play the guessing game for all characters and guesser models.
        """
        for character in self.characters:
            logger.info(f"=== New character: {character} ===")
            
            for guesser_model in self.guesser_models:
                logger.info(f"=== {guesser_model} is now guessing ===")

                for game_round in range(self.num_rounds):
                    logger.info(f"-- Round {game_round + 1} --")

                    question_count = 0
                    self.history = []

                    while question_count < self.max_questions:
                        question_count += 1
                         
                        question = self._get_question(guesser_model)
                        logger.info(f"Q#{question_count}: {question}")

                        answer = self._get_answer(character, question)
                        if answer.lower() == "bravo" and character.lower() not in question.lower():
                            # Change the answer to "yes" if the character name is not in the answer
                            answer = "Yes"
                        logger.info(f"A: {answer}")
                        if answer.lower() == "bravo":
                            logger.info(f"{guesser_model} has guessed correctly!")
                            break

                        if answer.lower() == "dunno":
                            self.last_dunno = question
                        else:
                            self.history.append((question, answer))
                            self.last_dunno = ""

                    if question_count == self.max_questions:
                        logger.info(f"{guesser_model} has reached the maximum number of questions without guessing correctly.")

    def _get_question(self, guesser_model: str) -> str:
        """
        Get a question from the guesser model.
        
        Args:
            guesser_model (str): The name of the guesser model.
        
        Returns:
            str: The question from the guesser model.
        """
        guesser_prompt = build_guesser_prompt(self.history, self.last_dunno)
        return send_prompt(self.client, guesser_model, guesser_prompt)

    def _get_answer(self, character: str, question: str) -> str:
        """
        Get an answer from the judge model.
        
        Args:
            character (str): The character to be guessed.
            question (str): The question to answer.
        
        Returns:
            str: The answer from the judge model.
        """
        judge_prompt = build_judge_prompt(character, self.history, question)
        answer = send_prompt(self.client, self.judge_model, judge_prompt)
        return answer
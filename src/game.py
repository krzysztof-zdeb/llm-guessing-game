from typing import List, Tuple
from openai import OpenAI
from config import Character, config
from prompts import build_guesser_prompt, build_judge_prompt
from utils import get_openai_client, send_prompt
from logger import logger
from database import Database

class GuessingGame:

    def __init__(self):
        self.client = get_openai_client()
        self.judge_model: str = config.MODELS["judge"]
        self.guesser_models: List[str] = config.MODELS["guessers"]
        self.characters: List[Character] = config.CHARACTERS_TO_GUESS
        self.max_questions: int = config.MAX_QUESTIONS
        self.num_rounds: int = config.NUM_ROUNDS
        self.history: List[Tuple[int, str, str]] = []
        self.last_dunno: str = ""
        self.db = Database()

    def play_game(self) -> None:
        """
        Play the guessing game for all characters and guesser models.
        
        """

        for character in self.characters:
            logger.info(f"=== New character: {character.primary} ===")
            
            for guesser_model in self.guesser_models:
                logger.info(f"=== {guesser_model} is now guessing ===")

                for game_round in range(self.num_rounds):
                    logger.info(f"-- Round {game_round + 1} --")

                    question_count = 0
                    self.history = []

                    # Insert dummy record
                    round_sk = self.db.insert_game_round(character.primary, guesser_model, self.judge_model)

                    while question_count < self.max_questions:
                        question_count += 1

                        if question_count == self.max_questions:
                            logger.info(f"{guesser_model} has reached the maximum number of questions without guessing correctly.")
                            # Update the game round record
                            self.db.update_game_round(round_sk, question_count, False)
                            break

                        question = self._get_question(guesser_model)
                        logger.info(f"Q#{question_count}: {question}")

                        answer = self._get_answer(character, question)
                    
                        if answer.lower().startswith("bravo") and not self._is_correct_guess(character, question):
                            # Change the answer to "yes" if the character name is not in the answer
                            answer = "Yes"
                        logger.info(f"A: {answer}")
                        
                        if answer.lower().startswith("bravo"):
                            logger.info(f"{guesser_model} has guessed correctly!")
                            # Update the game round record
                            self.history.append((question_count, question, answer))
                            self.db.update_game_round(round_sk, question_count, True)
                            break

                        if answer.lower().startswith("dunno"):
                            self.last_dunno = question
                        else:
                            self.history.append((question_count, question, answer))
                            self.last_dunno = ""

                    # Insert conversation history for the round
                    if self.history:
                        self.db.insert_conversation_history(round_sk, self.history)

        self.db.close()

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

    def _get_answer(self, character: Character, question: str) -> str:
        """
        Get an answer from the judge model.
        
        Args:
            character (Character): The character to be guessed.
            question (str): The question to answer.
        
        Returns:
            str: The answer from the judge model.
        """
        judge_prompt = build_judge_prompt(character.primary, self.history, question)
        answer = send_prompt(self.client, self.judge_model, judge_prompt)
        return answer

    def _is_correct_guess(self, character: Character, question: str) -> bool:
        """
        Check if the question contains the correct character name or any of its aliases.
        
        Args:
            character (Character): The character to be guessed.
            question (str): The question to check.
        
        Returns:
            bool: True if the question contains the correct character name or any of its aliases, False otherwise.
        """
        question_lower = question.lower()
        return (
            character.primary.lower() in question_lower or
            any(alias.lower() in question_lower for alias in character.aliases)
        )
from typing import List, Tuple

def build_guess_character_prompt() -> str:
    """
    Build the prompt for guessing a character.
    
    Returns:
        str: The prompt for guessing a character.
    """
    return (
        "You are participating in a guessing game. Your task is to think of a well-known character "
        "from fiction, history, or popular culture. This character should be recognizable to a wide audience. "
        "Be creative and think of a character that is not too obscure or well-known. "
        "Please provide the name of the character you've chosen."
    )

def generate_game_history(history: List[Tuple[str, str]]) -> str:
    """
    Generate a string representation of the game history.
    
    Args:
        history (List[Tuple[str, str]]): List of question-answer pairs processed so far.
    
    Returns:
        str: Formatted game history.
    """
    return "\n".join([f"- Q: {q} - A: {a}" for q, a in history])

def build_guesser_prompt(history: List[Tuple[str, str]]) -> str:
    """
    Build the prompt for the guesser model.
    
    Args:
        history (List[Tuple[str, str]]): List of question-answer pairs processed so far.
    
    Returns:
        str: The prompt for the guesser model.
    """
    prompt = (
        "You are participating in a guessing game where your goal is to identify a specific character. "
        "You have been asking questions to narrow down who the character might be. "
    )
    
    if history:
        game_history = generate_game_history(history)
        prompt += (
            "Below are the questions you have asked so far and their corresponding answers.\n\n"
            f"{game_history}\n\n"
            "Remember to consider all previous questions and answers before forming your next question. "
            "Do not ask the same question twice. "
            "Avoid enumerating titles of series or franchises. Instead try to narrow down the character by asking about their traits or actions. "
            "You can only ask one question. "
            "Provide only question, do not include any other text. "
            "What is your next question?"
            # "The last question you asked was either too vague, ambiguous, or not directly related to identifying the character. "
        )
    
    # prompt += (
    #     "Please rephrase or clarify your question so that it can be answered with a clear 'Yes' or 'No.' "
    # )
    return prompt

def build_judge_prompt(character: str, history: List[Tuple[str, str]], question: str) -> str:
    """
    Build the prompt for the judge model.
    
    Args:
        character (str): The character to be guessed.
        history (List[Tuple[str, str]]): List of question-answer pairs processed so far.
        question (str): The current question to be answered.
    
    Returns:
        str: The prompt for the judge model.
    """
    prompt = (
        "You are participating in a guessing game where another model will attempt to guess a specific character "
        "by asking closed questions. Your role is to answer questions based on your knowledge of the character.\n\n"
        f"The character is: {character}.\n\n"
        "Respond with 'Yes' or 'No' based on the accuracy of the question in relation to the character. "
        "If the question is unclear, too vague, or does not directly apply to the character, respond with 'Dunno'. "
        "If the question properly indicates the character to be guessed, respond with 'Bravo'. "
        "You can only answer with 'Bravo' if the question is clear, specific, and directly related to the character and not the movie or book the character is from. "
        "Your answers must be consistent with the character's traits, actions, and known information. "
    )

    if history:
        game_history = generate_game_history(history)
        prompt += (
            "Make sure your answer is coherent with the previous answers which are:\n\n"
            f"{game_history}\n\n"
        )

    prompt += f"The question you need to answer now is: {question}"

    return prompt

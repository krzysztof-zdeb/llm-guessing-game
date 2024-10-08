from typing import List, Tuple

def generate_game_history(history: List[Tuple[int, str, str]]) -> str:
    """
    Generate a string representation of the game history.
    
    Args:
        history (List[Tuple[int, str, str]]): List of question-answer pairs processed so far.
    
    Returns:
        str: Formatted game history.
    """
    return "\n".join([f"- Q: {q} - A: {a}" for i, q, a in history])

def build_guesser_prompt(history: List[Tuple[int, str, str]], last_dunno: str) -> str:
    """
    Build the prompt for the guesser model.
    
    Args:
        history (List[Tuple[int, str, str]]): List of question-answer pairs processed so far.
        last_dunno (str): The last question, if the answer to it was 'Dunno'.
    
    Returns:
        str: The prompt for the guesser model.
    """
    prompt = (
        "You are participating in a guessing game where your goal is to identify a specific character. "
        "You can only ask questions that can be answered with 'Yes' or 'No'. "
    )
    
    if history:
        game_history = generate_game_history(history)
        prompt += (
            "Below are the questions you have asked so far and their corresponding answers.\n"
            f"{game_history}\n\n"
            "Remember to consider all previous questions and answers before forming your next question. "
            "Do not ask the same question twice. You can only ask one question at a time. "
            "Avoid enumerating titles of series or franchises. Instead try to narrow down the character "
            "by asking about their traits or actions. "
            "If based on the questions and answers so far, you know the character, provide its name. "
            "Don't ask excessive questions if you already have a good idea of the character. Just provide its name. "
        )
    
        if last_dunno:
            prompt += (
                "The last question you asked was either too vague, ambiguous, or not directly related to identifying the character. "
                "Please rephrase or clarify your question so that it can be answered with a clear 'Yes' or 'No'. "
            )

        prompt += "What is your next question? "
    else:
        prompt += "What is your first question? "

    prompt += "Provide only the question, do not include any other text."

    return prompt

def build_judge_prompt(character: str, history: List[Tuple[int, str, str]], question: str) -> str:
    """
    Build the prompt for the judge model.
    
    Args:
        character (str): The character to be guessed.
        history (List[Tuple[int, str, str]]): List of question-answer pairs processed so far.
        question (str): The current question to be answered.
    
    Returns:
        str: The prompt for the judge model.
    """
    prompt = (
        "You are participating in a guessing game where another person attempts to guess a specific character "
        "by asking closed yes/no questions. Your role is to answer the questions based on your knowledge of the character. "
        f"The character is: {character}.\n"
        "Respond with 'Yes' or 'No' based on the accuracy of the question about the character. "
        "Your answers must be consistent with the character's traits, actions, and known information. "
        "Answer with 'Bravo' if the question properly names the character. "
        "Its name must be directly mentioned in the question. "
        "If the question is unclear, too vague, or does not directly apply to the character, respond with 'Dunno'. "
        "If more than one question is asked, respond with 'Dunno'. "
    )

    if history:
        game_history = generate_game_history(history)
        prompt += (
            "Make sure your answer is coherent with the previous answers which are:\n\n"
            f"{game_history}\n\n"
        )

    prompt += f"The question you need to answer now is: {question}"

    return prompt

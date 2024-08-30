from game import GuessingGame
from logger import logger

def main():
    try:
        game = GuessingGame()
        game.play_game()
    except Exception as e:
        logger.error(f"An error occurred during the game: {e}")

if __name__ == "__main__":
    main()


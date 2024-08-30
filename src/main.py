from game import GuessingGame
from logger import logger
from database import Database

def main():
    try:
        game = GuessingGame()
        game.play_game()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if hasattr(game, 'db'):
            game.db.close()

if __name__ == "__main__":
    main()


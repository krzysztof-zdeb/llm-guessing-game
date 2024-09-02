# Character Guessing Game for LLMs

This project implements a character guessing game using OpenAI's GPT models. The game involves AI models trying to guess a character by asking yes/no questions.

## Description

The Character Guessing Game is an AI-powered game where different GPT models attempt to guess a character by asking a series of yes/no questions. The game is designed to showcase the reasoning capabilities of various AI models and how they approach problem-solving.

For a detailed explanation of the project and its implementation, check out the article on Medium (link to be provided).

## Prerequisites

- Python 3.11 or higher
- OpenAI API key

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/krzysztof-zdeb/llm-guessing-game.git
   cd character-guessing-game
   ```

2. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the setup script:
   ```
   .\run.ps1 setup
   ```

   This will create a virtual environment and install the required dependencies.

## Usage

To run the game:
```
.\run.ps1 run
```

This will activate the virtual environment and start the main script.

## Project Structure

- `src/`: Contains the main source code
  - `main.py`: Entry point of the application
  - `game.py`: Implements the GuessingGame class
  - `config.py`: Handles configuration loading
  - `prompts.py`: Contains functions for building prompts
  - `utils.py`: Utility functions
  - `logger.py`: Logging setup
  - `database.py`: Database operations
- `requirements.txt`: List of Python dependencies
- `run.ps1`: PowerShell script for setup and running the game
- `config.yaml`: Configuration file for the game

## Configuration

You can modify the game settings in the `src/config.yaml` file. This includes:

- API settings
- Models to use
- Characters to guess
- Game parameters

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

This project uses OpenAI's GPT models. Make sure you comply with OpenAI's use-case policy when using this code.

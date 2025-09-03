# Hangman Game

A simple console-based Hangman game written in Python using Test-Driven Development (TDD).

## Features

- Two difficulty levels: Basic (single words) and Intermediate (phrases)
- 15-second timer for each guess
- 6 lives system
- Input validation
- Case-insensitive guessing

## Requirements

- Python 3.7+
- No external libraries needed (uses built-in modules)

## How to Run

1. Clone or download this repository
2. Open terminal/command prompt
3. Navigate to the project folder
4. Run the game:
```bash
python3 main.py
```

## How to Run Tests

```bash
python3 -m unittest test_hangman.py -v
```

## Game Rules

1. Choose difficulty level (Basic or Intermediate)
2. Guess letters one at a time
3. You have 15 seconds per guess
4. Wrong guesses or timeouts cost you a life
5. Win by guessing all letters before losing all 6 lives
6. Type 'quit' to exit anytime

## Files

- `hangman.py` - Main game logic
- `main.py` - Game interface and user interaction
- `test_hangman.py` - Unit tests (21 tests total)
- `requirements.txt` - Development tools for linting/formatting

## Development

This project was built using Test-Driven Development (TDD) methodology with comprehensive unit testing to ensure code quality and reliability. 
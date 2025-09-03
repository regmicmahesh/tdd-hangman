import random
import time
from enum import Enum
from typing import Set, List, Optional


class GameLevel(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"


class GameState(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class HangmanGame:
    # Word lists for the different difficulty levels
    BASIC_WORDS = [
        "PYTHON", "PROGRAMMING", "COMPUTER", "KEYBOARD", "MONITOR",
        "SOFTWARE", "HARDWARE", "INTERNET", "WEBSITE", "DATABASE",
        "FUNCTION", "VARIABLE", "BOOLEAN", "INTEGER", "STRING"
    ]

    INTERMEDIATE_PHRASES = [
        "HELLO WORLD", "COMPUTER SCIENCE", "SOFTWARE DEVELOPMENT",
        "ARTIFICIAL INTELLIGENCE", "MACHINE LEARNING", "DATA STRUCTURE",
        "OBJECT ORIENTED", "VERSION CONTROL", "USER INTERFACE"
    ]

    def __init__(self, level: GameLevel):
        self.level = level
        self.lives = 6  # Standard hangman has 6 wrong guesses
        self.state = GameState.PLAYING
        self.guessed_letters: Set[str] = set()
        
        # Timer stuff
        self.timer_start: Optional[float] = None
        self.timer_duration = 15
        
        # Pick a random word or phrase based on level
        if level == GameLevel.BASIC:
            self.target = random.choice(self.BASIC_WORDS)
        else:
            self.target = random.choice(self.INTERMEDIATE_PHRASES)

    def get_display_word(self) -> str:
        if self.level == GameLevel.BASIC:
            # For single words, just put spaces between letters
            display_chars = []
            for char in self.target:
                if char.upper() in self.guessed_letters:
                    display_chars.append(char)
                else:
                    display_chars.append('_')
            return ' '.join(display_chars)
        else:
            # For phrases, need to handle spaces differently
            display_chars = []
            for char in self.target:
                if char == ' ':
                    display_chars.append('  ')  # Double space between words
                elif char.upper() in self.guessed_letters:
                    display_chars.append(char + ' ')
                else:
                    display_chars.append('_ ')
            return ''.join(display_chars).rstrip()

    def make_guess(self, letter: str) -> bool:
        # Check if input is valid
        if not letter or len(letter) != 1 or not letter.isalpha():
            raise ValueError("Guess must be a single letter")
        
        letter = letter.upper()  # Make everything uppercase
        
        # If already guessed, just return if it was correct
        if letter in self.guessed_letters:
            return letter in self.target.upper()
        
        # Add to our list of guessed letters
        self.guessed_letters.add(letter)
        
        # Check if the letter is in the word
        is_correct = letter in self.target.upper()
        
        if not is_correct:
            self.lives -= 1  # Wrong guess = lose a life
            
        self._update_game_state()  # Check if game is over
        
        return is_correct

    def start_timer(self):
        # Record when we started timing
        self.timer_start = time.time()

    def get_remaining_time(self) -> Optional[int]:
        if self.timer_start is None:
            return None
        
        elapsed = time.time() - self.timer_start
        remaining = self.timer_duration - elapsed
        return max(0, int(remaining + 0.5))  # Round up

    def is_time_up(self) -> bool:
        if self.timer_start is None:
            return False
        
        elapsed = time.time() - self.timer_start
        return elapsed >= self.timer_duration

    def handle_timeout(self):
        # Time's up! Lose a life
        self.lives -= 1
        self._update_game_state()
        self.timer_start = None  # Reset for next guess

    def get_guessed_letters(self) -> List[str]:
        return sorted(list(self.guessed_letters))

    def get_target_answer(self) -> str:
        return self.target

    def _update_game_state(self):
        # Check if player lost (no lives left)
        if self.lives <= 0:
            self.state = GameState.LOST
            return
            
        # Check if player won (guessed all letters)
        # Only count actual letters, not spaces
        target_letters = set(char.upper() for char in self.target if char.isalpha())
        if target_letters.issubset(self.guessed_letters):
            self.state = GameState.WON

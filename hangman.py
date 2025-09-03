"""
Simple Hangman Game Implementation using TDD approach.

This module contains the core game logic for a Hangman word guessing game
with support for both basic (single word) and intermediate (phrase) levels.
"""

import random
import time
from enum import Enum
from typing import Set, List, Optional


class GameLevel(Enum):
    """Enumeration for game difficulty levels."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"


class GameState(Enum):
    """Enumeration for game states."""
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class HangmanGame:
    """
    Simple Hangman game class.
    
    Supports two levels:
    - BASIC: Single word guessing
    - INTERMEDIATE: Phrase guessing with multiple words
    """

    # Basic words dictionary
    BASIC_WORDS = [
        "PYTHON", "PROGRAMMING", "COMPUTER", "KEYBOARD", "MONITOR",
        "SOFTWARE", "HARDWARE", "INTERNET", "WEBSITE", "DATABASE",
        "FUNCTION", "VARIABLE", "BOOLEAN", "INTEGER", "STRING"
    ]

    # Intermediate phrases dictionary  
    INTERMEDIATE_PHRASES = [
        "HELLO WORLD", "COMPUTER SCIENCE", "SOFTWARE DEVELOPMENT",
        "ARTIFICIAL INTELLIGENCE", "MACHINE LEARNING", "DATA STRUCTURE",
        "OBJECT ORIENTED", "VERSION CONTROL", "USER INTERFACE"
    ]

    def __init__(self, level: GameLevel):
        """Initialize a new Hangman game."""
        self.level = level
        self.lives = 6
        self.state = GameState.PLAYING
        self.guessed_letters: Set[str] = set()
        
        # Timer variables (simple approach)
        self.timer_start: Optional[float] = None
        self.timer_duration = 15  # 15 seconds per guess
        
        # Select target word/phrase based on level
        if level == GameLevel.BASIC:
            self.target = random.choice(self.BASIC_WORDS)
        else:
            self.target = random.choice(self.INTERMEDIATE_PHRASES)

    def get_display_word(self) -> str:
        """Get the current display representation of the word/phrase."""
        if self.level == GameLevel.BASIC:
            # Basic level: single word with spaces between characters
            display_chars = []
            for char in self.target:
                if char.upper() in self.guessed_letters:
                    display_chars.append(char)
                else:
                    display_chars.append('_')
            return ' '.join(display_chars)
        else:
            # Intermediate level: phrase with spaces between letters
            display_chars = []
            for char in self.target:
                if char == ' ':
                    display_chars.append('  ')  # Double space for word separation
                elif char.upper() in self.guessed_letters:
                    display_chars.append(char + ' ')
                else:
                    display_chars.append('_ ')
            return ''.join(display_chars).rstrip()

    def make_guess(self, letter: str) -> bool:
        """
        Make a guess for a letter.
        
        Args:
            letter: The letter to guess (single character)
            
        Returns:
            True if the letter is in the target word/phrase, False otherwise
        """
        # Input validation
        if not letter or len(letter) != 1 or not letter.isalpha():
            raise ValueError("Guess must be a single letter")
        
        # Convert to uppercase for consistency
        letter = letter.upper()
        
        # Check if already guessed
        if letter in self.guessed_letters:
            return letter in self.target.upper()
        
        # Add to guessed letters
        self.guessed_letters.add(letter)
        
        # Check if letter is in target
        is_correct = letter in self.target.upper()
        
        if not is_correct:
            self.lives -= 1
            
        # Update game state
        self._update_game_state()
        
        return is_correct

    def start_timer(self):
        """Start the guess timer."""
        self.timer_start = time.time()

    def get_remaining_time(self) -> Optional[int]:
        """Get remaining time in seconds, or None if timer not started."""
        if self.timer_start is None:
            return None
        
        elapsed = time.time() - self.timer_start
        remaining = self.timer_duration - elapsed
        return max(0, int(remaining + 0.5))  # Round up

    def is_time_up(self) -> bool:
        """Check if the timer has expired."""
        if self.timer_start is None:
            return False
        
        elapsed = time.time() - self.timer_start
        return elapsed >= self.timer_duration

    def handle_timeout(self):
        """Handle timeout scenario - reduces lives by 1."""
        self.lives -= 1
        self._update_game_state()
        self.timer_start = None  # Reset timer

    def get_guessed_letters(self) -> List[str]:
        """Get list of all guessed letters."""
        return sorted(list(self.guessed_letters))

    def get_target_answer(self) -> str:
        """Get the target word/phrase."""
        return self.target

    def _update_game_state(self):
        """Update the game state based on current conditions."""
        if self.lives <= 0:
            self.state = GameState.LOST
            return
            
        # Check if all letters have been guessed
        target_letters = set(char.upper() for char in self.target if char.isalpha())
        if target_letters.issubset(self.guessed_letters):
            self.state = GameState.WON 
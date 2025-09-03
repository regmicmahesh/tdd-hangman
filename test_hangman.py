"""
Test suite for the Hangman game.

This module contains comprehensive unit tests for the HangmanGame class,
testing all game mechanics including word selection, guess processing,
timer functionality, and game state management.
"""

import unittest
import time
from unittest.mock import patch
from hangman import HangmanGame, GameLevel, GameState


class TestHangmanGame(unittest.TestCase):
    """Test cases for the main HangmanGame class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test games for each level
        self.basic_game = HangmanGame(GameLevel.BASIC)
        self.intermediate_game = HangmanGame(GameLevel.INTERMEDIATE)

    def test_game_initialization_basic(self):
        """Test that basic game sets up correctly."""
        # Test that basic game sets up correctly
        game = HangmanGame(GameLevel.BASIC)
        self.assertEqual(game.level, GameLevel.BASIC)
        self.assertEqual(game.lives, 6)
        self.assertEqual(game.state, GameState.PLAYING)
        self.assertIsNotNone(game.target)
        self.assertFalse(" " in game.target)  # Basic should be single word

    def test_game_initialization_intermediate(self):
        """Test that intermediate game sets up correctly."""
        # Test that intermediate game sets up correctly
        game = HangmanGame(GameLevel.INTERMEDIATE)
        self.assertEqual(game.level, GameLevel.INTERMEDIATE)
        self.assertEqual(game.lives, 6)
        self.assertEqual(game.state, GameState.PLAYING)
        self.assertIsNotNone(game.target)

    def test_display_word_initial(self):
        """Test that word shows as underscores at the start."""
        # Test that word shows as underscores at the start
        with patch.object(self.basic_game, "target", "PYTHON"):
            display = self.basic_game.get_display_word()
            self.assertEqual(display, "_ _ _ _ _ _")

    def test_display_phrase_initial(self):
        """Test that phrases show underscores with proper spacing."""
        # Test that phrases show underscores with proper spacing
        with patch.object(self.intermediate_game, "target", "HELLO WORLD"):
            display = self.intermediate_game.get_display_word()
            self.assertEqual(display, "_ _ _ _ _   _ _ _ _ _")

    def test_valid_guess_letter(self):
        """Test guessing a letter that's in the word."""
        # Test guessing a letter that's in the word
        with patch.object(self.basic_game, "target", "PYTHON"):
            result = self.basic_game.make_guess("P")
            self.assertTrue(result)
            self.assertEqual(self.basic_game.get_display_word(), "P _ _ _ _ _")
            self.assertEqual(self.basic_game.lives, 6)

    def test_invalid_guess_letter(self):
        """Test guessing a letter that's NOT in the word."""
        # Test guessing a letter that's NOT in the word
        with patch.object(self.basic_game, "target", "PYTHON"):
            result = self.basic_game.make_guess("Z")
            self.assertFalse(result)
            self.assertEqual(self.basic_game.get_display_word(), "_ _ _ _ _ _")
            self.assertEqual(self.basic_game.lives, 5)  # Should lose a life

    def test_multiple_occurrences_revealed(self):
        """Test that all instances of a letter are revealed at once."""
        # Test that all instances of a letter are revealed at once
        with patch.object(self.basic_game, "target", "HELLO"):
            self.basic_game.make_guess("L")
            display = self.basic_game.get_display_word()
            self.assertEqual(display, "_ _ L L _")

    def test_game_won(self):
        """Test winning by guessing all letters."""
        # Test winning by guessing all letters
        with patch.object(self.basic_game, "target", "CAT"):
            self.basic_game.make_guess("C")
            self.basic_game.make_guess("A")
            self.basic_game.make_guess("T")
            self.assertEqual(self.basic_game.state, GameState.WON)

    def test_game_lost(self):
        """Test losing by running out of lives."""
        # Test losing by running out of lives
        with patch.object(self.basic_game, "target", "PYTHON"):
            wrong_letters = ["Z", "X", "Q", "W", "K", "J"]  # 6 wrong guesses
            for letter in wrong_letters:
                self.basic_game.make_guess(letter)
            self.assertEqual(self.basic_game.state, GameState.LOST)
            self.assertEqual(self.basic_game.lives, 0)

    def test_repeated_guess_same_result(self):
        """Test that guessing the same letter twice doesn't change anything."""
        # Test that guessing the same letter twice doesn't change anything
        with patch.object(self.basic_game, "target", "PYTHON"):
            result1 = self.basic_game.make_guess("P")
            lives_after_first = self.basic_game.lives

            result2 = self.basic_game.make_guess("P")  # Same guess again
            self.assertEqual(result1, result2)
            self.assertEqual(self.basic_game.lives, lives_after_first)

    def test_case_insensitive_guessing(self):
        """Test that lowercase letters work the same as uppercase."""
        # Test that lowercase letters work the same as uppercase
        with patch.object(self.basic_game, "target", "PYTHON"):
            result = self.basic_game.make_guess("p")  # lowercase
            self.assertTrue(result)
            self.assertEqual(self.basic_game.get_display_word(), "P _ _ _ _ _")

    def test_invalid_input_handling(self):
        """Test that invalid inputs raise errors."""
        # Test that invalid inputs raise errors
        with self.assertRaises(ValueError):
            self.basic_game.make_guess("")  # Empty string
        with self.assertRaises(ValueError):
            self.basic_game.make_guess("AB")  # Multiple letters
        with self.assertRaises(ValueError):
            self.basic_game.make_guess("1")  # Number

    def test_get_guessed_letters(self):
        """Test that we can get a list of guessed letters."""
        # Test that we can get a list of guessed letters
        with patch.object(self.basic_game, "target", "PYTHON"):
            self.basic_game.make_guess("P")
            self.basic_game.make_guess("Z")
            guessed = self.basic_game.get_guessed_letters()
            self.assertIn("P", guessed)
            self.assertIn("Z", guessed)

    def test_timer_start(self):
        """Test that timer starts correctly."""
        # Test that timer starts correctly
        self.basic_game.start_timer()
        self.assertIsNotNone(self.basic_game.timer_start)
        remaining = self.basic_game.get_remaining_time()
        self.assertTrue(0 < remaining <= 15)

    def test_timer_not_started(self):
        """Test timer behavior when not started."""
        # Test timer behavior when not started
        remaining = self.basic_game.get_remaining_time()
        self.assertIsNone(remaining)
        self.assertFalse(self.basic_game.is_time_up())

    def test_timer_timeout(self):
        """Test that timer correctly detects timeout."""
        # Test that timer correctly detects timeout
        with patch.object(self.basic_game, "timer_start", time.time() - 16):
            self.assertTrue(self.basic_game.is_time_up())
            self.assertEqual(self.basic_game.get_remaining_time(), 0)

    def test_handle_timeout_reduces_lives(self):
        """Test that timeout reduces lives."""
        # Test that timeout reduces lives
        initial_lives = self.basic_game.lives
        self.basic_game.handle_timeout()
        self.assertEqual(self.basic_game.lives, initial_lives - 1)

    def test_timeout_can_end_game(self):
        """Test that timeout can cause game to end."""
        # Test that timeout can cause game to end
        self.basic_game.lives = 1
        self.basic_game.handle_timeout()
        self.assertEqual(self.basic_game.state, GameState.LOST)

    def test_get_target_answer(self):
        """Test that we can get the target word/phrase."""
        # Test that we can get the target word/phrase
        target = self.basic_game.get_target_answer()
        self.assertEqual(target, self.basic_game.target)


class TestGameEnums(unittest.TestCase):
    """Test cases for the game enums (GameLevel and GameState)."""

    def test_game_level_enum(self):
        """Test that GameLevel enum values are correct."""
        self.assertEqual(GameLevel.BASIC.value, "basic")
        self.assertEqual(GameLevel.INTERMEDIATE.value, "intermediate")

    def test_game_state_enum(self):
        """Test that GameState enum values are correct."""
        self.assertEqual(GameState.PLAYING.value, "playing")
        self.assertEqual(GameState.WON.value, "won")
        self.assertEqual(GameState.LOST.value, "lost")


if __name__ == "__main__":
    unittest.main()

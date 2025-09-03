import unittest
import time
from unittest.mock import patch
from hangman import HangmanGame, GameLevel, GameState


class TestHangmanGame(unittest.TestCase):
    """Test cases for HangmanGame class following TDD approach."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.basic_game = HangmanGame(GameLevel.BASIC)
        self.intermediate_game = HangmanGame(GameLevel.INTERMEDIATE)

    def test_game_initialization_basic(self):
        """Test that basic game initializes correctly."""
        game = HangmanGame(GameLevel.BASIC)
        self.assertEqual(game.level, GameLevel.BASIC)
        self.assertEqual(game.lives, 6)
        self.assertEqual(game.state, GameState.PLAYING)
        self.assertIsNotNone(game.target)
        self.assertFalse(' ' in game.target)  # Basic should be single word

    def test_game_initialization_intermediate(self):
        """Test that intermediate game initializes correctly."""
        game = HangmanGame(GameLevel.INTERMEDIATE)
        self.assertEqual(game.level, GameLevel.INTERMEDIATE)
        self.assertEqual(game.lives, 6)
        self.assertEqual(game.state, GameState.PLAYING)
        self.assertIsNotNone(game.target)

    def test_display_word_initial(self):
        """Test that display word shows underscores initially."""
        with patch.object(self.basic_game, 'target', 'PYTHON'):
            display = self.basic_game.get_display_word()
            self.assertEqual(display, '_ _ _ _ _ _')

    def test_display_phrase_initial(self):
        """Test that display phrase shows underscores and spaces initially."""
        with patch.object(self.intermediate_game, 'target', 'HELLO WORLD'):
            display = self.intermediate_game.get_display_word()
            self.assertEqual(display, '_ _ _ _ _   _ _ _ _ _')

    def test_valid_guess_letter(self):
        """Test making a valid letter guess."""
        with patch.object(self.basic_game, 'target', 'PYTHON'):
            result = self.basic_game.make_guess('P')
            self.assertTrue(result)
            self.assertEqual(self.basic_game.get_display_word(), 'P _ _ _ _ _')
            self.assertEqual(self.basic_game.lives, 6)

    def test_invalid_guess_letter(self):
        """Test making an invalid letter guess."""
        with patch.object(self.basic_game, 'target', 'PYTHON'):
            result = self.basic_game.make_guess('Z')
            self.assertFalse(result)
            self.assertEqual(self.basic_game.get_display_word(), '_ _ _ _ _ _')
            self.assertEqual(self.basic_game.lives, 5)

    def test_multiple_occurrences_revealed(self):
        """Test that all occurrences of a letter are revealed."""
        with patch.object(self.basic_game, 'target', 'HELLO'):
            self.basic_game.make_guess('L')
            display = self.basic_game.get_display_word()
            self.assertEqual(display, '_ _ L L _')

    def test_game_won(self):
        """Test game state changes to won when word is guessed."""
        with patch.object(self.basic_game, 'target', 'CAT'):
            self.basic_game.make_guess('C')
            self.basic_game.make_guess('A')
            self.basic_game.make_guess('T')
            self.assertEqual(self.basic_game.state, GameState.WON)

    def test_game_lost(self):
        """Test game state changes to lost when lives reach zero."""
        with patch.object(self.basic_game, 'target', 'PYTHON'):
            # Make 6 wrong guesses
            wrong_letters = ['Z', 'X', 'Q', 'W', 'K', 'J']
            for letter in wrong_letters:
                self.basic_game.make_guess(letter)
            self.assertEqual(self.basic_game.state, GameState.LOST)
            self.assertEqual(self.basic_game.lives, 0)

    def test_repeated_guess_same_result(self):
        """Test that repeated guesses return same result."""
        with patch.object(self.basic_game, 'target', 'PYTHON'):
            result1 = self.basic_game.make_guess('P')
            lives_after_first = self.basic_game.lives
            
            result2 = self.basic_game.make_guess('P')
            self.assertEqual(result1, result2)
            self.assertEqual(self.basic_game.lives, lives_after_first)

    def test_case_insensitive_guessing(self):
        """Test that guessing is case insensitive."""
        with patch.object(self.basic_game, 'target', 'PYTHON'):
            result = self.basic_game.make_guess('p')
            self.assertTrue(result)
            self.assertEqual(self.basic_game.get_display_word(), 'P _ _ _ _ _')

    def test_invalid_input_handling(self):
        """Test handling of invalid input."""
        with self.assertRaises(ValueError):
            self.basic_game.make_guess('')
        with self.assertRaises(ValueError):
            self.basic_game.make_guess('AB')
        with self.assertRaises(ValueError):
            self.basic_game.make_guess('1')

    def test_get_guessed_letters(self):
        """Test tracking of guessed letters."""
        with patch.object(self.basic_game, 'target', 'PYTHON'):
            self.basic_game.make_guess('P')
            self.basic_game.make_guess('Z')
            guessed = self.basic_game.get_guessed_letters()
            self.assertIn('P', guessed)
            self.assertIn('Z', guessed)

    def test_timer_start(self):
        """Test that timer starts correctly."""
        self.basic_game.start_timer()
        self.assertIsNotNone(self.basic_game.timer_start)
        remaining = self.basic_game.get_remaining_time()
        self.assertTrue(0 < remaining <= 15)

    def test_timer_not_started(self):
        """Test timer behavior when not started."""
        remaining = self.basic_game.get_remaining_time()
        self.assertIsNone(remaining)
        self.assertFalse(self.basic_game.is_time_up())

    def test_timer_timeout(self):
        """Test timer timeout functionality."""
        with patch.object(self.basic_game, 'timer_start', time.time() - 16):
            self.assertTrue(self.basic_game.is_time_up())
            self.assertEqual(self.basic_game.get_remaining_time(), 0)

    def test_handle_timeout_reduces_lives(self):
        """Test that handling timeout reduces lives."""
        initial_lives = self.basic_game.lives
        self.basic_game.handle_timeout()
        self.assertEqual(self.basic_game.lives, initial_lives - 1)

    def test_timeout_can_end_game(self):
        """Test that timeout can end the game."""
        self.basic_game.lives = 1
        self.basic_game.handle_timeout()
        self.assertEqual(self.basic_game.state, GameState.LOST)

    def test_get_target_answer(self):
        """Test getting the target answer."""
        target = self.basic_game.get_target_answer()
        self.assertEqual(target, self.basic_game.target)


class TestGameEnums(unittest.TestCase):
    """Test cases for game enums."""

    def test_game_level_enum(self):
        """Test GameLevel enum values."""
        self.assertEqual(GameLevel.BASIC.value, "basic")
        self.assertEqual(GameLevel.INTERMEDIATE.value, "intermediate")

    def test_game_state_enum(self):
        """Test GameState enum values."""
        self.assertEqual(GameState.PLAYING.value, "playing")
        self.assertEqual(GameState.WON.value, "won")
        self.assertEqual(GameState.LOST.value, "lost")


if __name__ == '__main__':
    unittest.main() 
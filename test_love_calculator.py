"""
test_love_calculator.py
Unit tests for Love + Aura Calculator.
"""

import os
import unittest
import wave

from love_calculator import (
    calculate_love,
    calculate_aura,
    calculate_final_vibe,
    get_title,
    get_song,
    calculate_profile,
    VALID_GENDERS,
)


class TestLoveCalculator(unittest.TestCase):

    def test_love_calculation_bounds(self):
        """Test love percentage is always between 1 and 100 inclusive."""
        test_pairs = [
            ("A", "B"),
            ("Romeo", "Juliet"),
            ("Naruto", "Hinata"),
            ("Bonnie", "Clyde"),
            ("Rahul", "Anu"),
            ("SuperLongNameThatHasLotsOfLetters", "AnotherVeryLongNameForTesting"),
        ]
        for name1, name2 in test_pairs:
            love = calculate_love(name1, name2)
            self.assertGreaterEqual(love, 1)
            self.assertLessEqual(love, 100)

    def test_love_case_insensitivity_and_whitespace(self):
        """Test that casing and whitespace don't create erratic scores."""
        love1 = calculate_love("Romeo", "Juliet")
        love2 = calculate_love("  romeo  ", "JULIET")
        self.assertEqual(love1, love2)

    def test_aura_variation_bounds(self):
        """Aura should stay within [1, 100] and within +/-10 of love."""
        test_pairs = [
            ("Alice", "Bob"),
            ("Jack", "Rose"),
            ("Chandler", "Monica"),
            ("A", "Z"),
        ]
        for name1, name2 in test_pairs:
            love = calculate_love(name1, name2)
            aura = calculate_aura(love, name1, name2)
            self.assertGreaterEqual(aura, 1)
            self.assertLessEqual(aura, 100)
            self.assertLessEqual(abs(aura - love), 10)

    def test_final_vibe(self):
        """Final vibe should be 60% love + 40% aura truncated to int."""
        self.assertEqual(calculate_final_vibe(100, 100), 100)
        self.assertEqual(calculate_final_vibe(50, 50), 50)
        self.assertEqual(calculate_final_vibe(87, 91), int(87 * 0.60 + 91 * 0.40))  # 52.2 + 36.4 = 88.6 -> 88
        self.assertEqual(calculate_final_vibe(1, 1), 1)

    def test_titles(self):
        """Verify all title tier boundaries."""
        self.assertEqual(get_title(100), "LEGENDARY DUO")
        self.assertEqual(get_title(90), "LEGENDARY DUO")
        self.assertEqual(get_title(89), "MAIN CHARACTER DUO")
        self.assertEqual(get_title(80), "MAIN CHARACTER DUO")
        self.assertEqual(get_title(79), "DANGEROUSLY COMPATIBLE")
        self.assertEqual(get_title(70), "DANGEROUSLY COMPATIBLE")
        self.assertEqual(get_title(69), "INTERESTING DUO")
        self.assertEqual(get_title(60), "INTERESTING DUO")
        self.assertEqual(get_title(59), "FRIENDSHIP ARC")
        self.assertEqual(get_title(40), "FRIENDSHIP ARC")
        self.assertEqual(get_title(39), "NPC DUO")
        self.assertEqual(get_title(0), "NPC DUO")

    def test_song_selection(self):
        """Verify song selection mapping."""
        self.assertEqual(get_song(95), "song_90.wav")
        self.assertEqual(get_song(90), "song_90.wav")
        self.assertEqual(get_song(85), "song_80.wav")
        self.assertEqual(get_song(80), "song_80.wav")
        self.assertEqual(get_song(75), "song_70.wav")
        self.assertEqual(get_song(70), "song_70.wav")
        self.assertEqual(get_song(65), "song_60.wav")
        self.assertEqual(get_song(60), "song_60.wav")
        self.assertEqual(get_song(59), "song_low.wav")
        self.assertEqual(get_song(10), "song_low.wav")

    def test_calculate_profile(self):
        """Verify the full dictionary profile output structure."""
        profile = calculate_profile("Alice", "female", "Bob", "male")
        self.assertIn("name1", profile)
        self.assertIn("gender1", profile)
        self.assertIn("name2", profile)
        self.assertIn("gender2", profile)
        self.assertIn("love", profile)
        self.assertIn("aura", profile)
        self.assertIn("final_vibe", profile)
        self.assertIn("title", profile)
        self.assertIn("song", profile)
        self.assertEqual(profile["name1"], "Alice")
        self.assertEqual(profile["gender1"], "female")
        self.assertEqual(profile["name2"], "Bob")
        self.assertEqual(profile["gender2"], "male")

    def test_wav_files_exist_and_are_valid(self):
        """Verify that all 5 audio .wav files exist in the folder and are valid WAV files."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        required_songs = ["song_90.wav", "song_80.wav", "song_70.wav", "song_60.wav", "song_low.wav"]
        for song_name in required_songs:
            song_path = os.path.join(current_dir, song_name)
            self.assertTrue(os.path.exists(song_path), f"Missing audio file: {song_name}")
            with wave.open(song_path, "rb") as wf:
                self.assertGreater(wf.getnframes(), 0)
                self.assertEqual(wf.getframerate(), 44100)
                self.assertEqual(wf.getsampwidth(), 2)


if __name__ == "__main__":
    unittest.main()

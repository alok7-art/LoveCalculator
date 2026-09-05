"""
====================================================================
               LOVE + AURA CALCULATOR
====================================================================
A fun, entertainment-only Python program that calculates Love/Chemistry,
Aura, Final Vibe, Duo Title, and plays a soundtrack matching your vibe!
"""

import os
import sys
import time
import argparse

# Ensure standard output can handle UTF-8 / special characters on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Try importing winsound for Windows audio playback
try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False


VALID_GENDERS = ["male", "female", "other"]


def calculate_love(name1: str, name2: str) -> int:
    """
    Calculates Love / Chemistry percentage based on the combined names.
    Formula:
      combined = name1.lower() + name2.lower()
      total = sum(ord(c) * (i + 1))
      love = (total % 100) + 1  -> range [1, 100]
    """
    combined = name1.strip().lower() + name2.strip().lower()
    total = 0
    for i in range(len(combined)):
        total += ord(combined[i]) * (i + 1)
    love = (total % 100) + 1
    return love


def calculate_aura(love: int, name1: str, name2: str) -> int:
    """
    Calculates Aura percentage tied to the Love score with name-based variation.
    Formula:
      aura_variation = sum(ord(c) for c in combined) % 21 - 10  -> range [-10, +10]
      aura = love + aura_variation
      aura = max(1, min(100, aura))
    """
    combined = name1.strip().lower() + name2.strip().lower()
    aura_variation = sum(ord(c) for c in combined) % 21 - 10
    aura = love + aura_variation
    aura = max(1, min(100, aura))
    return aura


def calculate_final_vibe(love: int, aura: int) -> int:
    """
    Calculates Final Vibe score:
      60% Love/Chemistry + 40% Aura
    """
    return int((love * 0.60) + (aura * 0.40))


def get_title(score: int) -> str:
    """
    Returns funny duo title based on the Final Vibe score:
      90–100 = LEGENDARY DUO
      80–89  = MAIN CHARACTER DUO
      70–79  = DANGEROUSLY COMPATIBLE
      60–69  = INTERESTING DUO
      40–59  = FRIENDSHIP ARC
      0–39   = NPC DUO
    """
    if score >= 90:
        return "LEGENDARY DUO"
    elif score >= 80:
        return "MAIN CHARACTER DUO"
    elif score >= 70:
        return "DANGEROUSLY COMPATIBLE"
    elif score >= 60:
        return "INTERESTING DUO"
    elif score >= 40:
        return "FRIENDSHIP ARC"
    else:
        return "NPC DUO"


def get_song(love: int) -> str:
    """
    Returns the appropriate .wav filename based on the Love/Chemistry percentage:
      love >= 90 -> song_90.wav
      love >= 80 -> song_80.wav
      love >= 70 -> song_70.wav
      love >= 60 -> song_60.wav
      else       -> song_low.wav
    """
    if love >= 90:
        return "song_90.wav"
    elif love >= 80:
        return "song_80.wav"
    elif love >= 70:
        return "song_70.wav"
    elif love >= 60:
        return "song_60.wav"
    else:
        return "song_low.wav"


def calculate_profile(name1: str, gender1: str, name2: str, gender2: str) -> dict:
    """
    Runs the complete calculation pipeline and returns all metrics in a dictionary.
    Ready for easy integration into future web frameworks (Flask, FastAPI, Streamlit).
    """
    love = calculate_love(name1, name2)
    aura = calculate_aura(love, name1, name2)
    final_vibe = calculate_final_vibe(love, aura)
    title = get_title(final_vibe)
    song = get_song(love)

    return {
        "name1": name1.strip().title(),
        "gender1": gender1.strip().lower(),
        "name2": name2.strip().title(),
        "gender2": gender2.strip().lower(),
        "love": love,
        "aura": aura,
        "final_vibe": final_vibe,
        "title": title,
        "song": song,
    }


def play_song(song_filename: str, async_mode: bool = False):
    """
    Plays the selected .wav song using Windows winsound.
    Resolves the song path relative to the script directory.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    song_path = os.path.join(script_dir, song_filename)

    if not os.path.exists(song_path):
        print(f"\n[!] Audio file '{song_filename}' not found at {song_path}.")
        return

    if not WINSOUND_AVAILABLE:
        print(f"\n[i] winsound is only available on Windows. Skipping playback of '{song_filename}'.")
        return

    try:
        flags = winsound.SND_FILENAME
        if async_mode:
            flags |= winsound.SND_ASYNC
        print(f"\n▶ Playing your vibe soundtrack: {song_filename} ...")
        winsound.PlaySound(song_path, flags)
    except Exception as e:
        print(f"[!] Unable to play sound: {e}")


def prompt_gender(prompt_text: str) -> str:
    """Prompts the user for gender and ensures valid input."""
    while True:
        value = input(prompt_text).strip().lower()
        if value in VALID_GENDERS:
            return value
        # Allow short forms 'm', 'f', 'o'
        if value == "m":
            return "male"
        if value == "f":
            return "female"
        if value == "o":
            return "other"
        print("  [!] Invalid selection. Please enter: male, female, or other.")


def prompt_name(prompt_text: str) -> str:
    """Prompts the user for a non-empty name."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("  [!] Name cannot be empty. Please enter a valid name.")


def print_banner():
    banner = """
+-------------------------------------------------------------+
|                 LOVE + AURA CALCULATOR                      |
|         Find your Chemistry, Aura & Duo Vibe!               |
|        (For entertainment & fun purposes only)              |
+-------------------------------------------------------------+
"""
    print(banner)


def display_results(results: dict):
    """Displays formatted results matching the required output format."""
    print("\n" + "=" * 55)
    print(f"COUPLE: {results['name1']} ({results['gender1'].capitalize()}) + {results['name2']} ({results['gender2'].capitalize()})")
    print("-" * 55)
    print(f"LOVE / CHEMISTRY: {results['love']}%")
    print(f"AURA: {results['aura']}%")
    print(f"FINAL VIBE: {results['final_vibe']}%")
    print()
    print(f"TITLE: {results['title']}")
    print()
    print(f"YOUR SONG: {results['song']}")
    print("=" * 55)


def run_interactive():
    """Interactive CLI loop."""
    print_banner()

    while True:
        print("\n--- Enter Details ---")
        name1 = prompt_name("1. First person's name: ")
        gender1 = prompt_gender("2. First person's gender (male / female / other): ")

        name2 = prompt_name("3. Second person's name: ")
        gender2 = prompt_gender("4. Second person's gender (male / female / other): ")

        print("\nReading the cosmic vibrations and calculating aura...")
        time.sleep(0.8)

        results = calculate_profile(name1, gender1, name2, gender2)
        display_results(results)

        # Play song
        play_song(results["song"], async_mode=False)

        again = input("\nWould you like to calculate another couple? (y/n): ").strip().lower()
        if again not in ["y", "yes"]:
            print("\nThanks for using Love + Aura Calculator! Keep spreading good vibes!\n")
            break


def main():
    parser = argparse.ArgumentParser(description="Love + Aura Calculator")
    parser.add_argument("--name1", help="First person's name")
    parser.add_argument("--gender1", choices=VALID_GENDERS, help="First person's gender")
    parser.add_argument("--name2", help="Second person's name")
    parser.add_argument("--gender2", choices=VALID_GENDERS, help="Second person's gender")
    parser.add_argument("--no-sound", action="store_true", help="Disable audio playback")

    args = parser.parse_args()

    # If CLI arguments provided, run directly in non-interactive mode
    if args.name1 and args.gender1 and args.name2 and args.gender2:
        results = calculate_profile(args.name1, args.gender1, args.name2, args.gender2)
        display_results(results)
        if not args.no_sound:
            play_song(results["song"])
    else:
        run_interactive()


if __name__ == "__main__":
    main()

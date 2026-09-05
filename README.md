# 💖 Love + Aura Calculator

An interactive, entertainment-oriented Python application that calculates:
1. **Love / Chemistry Percentage**
2. **Aura Percentage**
3. **Final Vibe Score** (60% Love + 40% Aura)
4. **Funny Duo Title** (Legendary Duo, Main Character Duo, etc.)
5. **Vibe Soundtrack** (Plays the corresponding `.wav` audio track using Windows `winsound`)

> **Note:** For entertainment purposes only. Not a scientific measurement of love or compatibility!

---

## 📁 Project Structure

```text
LoveCalculator/
│
├── love_calculator.py     # Main interactive Python CLI program
├── generate_sounds.py     # Synthesizes the 5 retro/synth .wav audio files
├── test_love_calculator.py# Comprehensive unit tests (8 tests, 100% pass)
│
├── song_90.wav            # Tier 90-100: Triumphant celebratory fanfare
├── song_80.wav            # Tier 80-89:  Upbeat anime/hero lead groove
├── song_70.wav            # Tier 70-79:  Smooth romantic groove
├── song_60.wav            # Tier 60-69:  Quirky, playful bouncing tune
├── song_low.wav           # Tier 0-59:   Comical wah-wah sad trombone
│
├── index.html             # Bonus Web App prototype (ready for browser)
├── run_web.py             # 1-click web launcher (`python run_web.py`)
└── README.md              # Documentation
```

---

## 🚀 Quick Start (Python CLI)

### 1. Interactive Mode
Run the script from your terminal:

```bash
python love_calculator.py
```

You will be prompted to enter:
1. First person's name
2. First person's gender (`male`, `female`, or `other`)
3. Second person's name
4. Second person's gender (`male`, `female`, or `other`)

The program will compute the vibe, print the formatted card, and play the corresponding `.wav` soundtrack through your speakers!

### 2. Command-Line Arguments Mode
You can also run it directly with arguments (great for automated testing or scripting):

```bash
python love_calculator.py --name1 Alice --gender1 female --name2 Bob --gender2 male
```

To run silently without playing audio:
```bash
python love_calculator.py --name1 Alice --gender1 female --name2 Bob --gender2 male --no-sound
```

---

## 📊 Logic & Formulas

### 1. Love / Chemistry
```python
combined = name1.lower() + name2.lower()

total = 0
for i in range(len(combined)):
    total += ord(combined[i]) * (i + 1)

love = (total % 100) + 1  # 1% to 100%
```

### 2. Aura
Aura is tied directly to the Love score, with a small name-based variation between -10% and +10%:
```python
aura_variation = sum(ord(c) for c in combined) % 21 - 10

aura = love + aura_variation
aura = max(1, min(100, aura))
```

### 3. Final Vibe
Weighted combination:
```python
final_score = int((love * 0.60) + (aura * 0.40))
```

### 4. Funny Titles
| Final Vibe Range | Duo Title |
| :--- | :--- |
| **90 – 100** | `LEGENDARY DUO` |
| **80 – 89** | `MAIN CHARACTER DUO` |
| **70 – 79** | `DANGEROUSLY COMPATIBLE` |
| **60 – 69** | `INTERESTING DUO` |
| **40 – 59** | `FRIENDSHIP ARC` |
| **0 – 39** | `NPC DUO` |

### 5. Song Selection
| Love / Chemistry | Soundtrack File | Vibe Description |
| :--- | :--- | :--- |
| **>= 90%** | `song_90.wav` | Triumphant fanfare & sparkling chimes |
| **>= 80%** | `song_80.wav` | Energetic upbeat anime/hero theme |
| **>= 70%** | `song_70.wav` | Smooth romantic chords & groove |
| **>= 60%** | `song_60.wav` | Playful quirky bounce |
| **< 60%** | `song_low.wav` | Comical descending trombone wah-wah |

Sound is played using Windows native `winsound`:
```python
import winsound
winsound.PlaySound(song, winsound.SND_FILENAME)
```

---

## 🧪 Running Unit Tests

Run the test suite to verify calculation bounds, title assignments, and audio file integrity:

```bash
python -m unittest test_love_calculator.py -v
```

---

## 🌐 Future Web App

A prototype matching your web vision is already included in `index.html`!

To preview it in your browser:
```bash
python run_web.py
```
Or simply double-click [index.html](file:///C:/Users/ADMIN/.gemini/antigravity/scratch/LoveCalculator/index.html).

It displays:
- **RAHUL + ANU**
- **LOVE CHEMISTRY: 87%**
- **AURA: 91%**
- **FINAL VIBE: 88%**
- **MAIN CHARACTER DUO**
- **YOUR SONG: song_80.wav**
- **[ PLAY SONG ]** / **[ TRY AGAIN ]**

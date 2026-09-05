"""
generate_sounds.py
Synthesizes 5 fun, distinct retro/synth WAV audio tracks for the Love & Aura Calculator tiers:
- song_90.wav : Triumphant fanfare / celestial arpeggio (Legendary Duo)
- song_80.wav : Upbeat, energetic anime/hero synth arpeggio (Main Character Duo)
- song_70.wav : Smooth, seductive romantic groove (Dangerously Compatible)
- song_60.wav : Quirky, playful bouncing melody (Interesting Duo)
- song_low.wav: Comical descending wah-wah / sad trombone (NPC Duo / Friendship Arc)
"""

import math
import struct
import wave
import os

SAMPLE_RATE = 44100

def synthesize_note(freq, duration, volume=0.5, instrument='synth', vibrato_freq=5.0, vibrato_depth=0.0):
    """Generates audio samples for a note with attack, decay, sustain, release envelope."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    # ADSR Envelope lengths in samples
    attack = int(SAMPLE_RATE * 0.04)
    decay = int(SAMPLE_RATE * 0.08)
    sustain_level = 0.75
    release = int(SAMPLE_RATE * 0.1)
    
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        
        # Envelope calculation
        if i < attack:
            env = (i / attack)
        elif i < attack + decay:
            progress = (i - attack) / decay
            env = 1.0 - (1.0 - sustain_level) * progress
        elif i > n_samples - release:
            progress = (n_samples - i) / release
            env = sustain_level * progress
        else:
            env = sustain_level
            
        # Optional vibrato
        current_freq = freq
        if vibrato_depth > 0:
            current_freq += vibrato_depth * math.sin(2 * math.pi * vibrato_freq * t)
            
        # Harmonic sound design
        phase = 2 * math.pi * current_freq * t
        if instrument == 'bell':
            # Bell-like chime: fundamental + octaves + sparkle
            sample_val = (
                0.60 * math.sin(phase) +
                0.25 * math.sin(2 * phase) +
                0.10 * math.sin(3 * phase) +
                0.05 * math.sin(4.2 * phase)
            )
        elif instrument == 'hero_synth':
            # Warm brassy synth lead
            sample_val = (
                0.50 * math.sin(phase) +
                0.25 * math.sin(2 * phase) +
                0.15 * math.sin(3 * phase) +
                0.10 * math.sin(4 * phase)
            )
        elif instrument == 'smooth_vibe':
            # Warm electric piano / rhodes feel
            sample_val = (
                0.70 * math.sin(phase) +
                0.20 * math.sin(2 * phase) +
                0.10 * math.sin(3 * phase)
            )
        elif instrument == 'quirky':
            # Bouncy square-ish / 8-bit sound
            sine_val = math.sin(phase)
            sample_val = 0.5 * (1.0 if sine_val > 0 else -1.0) + 0.3 * math.sin(phase)
        elif instrument == 'trombone':
            # Sawtooth-like brass for sad trombone
            period = 1.0 / max(1.0, current_freq)
            phase_in_cycle = (t % period) / period
            sample_val = (2.0 * phase_in_cycle - 1.0) * 0.7 + 0.3 * math.sin(phase)
        else:
            sample_val = math.sin(phase)
            
        val = sample_val * env * volume
        # Clamp to 16-bit range
        clamped = max(-32767, min(32767, int(val * 32767)))
        samples.append(struct.pack('<h', clamped))
        
    return b''.join(samples)

def save_wav(filename, audio_bytes):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_bytes)
    print(f"Generated: {os.path.basename(filename)} ({len(audio_bytes)} bytes)")

def generate_all_sounds(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. song_90.wav: Legendary Duo (Fanfare & sparkling triumphant arpeggio)
    print("Synthesizing song_90.wav...")
    audio_90 = []
    notes_90 = [
        (523.25, 0.22, 'bell'),
        (659.25, 0.22, 'bell'),
        (783.99, 0.22, 'bell'),
        (987.77, 0.22, 'bell'),
        (1046.50, 0.35, 'bell'),
        (1318.51, 0.80, 'bell'),  # High E6 grand finale
    ]
    for freq, dur, inst in notes_90:
        audio_90.append(synthesize_note(freq, dur, volume=0.55, instrument=inst))
    save_wav(os.path.join(output_dir, "song_90.wav"), b''.join(audio_90))
    
    # 2. song_80.wav: Main Character Duo (Upbeat anime/hero lead groove)
    print("Synthesizing song_80.wav...")
    audio_80 = []
    notes_80 = [
        (440.00, 0.20, 'hero_synth'),
        (523.25, 0.20, 'hero_synth'),
        (587.33, 0.20, 'hero_synth'),
        (659.25, 0.28, 'hero_synth'),
        (783.99, 0.25, 'hero_synth'),
        (659.25, 0.70, 'hero_synth'),
    ]
    for freq, dur, inst in notes_80:
        audio_80.append(synthesize_note(freq, dur, volume=0.50, instrument=inst))
    save_wav(os.path.join(output_dir, "song_80.wav"), b''.join(audio_80))
    
    # 3. song_70.wav: Dangerously Compatible (Smooth romantic groove / spicy chords)
    print("Synthesizing song_70.wav...")
    audio_70 = []
    notes_70 = [
        (329.63, 0.28, 'smooth_vibe'),
        (392.00, 0.28, 'smooth_vibe'),
        (493.88, 0.28, 'smooth_vibe'),
        (587.33, 0.35, 'smooth_vibe'),
        (739.99, 0.75, 'smooth_vibe'),
    ]
    for freq, dur, inst in notes_70:
        audio_70.append(synthesize_note(freq, dur, volume=0.55, instrument=inst))
    save_wav(os.path.join(output_dir, "song_70.wav"), b''.join(audio_70))
    
    # 4. song_60.wav: Interesting Duo (Bouncy quirky chime)
    print("Synthesizing song_60.wav...")
    audio_60 = []
    notes_60 = [
        (261.63, 0.18, 'quirky'),
        (329.63, 0.18, 'quirky'),
        (392.00, 0.18, 'quirky'),
        (440.00, 0.18, 'quirky'),
        (523.25, 0.55, 'quirky'),
    ]
    for freq, dur, inst in notes_60:
        audio_60.append(synthesize_note(freq, dur, volume=0.45, instrument=inst))
    save_wav(os.path.join(output_dir, "song_60.wav"), b''.join(audio_60))
    
    # 5. song_low.wav: Friendship Arc / NPC Duo (Sad comical wah-wah trombone)
    print("Synthesizing song_low.wav...")
    audio_low = []
    notes_low = [
        (370.00, 0.35, 'trombone', 0.0),
        (349.23, 0.35, 'trombone', 0.0),
        (329.63, 0.35, 'trombone', 0.0),
        (311.13, 0.90, 'trombone', 4.0),  # Vibrato wobble on the sad final note
    ]
    for freq, dur, inst, vib in notes_low:
        audio_low.append(synthesize_note(freq, dur, volume=0.45, instrument=inst, vibrato_depth=vib))
    save_wav(os.path.join(output_dir, "song_low.wav"), b''.join(audio_low))
    print("All 5 sound files successfully created!")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_all_sounds(current_dir)

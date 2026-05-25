import re
import math

def analyze_rhythm(text):
    if not text:
        return {}

    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    lengths = [len(s.split()) for s in sentences]

    if not lengths:
        return {}

    # Detect repetitive sentence patterns (e.g. "The... The... The...")
    first_words = [s.split()[0].lower() for s in sentences if s.split()]
    repetition_streak = 0
    if len(first_words) >= 3:
        for i in range(len(first_words)-2):
            if first_words[i] == first_words[i+1] == first_words[i+2]:
                repetition_streak += 1

    # Reading momentum: based on sentence length variation
    # A mix of short and long sentences creates better rhythm
    avg = sum(lengths) / len(lengths)
    variance = sum((x - avg)**2 for x in lengths) / len(lengths)
    momentum_score = min(100, int(math.sqrt(variance) * 10)) if variance > 0 else 0

    return {
        'sentence_lengths': lengths,
        'repetitive_starts': repetition_streak,
        'momentum_score': momentum_score,
        'entropy': -sum((l/sum(lengths)) * math.log(l/sum(lengths)) for l in lengths) if sum(lengths) > 0 else 0
    }

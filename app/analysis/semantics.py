import re
from collections import Counter

FILLER_WORDS = {
    'basically', 'actually', 'literally', 'virtually', 'simply', 'just', 'very',
    'really', 'totally', 'honestly', 'seriously', 'obviously', 'essentially'
}

TRANSITION_WORDS = {
    'however', 'therefore', 'consequently', 'furthermore', 'moreover',
    'additionally', 'similarly', 'likewise', 'alternatively', 'nevertheless',
    'nonetheless', 'conversely', 'accordingly', 'consequently'
}

def analyze_semantics(text):
    if not text:
        return {}

    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)

    fillers = [w for w in words if w in FILLER_WORDS]
    transitions = [w for w in words if w in TRANSITION_WORDS]

    filler_density = (len(fillers) / word_count * 100) if word_count > 0 else 0
    transition_density = (len(transitions) / word_count * 100) if word_count > 0 else 0

    # Simple tone detection based on keyword sets (AI-free)
    persuasive_words = {'should', 'must', 'need', 'important', 'crucial', 'essential', 'proven', 'effective'}
    technical_words = {'system', 'data', 'algorithm', 'process', 'technical', 'analysis', 'implementation'}

    tone_scores = {
        'persuasive': len([w for w in words if w in persuasive_words]),
        'technical': len([w for w in words if w in technical_words]),
        'neutral': word_count - len(fillers) # simplified
    }

    dominant_tone = max(tone_scores, key=tone_scores.get) if word_count > 0 else 'neutral'

    return {
        'filler_words_count': len(fillers),
        'filler_density': round(filler_density, 2),
        'transition_words_count': len(transitions),
        'transition_density': round(transition_density, 2),
        'dominant_tone': dominant_tone,
        'tone_scores': tone_scores,
        'fillers_found': list(set(fillers))[:10]
    }

import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def get_seo_analysis(text):
    if not text:
        return {}

    words = [w.lower() for w in word_tokenize(text) if w.isalnum()]
    stop_words = set(stopwords.words('english'))
    keywords = [w for w in words if w not in stop_words]

    word_freq = Counter(keywords).most_common(20)
    total_keywords = len(keywords)

    density = {word: round((count / total_keywords) * 100, 2) for word, count in word_freq} if total_keywords > 0 else {}

    # Passive voice detection
    passive_voice_count = len(re.findall(r'\b(am|is|are|was|were|be|been|being)\b\s+([a-z]+ed|known|seen|found|given|taken|broken)\b', text, re.I))

    # Mock more realistic scores based on content length and variety
    geo_score = min(100, (len(words) // 8) + (passive_voice_count * 2))
    aeo_score = min(100, (text.count('?') * 10) + (len(words) // 12))
    aio_score = min(100, 100 - (passive_voice_count * 5) - (len(words) // 50))
    sxo_score = min(100, (len(set(words)) // 4) + (len(words) // 15))

    return {
        "word_freq": word_freq,
        "density": density,
        "passive_voice_count": passive_voice_count,
        "seo_score": min(100, (len(words) // 10) + (len(set(keywords)) // 5)),
        "geo_score": geo_score,
        "aeo_score": aeo_score,
        "aio_score": aio_score,
        "sxo_score": sxo_score
    }

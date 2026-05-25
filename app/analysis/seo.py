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

    # Advanced SEO: SERP Preview Logic (extract title/meta)
    title_match = re.search(r'#\s+(.+)', text)
    title = title_match.group(1) if title_match else (text[:60] + '...' if len(text) > 60 else text)

    meta_desc = text[:160] + '...' if len(text) > 160 else text
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    return {
        "word_freq": word_freq,
        "density": density,
        "passive_voice_count": passive_voice_count,
        "seo_score": min(100, (len(words) // 10) + (len(set(keywords)) // 5)),
        "serp_preview": {
            "title": title[:70],
            "description": meta_desc[:160],
            "slug": slug[:50]
        }
    }

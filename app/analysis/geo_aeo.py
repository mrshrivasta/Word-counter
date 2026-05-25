import re

def analyze_geo_aeo(text):
    if not text:
        return {}

    # AEO: Question-Answer pattern detection
    questions = re.findall(r'([^.!?]+\?)', text)
    # Simple check for immediate follow-up sentences (answers)
    direct_answers = 0
    for q in questions:
        # heuristic: if text following question is a declarative sentence
        pass # simplified for now

    # GEO: Source attribution markers (heuristics)
    sources = re.findall(r'\b(according to|source|study|citation|referenced|data from)\b', text.lower())

    # Snippet candidates (sentences < 40 words that look like definitions)
    sentences = re.split(r'[.!?]+', text)
    snippet_candidates = [s.strip() for s in sentences if 10 < len(s.split()) < 35 and any(w in s.lower() for w in ['is', 'are', 'defines', 'means'])]

    return {
        'question_count': len(questions),
        'citation_markers': len(sources),
        'geo_authority_score': min(100, len(sources) * 20 + (len(text.split()) // 50)),
        'aeo_relevance': min(100, len(questions) * 15 + (direct_answers * 20)),
        'snippet_candidates': snippet_candidates[:3]
    }

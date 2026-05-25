import re

def analyze_structure(text):
    if not text:
        return {}

    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    wall_of_text = [i for i, p in enumerate(paragraphs) if len(p.split()) > 150]

    # Heading detection (markdown style)
    headings = re.findall(r'^(#+)\s+(.+)$', text, re.MULTILINE)
    heading_tree = []
    for h in headings:
        heading_tree.append({'level': len(h[0]), 'text': h[1]})

    # Sentence variety
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    lengths = [len(s.split()) for s in sentences]

    variety_score = 0
    if lengths:
        variety_score = max(0, 100 - (max(lengths) - min(lengths))) # Simplified

    return {
        'paragraph_count': len(paragraphs),
        'wall_of_text_indices': wall_of_text,
        'headings': heading_tree,
        'heading_count': len(heading_tree),
        'sentence_lengths': lengths,
        'avg_sentence_length': sum(lengths)/len(lengths) if lengths else 0,
        'variety_score': variety_score
    }

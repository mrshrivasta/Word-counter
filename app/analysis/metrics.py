import re
import math
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize

def get_basic_stats(text):
    if not text:
        return {
            "word_count": 0, "char_count": 0, "char_no_spaces": 0,
            "sentence_count": 0, "paragraph_count": 0, "line_count": 0,
            "page_count": 0, "reading_time": 0, "speaking_time": 0,
            "unique_words": 0, "avg_word_length": 0, "avg_sentence_length": 0
        }

    words = word_tokenize(text)
    words_filtered = [w for w in words if w.isalnum()]
    sentences = sent_tokenize(text)
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    lines = text.split('\n')

    word_count = len(words_filtered)
    char_count = len(text)
    char_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\r", ""))
    sentence_count = len(sentences)
    paragraph_count = len(paragraphs)
    line_count = len(lines)

    page_count = math.ceil(word_count / 300) if word_count > 0 else 0
    reading_time = math.ceil(word_count / 225)
    speaking_time = math.ceil(word_count / 140)
    unique_words = len(set(w.lower() for w in words_filtered))

    avg_word_length = sum(len(w) for w in words_filtered) / word_count if word_count > 0 else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

    return {
        "word_count": word_count, "char_count": char_count,
        "char_no_spaces": char_no_spaces, "sentence_count": sentence_count,
        "paragraph_count": paragraph_count, "line_count": line_count,
        "page_count": page_count, "reading_time": reading_time,
        "speaking_time": speaking_time, "unique_words": unique_words,
        "avg_word_length": round(avg_word_length, 2),
        "avg_sentence_length": round(avg_sentence_length, 2)
    }

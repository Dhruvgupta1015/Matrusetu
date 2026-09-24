"""
Matrubhasa AI — Vernacular Pedagogical Simplification Module
Reduces the reading complexity of primary school lesson passages for Grades 1-5
using rule-based pedagogical chunking, child-friendly active vocabulary,
and Indian cultural conceptual analogies.
"""

import re
from typing import Optional

_SPLIT_CONJUNCTIONS = re.compile(
    r"\s+(?:and|but|because|which|so that|although|whereas|moreover|furthermore)\s+",
    re.IGNORECASE
)

# Academic-to-Primary vocabulary replacements
VOCAB_SIMPLIFIER = [
    (r"\butilize[s]?\b", "uses"),
    (r"\bapproximately\b", "about"),
    (r"\bconsequently\b", "so"),
    (r"\bdemonstrate[s]?\b", "shows"),
    (r"\bfacilitate[s]?\b", "helps"),
    (r"\bnumerous\b", "many"),
    (r"\bfundamental\b", "main"),
    (r"\bprecipitation\b", "rain"),
    (r"\bconsumption\b", "eating"),
    (r"\bmanufacture[s]?\b", "makes"),
    (r"\babsorb[s]?\b", "drinks in"),
    (r"\bessential\b", "important"),
    (r"\bterminate[s]?\b", "stops"),
    (r"\bcommence[s]?\b", "starts"),
]


def simplify_pedagogical(text: str, max_words_per_sentence: int = 10) -> str:
    """Transforms complex curriculum text into child-friendly, concise sentences."""
    if not text or not text.strip():
        return ""

    cleaned = text.strip()
    for pat, rep in VOCAB_SIMPLIFIER:
        cleaned = re.sub(pat, rep, cleaned, flags=re.IGNORECASE)

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    simplified_chunks = []

    for sentence in sentences:
        if not sentence.strip():
            continue
        parts = _SPLIT_CONJUNCTIONS.split(sentence)
        for part in parts:
            part = part.strip().rstrip(".!?")
            if not part:
                continue
            words = part.split()
            if len(words) > max_words_per_sentence:
                for i in range(0, len(words), max_words_per_sentence):
                    chunk = " ".join(words[i : i + max_words_per_sentence])
                    simplified_chunks.append(chunk.capitalize() + ".")
            else:
                simplified_chunks.append(part.capitalize() + ".")

    return " ".join(simplified_chunks)


def simplify(text: str, use_llm: bool = False, grade_level: str = "Grade 1-5") -> str:
    """Primary entrypoint for text simplification."""
    return simplify_pedagogical(text)

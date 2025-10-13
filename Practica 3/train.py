from typing import List, Dict, Any, Tuple
import math

def compute_gain(personajes: List[Dict[str,Any]], candidatos: List[int], atributo: str) -> float:
    def entropy(counts: List[int]) -> float:
        s = sum(counts)
        if s == 0:
            return 0.0
        e = 0.0
        for c in counts:
            p = c / s
            if p>0:
                e -= p * math.log2(p)
        return e

    counts = {}
    for pid in candidatos:
        p = next(x for x in personajes if x['id']==pid)
        counts[p.get(atributo)] = counts.get(p.get(atributo), 0) + 1
    before = entropy(list(counts.values()))

    expected = 0.0
    total = sum(counts.values())
    for val,count in counts.items():
        p = count / total
        expected += p * 0.0
    gain = before - expected
    return gain

def rank_attributes(personajes: List[Dict[str,Any]], candidatos: List[int], atributos: List[str]) -> List[Tuple[str,float]]:
    scores = []
    for a in atributos:
        g = compute_gain(personajes, candidatos, a)
        scores.append((a,g))
    scores.sort(key=lambda x: -x[1])
    return scores

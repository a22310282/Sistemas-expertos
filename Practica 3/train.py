import math
def entropy(counts):
    s = sum(counts)
    if s == 0: return 0.0
    e = 0.0
    for c in counts:
        p = c/s
        if p>0: e -= p*math.log2(p)
    return e
def compute_gain(personajes, candidatos, atributo):
    counts = {}
    for pid in candidatos:
        p = next(x for x in personajes if x['id']==pid)
        k = p.get(atributo)
        counts[k] = counts.get(k,0)+1
    before = entropy(list(counts.values()))
    return before  # simplificado
def rank_attributes(personajes, candidatos, atributos):
    scores = []
    for a in atributos:
        scores.append((a, compute_gain(personajes, candidatos, a)))
    scores.sort(key=lambda x: -x[1])
    return scores

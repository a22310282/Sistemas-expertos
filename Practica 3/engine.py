from typing import List, Dict, Any, Callable, Optional

class Rule:
    def __init__(self, name: str, condition: Callable[[Dict[str,Any]], bool], action: Callable[[Dict[str,Any]], None], priority: int = 0):
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority

class ExpertEngine:
    def __init__(self, personajes: List[Dict[str,Any]]):
        self.personajes = personajes
        self.candidatos = [p['id'] for p in personajes]
        self.hechos: Dict[str, Any] = {}
        self.rules: List[Rule] = []

    def reset(self):
        self.candidatos = [p['id'] for p in self.personajes]
        self.hechos = {}

    def register_rule(self, rule: Rule):
        self.rules.append(rule)
        self.rules.sort(key=lambda r: -r.priority)

    def apply_answer(self, atributo: str, valor: Any):
        self.hechos[atributo] = valor
        nuevos = []
        for pid in self.candidatos:
            p = next(x for x in self.personajes if x['id'] == pid)
            if p.get(atributo) == valor:
                nuevos.append(pid)
        self.candidatos = nuevos

    def forward_chain(self):
        changed = True
        while changed:
            changed = False
            for r in self.rules:
                if r.condition(self.hechos):
                    before = set(self.candidatos)
                    r.action(self.hechos)
                    if set(self.candidatos) != before:
                        changed = True

    def next_best_attribute(self, atributos: List[str]):
        mejores = None
        mejor_attr = None
        for a in atributos:
            if a in self.hechos:
                continue
            counts = {}
            for pid in self.candidatos:
                p = next(x for x in self.personajes if x['id']==pid)
                counts[p.get(a)] = counts.get(p.get(a), 0) + 1
            if not counts:
                continue
            vals = list(counts.values())
            score = max(vals) - min(vals)
            if mejores is None or score < mejores:
                mejores = score
                mejor_attr = a
        return mejor_attr

    def guess(self) -> Optional[int]:
        if len(self.candidatos) == 1:
            return self.candidatos[0]
        return None

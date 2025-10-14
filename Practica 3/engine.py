import json, os
from typing import List, Dict, Any, Optional
from train import rank_attributes

class ExpertEngine:
    def __init__(self, base_path: str):
        self.base_path = base_path
        with open(base_path, 'r', encoding='utf-8') as f:
            self.personajes: List[Dict[str, Any]] = json.load(f)
        self.reset()

    def reset(self):
        self.candidatos = [p['id'] for p in self.personajes]
        self.hechos: Dict[str, Any] = {}
        self.asked = []

    def apply_answer(self, atributo: str, valor: Any):
        self.hechos[atributo] = valor
        if atributo not in self.asked:
            self.asked.append(atributo)
        nuevos = []
        # valor None => no filtrar
        if valor is None:
            return
        for pid in self.candidatos:
            p = next(x for x in self.personajes if x['id'] == pid)
            pv = p.get(atributo)
            if isinstance(pv, bool):
                if isinstance(valor, bool) and pv == valor:
                    nuevos.append(pid)
            else:
                if isinstance(valor, str) and str(pv).lower() == valor.lower():
                    nuevos.append(pid)
        if nuevos:
            self.candidatos = nuevos

    def next_question(self, atributos: List[str]):
        candidates = [a for a in atributos if a not in self.asked]
        if not candidates:
            return None
        scores = rank_attributes(self.personajes, self.candidatos, candidates)
        return scores[0][0] if scores else None

    def guess(self) -> Optional[int]:
        if len(self.candidatos) == 1:
            return self.candidatos[0]
        scores = []
        for pid in self.candidatos:
            p = next(x for x in self.personajes if x['id']==pid)
            score = 0
            for a,v in self.hechos.items():
                if v is None:
                    continue
                pv = p.get(a)
                if isinstance(pv, bool) and isinstance(v, bool):
                    if pv == v: score += 1
                else:
                    if isinstance(v, str) and str(pv).lower() == v.lower(): score += 1
            scores.append((pid, score))
        scores.sort(key=lambda x: -x[1])
        return scores[0][0] if scores else None

    def add_new_character(self, nuevo: Dict[str, Any]) -> Dict[str, Any]:
        """Append a new character to the JSON base and memory."""
        # assign new unique id
        used_ids = {p['id'] for p in self.personajes}
        new_id = 1
        while new_id in used_ids:
            new_id += 1
        nuevo['id'] = new_id
        self.personajes.append(nuevo)
        # persist
        with open(self.base_path, 'w', encoding='utf-8') as f:
            json.dump(self.personajes, f, ensure_ascii=False, indent=2)
        # refresh candidates pool to include new one next game
        self.reset()
        return nuevo

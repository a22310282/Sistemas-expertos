import json
from typing import List, Dict, Any, Optional, Tuple

ATTR_ORDER = [
    "aparece_en_grupo","usa_ropa","tiene_cabello","es_humanoide",
    "es_niño","es_comico","es_valiente","tiene_poderes",
    "es_robot","es_extraterrestre","es_villano","es_protagonista"
]

class ExpertEngine:
    def __init__(self, base_path: str):
        self.base_path = base_path
        with open(base_path, 'r', encoding='utf-8') as f:
            self.personajes: List[Dict[str, Any]] = json.load(f)
        self.reset()

    def reset(self):
        self.candidatos = [p['id'] for p in self.personajes]
        self.hechos: Dict[str, Optional[bool]] = {}
        self.asked: List[str] = []
        self.history: List[Tuple[List[int], Dict[str, Optional[bool]], List[str]]] = []
        self.intentos_adivinar = 0
        self.preguntas_hechas = 0

    def snapshot(self):
        self.history.append((self.candidatos.copy(), self.hechos.copy(), self.asked.copy()))

    def undo(self) -> bool:
        if not self.history:
            return False
        cand, hechos, asked = self.history.pop()
        self.candidatos = cand
        self.hechos = hechos
        self.asked = asked
        if self.preguntas_hechas > 0:
            self.preguntas_hechas -= 1
        return True

    def apply_answer(self, atributo: str, valor: Optional[bool]):
        self.snapshot()
        self.hechos[atributo] = valor
        if atributo not in self.asked:
            self.asked.append(atributo)
        if valor is None:
            return
        nuevos: List[int] = []
        for pid in self.candidatos:
            p = next(x for x in self.personajes if x['id']==pid)
            pv = bool(p.get(atributo, False))
            if pv == valor:
                nuevos.append(pid)
        if nuevos:
            self.candidatos = nuevos

    def next_question(self, atributos: List[str]) -> Optional[str]:
        candidates = [a for a in ATTR_ORDER if a in atributos and a not in self.asked]
        if not candidates:
            return None
        return candidates[0]

    def top_candidate(self) -> Optional[int]:
        if not self.candidatos:
            return None
        scores = []
        for pid in self.candidatos:
            p = next(x for x in self.personajes if x['id']==pid)
            score = 0
            for a,v in self.hechos.items():
                if v is None: continue
                if bool(p.get(a, False)) == v: score += 1
            scores.append((pid, score))
        scores.sort(key=lambda x: -x[1])
        return scores[0][0]

    def guess(self) -> Optional[int]:
        return self.top_candidate()

    def add_new_character(self, nuevo: Dict[str, Any]) -> Dict[str, Any]:
        used_ids = {p['id'] for p in self.personajes}
        new_id = 1
        while new_id in used_ids:
            new_id += 1
        nuevo['id'] = new_id
        self.personajes.append(nuevo)
        with open(self.base_path, 'w', encoding='utf-8') as f:
            json.dump(self.personajes, f, ensure_ascii=False, indent=2)
        self.reset()
        return nuevo

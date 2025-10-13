import argparse
from engine import ExpertEngine, Rule
from utils import PERSONAJES, ATRIBUTOS
from cbr import CaseRepository
from train import rank_attributes

def human_vs_ai():
    engine = ExpertEngine(PERSONAJES)
    case_repo = CaseRepository()
    initial_ids = engine.candidatos.copy()
    print('Piensa en un personaje del conjunto:')
    while True:
        if len(engine.candidatos) == 1:
            pid = engine.candidatos[0]
            p = next(x for x in PERSONAJES if x['id']==pid)
            print(f'Creo que tu personaje es: {p["nombre"]} (id={pid})')
            ok = input('¿Correcto? (s/n): ').strip().lower()
            result = (ok=='s')
            case_repo.save_case({'initial_ids': initial_ids, 'questions': [], 'target': pid, 'result': result, 'num_questions': 0})
            break
        attr = engine.next_best_attribute(ATRIBUTOS)
        if attr is None:
            print('No sé qué preguntar más, adivinaré al azar.')
            pid = engine.candidatos[0]
            p = next(x for x in PERSONAJES if x['id']==pid)
            print(f'Creo que es: {p["nombre"]}')
            break
        ans = input(f'¿Tu personaje tiene {attr}? (escribe el valor): ').strip()
        val = ans
        if ans.lower() in ['true','t','s','si','sí']:
            val = True
        elif ans.lower() in ['false','f','n','no']:
            val = False
        engine.apply_answer(attr, val)

def ai_vs_ai():
    print('Modo ai_vs_ai: por implementar.')

def train():
    repo = CaseRepository()
    casos = repo.load_cases()
    engine = ExpertEngine(PERSONAJES)
    scores = rank_attributes(PERSONAJES, engine.candidatos, ATRIBUTOS)
    print('Ranking inicial de atributos por ganancia estimada:')
    for a,g in scores:
        print(f"{a}: {g:.4f}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['human_vs_ai','ai_vs_ai','train'], default='human_vs_ai')
    args = parser.parse_args()
    if args.mode == 'human_vs_ai':
        human_vs_ai()
    elif args.mode == 'ai_vs_ai':
        ai_vs_ai()
    elif args.mode == 'train':
        train()

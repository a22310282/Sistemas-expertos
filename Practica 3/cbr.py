import csv
from typing import List, Dict, Any

class CaseRepository:
    def __init__(self, filename: str = 'cases.csv'):
        self.filename = filename

    def save_case(self, case: Dict[str, Any]):
        header = ['initial_ids','questions','target','result','num_questions']
        try:
            with open(self.filename, 'x', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
        except FileExistsError:
            pass
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                '|'.join(map(str, case.get('initial_ids',[]))),
                '|'.join([f"{a}={v}" for a,v in case.get('questions',[])]),
                case.get('target',''),
                int(case.get('result', False)),
                case.get('num_questions', 0)
            ])

    def load_cases(self) -> List[Dict[str, Any]]:
        casos = []
        try:
            with open(self.filename, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    casos.append(row)
        except FileNotFoundError:
            pass
        return casos

    def retrieve_similar(self, initial_ids: List[int]) -> List[Dict[str, Any]]:
        similar = []
        for c in self.load_cases():
            ids = [int(x) for x in c['initial_ids'].split('|')] if c.get('initial_ids') else []
            overlap = len(set(ids).intersection(set(initial_ids)))
            similar.append((overlap, c))
        similar.sort(key=lambda x: -x[0])
        return [c for _,c in similar]

import json
from typing import Dict, Any, List

class CaseRepositoryJSON:
    def __init__(self, filename: str):
        self.filename = filename
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.cases = json.load(f)
        except FileNotFoundError:
            self.cases = []

    def save_case(self, case: Dict[str, Any]):
        self.cases.append(case)
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.cases, f, ensure_ascii=False, indent=2)

    def retrieve_all(self) -> List[Dict[str, Any]]:
        return self.cases

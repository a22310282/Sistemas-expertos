import os, json
BASE_FILE = os.path.join(os.path.dirname(__file__), 'base_conocimiento.json')
CASOS_FILE = os.path.join(os.path.dirname(__file__), 'casos.json')
ICONS_DIR = os.path.join(os.path.dirname(__file__), 'icons')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

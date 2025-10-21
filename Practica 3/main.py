import tkinter as tk
from tkinter import messagebox, simpledialog
import os, random
from engine import ExpertEngine, ATTR_ORDER
from cbr import CaseRepositoryJSON
from utils import BASE_FILE, ICONS_DIR
from PIL import Image, ImageTk, ImageDraw, ImageFont

ATRIBUTOS = ATTR_ORDER[:]

CN_BLUE = '#009BFF'
CN_BLACK = '#000000'
CN_WHITE = '#FFFFFF'

def generate_icon(path, name, color=(180,180,255)):
    img = Image.new('RGBA', (180,180), color+(255,))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', 20)
    except Exception:
        font = ImageFont.load_default()
    words = name.split()
    lines, line = [], ''
    for w in words:
        if len((line+' '+w).strip()) <= 12: line = (line+' '+w).strip()
        else: lines.append(line); line = w
    if line: lines.append(line)
    y = 80 - (len(lines)*12)
    for ln in lines[:3]:
        w,h = draw.textsize(ln, font=font)
        draw.text(((180-w)/2, y), ln, fill=(0,0,0), font=font)
        y += h+4
    img.save(path)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('ADIVINA QUIÉN — CARTOON NETWORK (2000–2015)')
        self.root.configure(bg=CN_WHITE)
        self.engine = ExpertEngine(BASE_FILE)
        self.repo = CaseRepositoryJSON(os.path.join(os.path.dirname(__file__), 'casos.json'))
        self.max_preguntas_totales = 20

        # Splash
        self.splash = tk.Frame(root, bg=CN_WHITE)
        self.splash.pack(fill='both', expand=True)
        title = tk.Label(self.splash, text='ADIVINA QUIÉN', fg=CN_BLACK, bg=CN_WHITE, font=('Arial Black', 28))
        subtitle = tk.Label(self.splash, text='CARTOON NETWORK (2000–2015)', fg=CN_BLUE, bg=CN_WHITE, font=('Arial', 16, 'bold'))
        start_btn = tk.Button(self.splash, text='Comenzar partida', bg=CN_BLUE, fg=CN_WHITE, font=('Arial', 14, 'bold'), command=self.start_ui, activebackground='#0DB3FF', activeforeground=CN_WHITE, padx=20, pady=10, relief='flat')
        title.pack(pady=(40,10)); subtitle.pack(pady=(0,30)); start_btn.pack()

        # Main
        self.main = tk.Frame(root, bg=CN_WHITE)
        self.header = tk.Label(self.main, text='Piensa en un personaje \n Responde Sí/No', fg=CN_BLACK, bg=CN_WHITE, font=('Arial', 14))
        self.header.pack(pady=10)
        btns = tk.Frame(self.main, bg=CN_WHITE); btns.pack(pady=5)
        self.btn_yes = tk.Button(btns, text='Sí', width=10, command=lambda: self.answer(True), bg=CN_BLUE, fg=CN_WHITE)
        self.btn_no = tk.Button(btns, text='No', width=10, command=lambda: self.answer(False), bg=CN_BLACK, fg=CN_WHITE)
        self.btn_unknown = tk.Button(btns, text='No sé', width=10, command=lambda: self.answer(None), bg='#666666', fg=CN_WHITE)
        self.btn_back = tk.Button(btns, text='↩ Regresar', width=12, command=self.go_back, bg='#CCCCCC', fg=CN_BLACK)
        self.btn_yes.pack(side='left', padx=6); self.btn_no.pack(side='left', padx=6); self.btn_unknown.pack(side='left', padx=6); self.btn_back.pack(side='left', padx=6)

        self.canvas = tk.Canvas(self.main, width=720, height=280, bg=CN_WHITE, highlightthickness=0)
        self.canvas.pack(pady=10)
        self.icon_images = {}

        self.question_label = tk.Label(self.main, text='', fg=CN_BLACK, bg=CN_WHITE, font=('Arial', 13, 'bold'))
        self.question_label.pack(pady=(0,8))
        self.counter_label = tk.Label(self.main, text='0 / 20 preguntas — Intentos: 0/3', fg='#333333', bg=CN_WHITE, font=('Arial', 10))
        self.counter_label.pack()

        self.current_attr = None

    def start_ui(self):
        self.splash.pack_forget()
        self.main.pack(fill='both', expand=True)
        self.reset_game()
        self.next_question()

    def reset_game(self):
        self.engine.reset()
        self.canvas.delete('all')
        self.icon_images = {}
        self.current_attr = None
        self.update_counter()

    def update_counter(self):
        self.counter_label.config(text=f"{self.engine.preguntas_hechas} / {self.max_preguntas_totales} preguntas — Intentos: {self.engine.intentos_adivinar}/3")

    def make_question_text(self, attr):
        mapping = {
            'usa_ropa': '¿Tu personaje usa ropa?',
            'tiene_poderes': '¿Tu personaje tiene poderes?',
            'es_niño': '¿Tu personaje es un niño/niña?',
            'es_villano': '¿Tu personaje es villano?',
            'es_protagonista': '¿Es protagonista en su serie?',
            'tiene_cabello': '¿Tu personaje tiene cabello?',
            'es_humanoide': '¿Tu personaje es humanoide?',
            'es_extraterrestre': '¿Tu personaje es extraterrestre?',
            'es_robot': '¿Tu personaje es un robot?',
            'aparece_en_grupo': '¿Tu personaje aparece en un grupo/equipo?',
            'es_comico': '¿Tu personaje es principalmente cómico?',
            'es_valiente': '¿Tu personaje es valiente?'
        }
        return mapping.get(attr, f'Pregunta sobre {attr}')

    def answer(self, val):
        if self.current_attr is None:
            return
        if self.engine.preguntas_hechas >= self.max_preguntas_totales and len(self.engine.candidatos) > 1:
            self.try_guess_or_finish()
            return
        self.engine.apply_answer(self.current_attr, val)
        self.engine.preguntas_hechas += 1
        self.update_counter()
        if len(self.engine.candidatos) <= 3 or self.engine.preguntas_hechas >= self.max_preguntas_totales:
            self.try_guess_or_finish()
            return
        self.next_question()

    def go_back(self):
        if self.engine.undo():
            self.update_counter()
            self.update_candidate_icons()
            self.next_question(set_new=False)
        else:
            messagebox.showinfo('Regresar', 'No hay pasos anteriores que deshacer.')

    def update_candidate_icons(self):
        self.canvas.delete('all')
        x,y = 10,10; per_row = 8; idx = 0
        for pid in self.engine.candidatos:
            p = next(x for x in self.engine.personajes if x['id']==pid)
            name_key = p['nombre'].replace(' ','_')
            path = os.path.join(ICONS_DIR, f'{name_key}.png')
            if os.path.exists(path):
                img = Image.open(path).resize((80,80))
                tkimg = ImageTk.PhotoImage(img); self.icon_images[f'{pid}'] = tkimg
                self.canvas.create_image(x+40,y+40,image=tkimg)
            self.canvas.create_text(x+40,y+95,text=p['nombre'])
            x += 90; idx += 1
            if idx % per_row == 0:
                x = 10; y += 120

    def next_question(self, set_new=True):
        if self.engine.preguntas_hechas >= self.max_preguntas_totales or len(self.engine.candidatos) <= 1:
            self.try_guess_or_finish(); return
        attr = self.engine.next_question(ATRIBUTOS)
        self.current_attr = attr
        if attr is None:
            self.try_guess_or_finish(); return
        q = self.make_question_text(attr)
        self.question_label.config(text=q)
        self.update_candidate_icons()

    def try_guess_or_finish(self):
        if self.engine.intentos_adivinar >= 3:
            self.learn_new_character()
            self.reset_game()
            self.next_question()
            return
        pid = self.engine.guess()
        if pid is None and self.engine.candidatos:
            pid = random.choice(self.engine.candidatos)
        if pid is None:
            self.learn_new_character()
            self.reset_game()
            self.next_question()
            return
        p = next(x for x in self.engine.personajes if x['id']==pid)
        ok = messagebox.askyesno('Adivinar', f'Intento {self.engine.intentos_adivinar+1}/3: ¿Tu personaje es {p["nombre"]}?')
        self.engine.intentos_adivinar += 1
        self.update_counter()
        if ok:
            self.save_case(pid, True)
            messagebox.showinfo('¡Genial!', '¡He adivinado tu personaje!')
            self.reset_game(); self.next_question()
        else:
            if pid in self.engine.candidatos:
                self.engine.candidatos.remove(pid)
            self.save_case(pid, False)
            if len(self.engine.candidatos) > 0 and self.engine.preguntas_hechas < self.max_preguntas_totales:
                self.next_question()
            else:
                self.try_guess_or_finish()

    def save_case(self, guessed_id, result):
        case = {
            'questions': self.engine.asked[:],
            'facts': self.engine.hechos.copy(),
            'guessed': guessed_id,
            'result': result,
            'num_questions': self.engine.preguntas_hechas,
            'guess_attempts': self.engine.intentos_adivinar
        }
        self.repo.save_case(case)

    def learn_new_character(self):
        name = simpledialog.askstring('Aprender', 'No pude adivinar después de 3 intentos.\n¿En quién estabas pensando? Escribe el nombre exacto:')
        if not name:
            messagebox.showinfo('Aprender', 'Sin nombre, no puedo aprender el personaje.')
            return
        nuevo = {'nombre': name}
        for a in ATRIBUTOS:
            v = self.engine.hechos.get(a, None)
            nuevo[a] = bool(v) if v is not None else False
        added = self.engine.add_new_character(nuevo)
        path = os.path.join(ICONS_DIR, f"{added['nombre'].replace(' ','_')}.png")
        h = abs(hash(added['nombre']))
        color = (100 + (h % 156), 100 + ((h//7) % 156), 100 + ((h//13) % 156))
        generate_icon(path, added['nombre'], color=color)
        messagebox.showinfo('Aprendido', f"He aprendido un nuevo personaje: {added['nombre']}. ¡Gracias!")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

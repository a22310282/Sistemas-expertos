import tkinter as tk
from tkinter import messagebox, simpledialog
import os, random
from engine import ExpertEngine, ATTR_ORDER
from cbr import CaseRepositoryJSON
from utils import BASE_FILE

ATRIBUTOS = ATTR_ORDER[:]

BG_SOFT = '#F8FAFC'
TXT_MAIN = '#1E1E1E'
BLUE = '#4DB5FF'
BLUE_ACTIVE = '#66C4FF'
GRAY_BTN = '#D9D9D9'
TXT_DIM = '#444444'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('ADIVINA QUIÉN — CARTOON NETWORK (2000–2015)')
        self.root.configure(bg=BG_SOFT)
        self.engine = ExpertEngine(BASE_FILE)
        self.repo = CaseRepositoryJSON(os.path.join(os.path.dirname(__file__), 'casos.json'))
        self.max_preguntas_totales = 20

        # Splash
        self.splash = tk.Frame(root, bg=BG_SOFT)
        self.splash.pack(fill='both', expand=True)
        title = tk.Label(self.splash, text='ADIVINA QUIÉN', fg=TXT_MAIN, bg=BG_SOFT, font=('Arial Black', 28))
        subtitle = tk.Label(self.splash, text='CARTOON NETWORK (2000–2015)', fg=BLUE, bg=BG_SOFT, font=('Arial', 16, 'bold'))
        start_btn = tk.Button(self.splash, text='Comenzar partida', bg=BLUE, fg='white', font=('Arial', 14, 'bold'),
                              command=self.to_instructions, activebackground=BLUE_ACTIVE, activeforeground='white',
                              padx=20, pady=10, relief='flat')
        title.pack(pady=(40,10)); subtitle.pack(pady=(0,30)); start_btn.pack()

        # Instructions
        self.instructions = tk.Frame(root, bg=BG_SOFT)
        # Draw simple CN logo with Canvas: [C][N] squares
        logo = tk.Canvas(self.instructions, width=180, height=90, bg=BG_SOFT, highlightthickness=0)
        logo.pack(pady=(40,10))
        logo.create_rectangle(0,0,90,90, fill='#000000', outline='#000000')
        logo.create_rectangle(90,0,180,90, fill='#FFFFFF', outline='#000000')
        logo.create_text(45,45, text='C', fill='#FFFFFF', font=('Arial Black', 36))
        logo.create_text(135,45, text='N', fill='#000000', font=('Arial Black', 36))
        msg = ('Piensa en un personaje de Cartoon Network (2000–2015).\n'
               'Responde las siguientes preguntas con Sí o No,\n'
               'y el simulador intentará adivinarlo.')
        text_lbl = tk.Label(self.instructions, text=msg, fg=TXT_MAIN, bg=BG_SOFT, font=('Arial', 14), justify='center')
        btns = tk.Frame(self.instructions, bg=BG_SOFT)
        btn_start = tk.Button(btns, text='Empezar preguntas', bg=BLUE, fg='white', font=('Arial', 12, 'bold'),
                              command=self.start_game, activebackground=BLUE_ACTIVE, activeforeground='white', padx=18, pady=8, relief='flat')
        btn_back_home = tk.Button(btns, text='Volver al inicio', bg=GRAY_BTN, fg=TXT_MAIN, font=('Arial', 12),
                                  command=self.to_splash, padx=18, pady=8, relief='flat')
        text_lbl.pack(pady=(0,10))
        btns.pack(pady=10)
        btn_start.pack(side='left', padx=6)
        btn_back_home.pack(side='left', padx=6)

        # Game
        self.main = tk.Frame(root, bg=BG_SOFT)
        self.header = tk.Label(self.main, text='Responde Sí / No / No sé', fg=TXT_MAIN, bg=BG_SOFT, font=('Arial', 14))
        self.header.pack(pady=10)
        btns2 = tk.Frame(self.main, bg=BG_SOFT); btns2.pack(pady=5)
        self.btn_yes = tk.Button(btns2, text='Sí', width=12, command=lambda: self.answer(True), bg=BLUE, fg='white', relief='flat')
        self.btn_no = tk.Button(btns2, text='No', width=12, command=lambda: self.answer(False), bg=TXT_MAIN, fg='white', relief='flat')
        self.btn_unknown = tk.Button(btns2, text='No sé', width=12, command=lambda: self.answer(None), bg='#666666', fg='white', relief='flat')
        self.btn_back = tk.Button(btns2, text='↩ Regresar', width=12, command=self.go_back, bg=GRAY_BTN, fg=TXT_MAIN, relief='flat')
        self.btn_yes.pack(side='left', padx=6); self.btn_no.pack(side='left', padx=6); self.btn_unknown.pack(side='left', padx=6); self.btn_back.pack(side='left', padx=6)

        self.question_label = tk.Label(self.main, text='', fg=TXT_MAIN, bg=BG_SOFT, font=('Arial', 13, 'bold'))
        self.question_label.pack(pady=(10,8))
        self.counter_label = tk.Label(self.main, text='0 / 20 preguntas — Intentos: 0/3', fg=TXT_DIM, bg=BG_SOFT, font=('Arial', 10))
        self.counter_label.pack()

        self.current_attr = None

    # Navigation
    def to_instructions(self):
        self.splash.pack_forget()
        self.instructions.pack(fill='both', expand=True)

    def to_splash(self):
        self.instructions.pack_forget()
        self.splash.pack(fill='both', expand=True)

    def start_game(self):
        self.instructions.pack_forget()
        self.main.pack(fill='both', expand=True)
        self.reset_game()
        self.next_question()

    # Game logic
    def reset_game(self):
        self.engine.reset()
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
            self.next_question(set_new=False)
        else:
            messagebox.showinfo('Regresar', 'No hay pasos anteriores que deshacer.')

    def next_question(self, set_new=True):
        if self.engine.preguntas_hechas >= self.max_preguntas_totales or len(self.engine.candidatos) <= 1:
            self.try_guess_or_finish(); return
        attr = self.engine.next_question(ATRIBUTOS)
        self.current_attr = attr
        if attr is None:
            self.try_guess_or_finish(); return
        q = self.make_question_text(attr)
        self.question_label.config(text=q)

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
        messagebox.showinfo('Aprendido', f"He aprendido un nuevo personaje: {added['nombre']}. ¡Gracias!")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

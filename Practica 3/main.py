import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os, json, random
from engine import ExpertEngine
from cbr import CaseRepositoryJSON
from utils import BASE_FILE, ICONS_DIR
from PIL import Image, ImageTk, ImageDraw, ImageFont

ATRIBUTOS = ['especie','color','usa_ropa','tiene_poderes','personalidad','serie','voz_tipo','tamano','inteligencia','protagonista']

def generate_icon(path, name, color=(180,180,255)):
    img = Image.new('RGBA', (160,160), color + (255,))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', 16)
    except Exception:
        font = ImageFont.load_default()
    # Center multi-line name
    words = name.split()
    lines, line = [], ''
    for w in words:
        if len((line+' '+w).strip()) <= 12:
            line = (line+' '+w).strip()
        else:
            lines.append(line)
            line = w
    if line: lines.append(line)
    y = 70 - (len(lines) * 10)
    for ln in lines[:3]:
        w,h = draw.textsize(ln, font=font)
        draw.text(((160-w)/2, y), ln, fill=(0,0,0), font=font)
        y += h + 4
    img.save(path)

class LearnDialog(tk.Toplevel):
    def __init__(self, master, hechos):
        super().__init__(master)
        self.title('Enseñar nuevo personaje')
        self.result = None
        tk.Label(self, text='¿En quién estabas pensando? Escribe el nombre exacto:', font=('Arial', 12)).pack(padx=10, pady=8)
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var, width=35).pack(padx=10, pady=4)
        tk.Label(self, text='Confirma o corrige los atributos:', font=('Arial', 11, 'bold')).pack(padx=10, pady=6)
        self.vars = {}
        frm = tk.Frame(self)
        frm.pack(padx=10, pady=6)
        # Build widgets per attribute
        row = 0
        for a in ATRIBUTOS:
            tk.Label(frm, text=a).grid(row=row, column=0, sticky='w', padx=4, pady=3)
            val = hechos.get(a, None)
            if isinstance(val, bool) or a in ['usa_ropa','tiene_poderes','protagonista']:
                v = tk.BooleanVar(value=True if val is True else False if val is False else False)
                cb = ttk.Checkbutton(frm, variable=v, text='Sí (marcado) / No (desmarcado)')
                cb.grid(row=row, column=1, sticky='w')
                self.vars[a] = v
            else:
                sv = tk.StringVar(value='' if val is None else str(val))
                ent = tk.Entry(frm, textvariable=sv, width=25)
                ent.grid(row=row, column=1, sticky='w')
                self.vars[a] = sv
            row += 1
        btns = tk.Frame(self)
        btns.pack(pady=8)
        tk.Button(btns, text='Guardar', command=self.on_save).pack(side='left', padx=6)
        tk.Button(btns, text='Cancelar', command=self.destroy).pack(side='left', padx=6)
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def on_save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning('Atención', 'Debes escribir un nombre.')
            return
        datos = {}
        for a, var in self.vars.items():
            if isinstance(var, tk.BooleanVar):
                datos[a] = bool(var.get())
            else:
                val = var.get().strip()
                datos[a] = val if val != '' else None
        self.result = {'nombre': name, **datos}
        self.destroy()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Adivina Quién - Cartoon Network (antropomorfos)')
        self.engine = ExpertEngine(BASE_FILE)
        self.repo = CaseRepositoryJSON(os.path.join(os.path.dirname(__file__), 'casos.json'))
        self.max_preguntas = 10
        self.preguntas_hechas = 0

        top = tk.Frame(root); top.pack(padx=10, pady=10)
        self.question_label = tk.Label(top, text='Piensa en un personaje... pulsa Comenzar', font=('Arial',14))
        self.question_label.pack()

        btn_frame = tk.Frame(root); btn_frame.pack(pady=5)
        self.start_btn = tk.Button(btn_frame, text='Comenzar', command=self.start)
        self.start_btn.pack(side='left', padx=5)
        self.reset_btn = tk.Button(btn_frame, text='Reiniciar', command=self.reset)
        self.reset_btn.pack(side='left', padx=5)

        resp_frame = tk.Frame(root); resp_frame.pack(pady=8)
        self.yes_btn = tk.Button(resp_frame, text='Sí', width=10, command=lambda: self.answer(True), state='disabled')
        self.no_btn = tk.Button(resp_frame, text='No', width=10, command=lambda: self.answer(False), state='disabled')
        self.dont_btn = tk.Button(resp_frame, text='No sé', width=10, command=lambda: self.answer(None), state='disabled')
        self.yes_btn.pack(side='left', padx=5); self.no_btn.pack(side='left', padx=5); self.dont_btn.pack(side='left', padx=5)

        self.canvas = tk.Canvas(root, width=600, height=240); self.canvas.pack(padx=10, pady=10)
        self.icon_images = {}
        self.load_icons()

    def load_icons(self):
        self.icon_paths = {}
        if os.path.isdir(ICONS_DIR):
            for fn in os.listdir(ICONS_DIR):
                if fn.lower().endswith('.png'):
                    path = os.path.join(ICONS_DIR, fn)
                    name = os.path.splitext(fn)[0]
                    self.icon_paths[name] = path

    def start(self):
        self.engine.reset(); self.preguntas_hechas = 0
        self.start_btn.config(state='disabled')
        for b in (self.yes_btn, self.no_btn, self.dont_btn): b.config(state='normal')
        self.next_question()

    def reset(self):
        self.engine.reset(); self.preguntas_hechas = 0
        self.question_label.config(text='Piensa en un personaje... pulsa Comenzar')
        self.start_btn.config(state='normal')
        for b in (self.yes_btn, self.no_btn, self.dont_btn): b.config(state='disabled')
        self.canvas.delete('all')

    def next_question(self):
        if self.preguntas_hechas >= self.max_preguntas:
            self.make_guess(final=True); return
        attr = self.engine.next_question(ATRIBUTOS)
        if attr is None:
            self.make_guess(final=True); return
        q = self.make_natural_question(attr)
        self.current_attr = attr
        self.question_label.config(text=f'Pregunta {self.preguntas_hechas+1}: {q}')
        self.update_candidate_icons()

    def make_natural_question(self, attr):
        mapping = {
            'especie': '¿Tu personaje es de qué especie? (perro, mapache, pájaro, gato, pez, etc.)',
            'color': '¿Cuál es el color principal de tu personaje? (azul, rosa, amarillo, etc.)',
            'usa_ropa': '¿Tu personaje usa ropa?',
            'tiene_poderes': '¿Tu personaje tiene poderes?',
            'personalidad': '¿Cómo describirías su personalidad? (travieso, amable, miedoso, relajado…)',
            'serie': '¿De qué serie es tu personaje? (Regular Show, Adventure Time, etc.)',
            'voz_tipo': '¿Su voz es grave, media o aguda?',
            'tamano': '¿El personaje es pequeño, mediano o grande?',
            'inteligencia': '¿Su inteligencia es alta, media o baja?',
            'protagonista': '¿Es protagonista de su serie?'
        }
        return mapping.get(attr, f'Pregunta sobre {attr}')

    def answer(self, val):
        # For textual attributes and yes/no pressed, ask text
        if self.current_attr in ['especie','color','personalidad','serie','voz_tipo','tamano','inteligencia'] and val is not None:
            v = simpledialog.askstring('Respuesta', 'Escribe la respuesta (texto):')
            if v is None: return
            respuesta = v.strip()
        else:
            respuesta = val
        self.engine.apply_answer(self.current_attr, respuesta)
        self.preguntas_hechas += 1
        if len(self.engine.candidatos) == 1:
            self.make_guess(final=False); return
        self.next_question()

    def update_candidate_icons(self):
        self.canvas.delete('all')
        x,y = 10,10; per_row = 6; idx = 0
        for pid in self.engine.candidatos:
            p = next(x for x in self.engine.personajes if x['id']==pid)
            name_key = p['nombre'].replace(' ','_')
            path = self.icon_paths.get(name_key)
            if path and os.path.exists(path):
                img = Image.open(path).resize((80,80))
                tkimg = ImageTk.PhotoImage(img); self.icon_images[f'{pid}'] = tkimg
                self.canvas.create_image(x+40,y+40,image=tkimg)
            self.canvas.create_text(x+40,y+95,text=p['nombre'])
            x += 100; idx += 1
            if idx % per_row == 0: x = 10; y += 120

    def make_guess(self, final=True):
        pid = self.engine.guess()
        if pid is None: pid = random.choice(self.engine.candidatos) if self.engine.candidatos else None
        if pid is None:
            messagebox.showinfo('Resultado', 'No pude adivinar ningún personaje.')
            self.learn_new_character()
            self.reset(); return
        p = next(x for x in self.engine.personajes if x['id']==pid)
        text = f'Creo que tu personaje es: {p["nombre"]}. ¿Es correcto?'
        ans = messagebox.askyesno('Adivinar', text)
        if ans:
            self.save_case(pid, True)
            messagebox.showinfo('¡Genial!', '¡Adiviné tu personaje! Caso guardado.')
            self.reset()
        else:
            # allow learning if wrong
            self.save_case(pid, False)
            self.learn_new_character()
            self.reset()

    def save_case(self, guessed_id, result):
        case = {
            'initial_ids': [x['id'] for x in self.engine.personajes],
            'questions': self.engine.asked,
            'hechos': self.engine.hechos,
            'guessed': guessed_id,
            'result': result,
            'num_questions': self.preguntas_hechas
        }
        self.repo.save_case(case)

    def learn_new_character(self):
        dlg = LearnDialog(self.root, self.engine.hechos)
        self.root.wait_window(dlg)
        if dlg.result is None: return
        nuevo = dlg.result
        # Ensure required fields exist; fill missing with 'desconocido'/False
        for a in ATRIBUTOS:
            if a not in nuevo:
                nuevo[a] = False if a in ['usa_ropa','tiene_poderes','protagonista'] else 'desconocido'
        # Add to base knowledge
        added = self.engine.add_new_character(nuevo)
        # Auto-generate icon with solid color background and the name
        name_key = added['nombre'].replace(' ','_')
        path = os.path.join(ICONS_DIR, f'{name_key}.png')
        # Pick color by hashing name
        h = abs(hash(added['nombre'])) % 255
        color = (100 + h%155, 100 + (h*2)%155, 100 + (h*3)%155)
        generate_icon(path, added['nombre'], color=color)
        messagebox.showinfo('Aprendido', f'He aprendido un nuevo personaje: {added["nombre"]}.')

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

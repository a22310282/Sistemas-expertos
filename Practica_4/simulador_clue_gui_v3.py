# -*- coding: utf-8 -*-
import json, random, os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

NOIR_BG = "#101820"
NOIR_PANEL = "#202830"
FG = "#EEEEEE"

RES_DIR = "recursos"
P_DIR = os.path.join(RES_DIR, "personajes")
A_DIR = os.path.join(RES_DIR, "armas")
L_DIR = os.path.join(RES_DIR, "lugares")

def slug(s):
    repl = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n","Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N"}
    for k,v in repl.items():
        s = s.replace(k,v)
    return s.lower().replace(" ", "_")

# --- Cargar base ---
with open("Practica_4/base_conocimiento_clue.json", "r", encoding="utf-8") as f:
    base = json.load(f)

personajes = base["personajes"]
lugares = base["lugares"]
armas = base["armas"]
historias = base["historias"]

# --- Caso secreto ---
culpable = random.choice(personajes)
arma = random.choice(armas)
lugar = random.choice(lugares)

class ClueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador CLUE – Misterio y Mentiras (v3)")
        self.geometry("980x720")
        self.configure(bg=NOIR_BG)
        self.resizable(True, True)
        self.minsize(1000, 760)

        self.intentos_restantes = 5
        self.seleccion = {"sospechoso": None, "arma": None, "lugar": None}

        container = tk.Frame(self, bg=NOIR_BG)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (PantallaInicio, PantallaInfo, PantallaSospechoso, PantallaArma, PantallaLugar, PantallaResultado):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar(PantallaInicio)

    def mostrar(self, pantalla):
        self.frames[pantalla].tkraise()

    def hearts_text(self):
        return "♥ " * self.intentos_restantes

class Header(tk.Frame):
    def __init__(self, parent, controller, title):
        super().__init__(parent, bg=NOIR_BG)
        self.controller = controller
        lbl = tk.Label(self, text=title, font=("Verdana", 20, "bold"), fg=FG, bg=NOIR_BG)
        lbl.pack(side="left", padx=18, pady=10)
        self.vidas = tk.Label(self, text=self.controller.hearts_text(), font=("Arial", 18, "bold"),
                              fg="#E14D4D", bg=NOIR_BG)
        self.vidas.pack(side="right", padx=18)
    def refresh(self):
        self.vidas.config(text=self.controller.hearts_text())

class PantallaInicio(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=NOIR_BG)
        self.header = Header(self, controller, "🕵️ CLUE: Misterio y Mentiras 🕵️")
        self.header.pack(fill="x")
        panel = tk.Frame(self, bg=NOIR_BG)
        panel.pack(expand=True)

        
        ttk.Button(panel, text="Iniciar partida",
                   command=lambda: controller.mostrar(PantallaInfo)).pack(pady=20, ipadx=12, ipady=6)

class PantallaInfo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=NOIR_BG)
        self.header = Header(self, controller, "⚡ Información del Caso ⚡")
        self.header.pack(fill="x")
        self.controller = controller

        body = tk.Frame(self, bg=NOIR_BG)
        body.pack(fill="both", expand=True, padx=16, pady=8)

        for title, items, subdir in [
            ("Sospechosos", personajes, P_DIR),
            ("Armas", armas, A_DIR),
            ("Lugares", lugares, L_DIR)
        ]:
            card = tk.LabelFrame(body, text=title, fg=FG, bg=NOIR_BG, font=("Arial", 12, "bold"))
            card.pack(side="left", expand=True, fill="both", padx=8, pady=8)
            canvas = tk.Canvas(card, bg=NOIR_PANEL, highlightthickness=0)
            canvas.pack(expand=True, fill="both", padx=6, pady=6)
            row, col = 0, 0
            icons = []
            labels = items if isinstance(items[0], str) else [p["nombre"] for p in items]
            for itm in labels:
                fpath = os.path.join(subdir, f"{slug(itm)}.png")
                if os.path.exists(fpath):
                    img = Image.open(fpath).resize((120,120))
                    ph = ImageTk.PhotoImage(img)
                    icons.append(ph)
                    canvas.create_image(20+col*140, 20+row*150, anchor="nw", image=ph)
                    canvas.create_text(20+col*140+60, 20+row*150+130, text=itm, fill=FG, font=("Arial", 10))
                else:
                    canvas.create_text(20+col*140+60, 20+row*150+60, text=itm, fill=FG, font=("Arial", 12))
                col += 1
                if col == 3:
                    col, row = 0, row+1
            card.icons = icons

        ttk.Button(self, text="Comenzar investigación",
                   command=lambda: controller.mostrar(PantallaSospechoso)).pack(pady=12)

    def tkraise(self, *a, **k):
        super().tkraise(*a, **k)
        self.header.refresh()

class GridSelect(tk.Frame):
    def __init__(self, parent, controller, title, options, res_subdir, key):
        super().__init__(parent, bg=NOIR_BG)
        self.controller = controller
        self.header = Header(self, controller, title)
        self.header.pack(fill="x")

        self.key = key
        body = tk.Frame(self, bg=NOIR_BG)
        body.pack(expand=True)

        grid = tk.Frame(body, bg=NOIR_BG)
        grid.pack(pady=12)

        self.icons = []
        labels = options if isinstance(options[0], str) else [p["nombre"] for p in options]
        for i, label in enumerate(labels):
            fpath = os.path.join(res_subdir, f"{slug(label)}.png")
            imgobj = None
            if os.path.exists(fpath):
                img = Image.open(fpath).resize((150,150))
                imgobj = ImageTk.PhotoImage(img)
                self.icons.append(imgobj)
            btn = ttk.Button(grid, text=label, width=22, command=lambda n=label: self.choose(n))
            if imgobj:
                btn.config(image=imgobj, compound="top")
            btn.grid(row=i//3, column=i%3, padx=10, pady=10, ipadx=6, ipady=6)

        self.btn_next = ttk.Button(self, text="Continuar", command=self.next_step, state="disabled")
        self.btn_next.pack(pady=12)

        self.selection_label = tk.Label(self, text="Selección: -", fg="#00FFAA", bg=NOIR_BG, font=("Arial", 12, "bold"))
        self.selection_label.pack()

    def choose(self, name):
        self.controller.seleccion[self.key] = name
        self.selection_label.config(text=f"Selección: {name}")
        self.btn_next.config(state="normal")

    def next_step(self):
        pass

    def tkraise(self, *a, **k):
        super().tkraise(*a, **k)
        self.header.refresh()

class PantallaSospechoso(GridSelect):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Selecciona un sospechoso", personajes, P_DIR, "sospechoso")
    def next_step(self):
        self.controller.mostrar(PantallaArma)

class PantallaArma(GridSelect):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Selecciona el arma", armas, A_DIR, "arma")
    def next_step(self):
        self.controller.mostrar(PantallaLugar)

class PantallaLugar(GridSelect):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Selecciona el lugar", lugares, L_DIR, "lugar")
    def next_step(self):
        self.controller.mostrar(PantallaResultado)

class PantallaResultado(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=NOIR_BG)
        self.controller = controller
        self.header = Header(self, controller, "Resultado de la conjetura")
        self.header.pack(fill="x")
        self.lbl = tk.Label(self, text="", fg=FG, bg=NOIR_BG, font=("Arial", 16, "bold"))
        self.lbl.pack(pady=12)

        self.txt = tk.Text(self, width=100, height=16, bg=NOIR_PANEL, fg=FG, font=("Consolas", 11), wrap="word")
        self.txt.pack(padx=16, pady=8)
        self.txt.config(state="disabled")

        self.btn_retry = ttk.Button(self, text="Intentar de nuevo", command=self.retry)
        self.btn_retry.pack(pady=6)
        self.btn_salir = ttk.Button(self, text="Salir", command=self.controller.destroy)
        self.btn_salir.pack()

    def tkraise(self, *a, **k):
        super().tkraise(*a, **k)
        self.show_result()
        self.header.refresh()

    def show_result(self):
        s = self.controller.seleccion
        correcto = (s["sospechoso"] == culpable["nombre"] and s["arma"] == arma and s["lugar"] == lugar)

        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)

        if correcto:
            self.lbl.config(text="🎉 ¡Has resuelto el misterio!", fg="#00FFAA")
            self.txt.insert(tk.END, f"Culpable: {culpable['nombre']} ({culpable['profesion']})\nArma: {arma}\nLugar: {lugar}\n\n")
            for h in historias:
                if culpable["nombre"] in h:
                    self.txt.insert(tk.END, "📜 Historia final:\n"+h+"\n")
                    break
            self.btn_retry.config(state="disabled")
        else:
            self.controller.intentos_restantes -= 1
            self.lbl.config(text=f"❌ Incorrecto. Intentos restantes: {self.controller.intentos_restantes}", fg="#FF6666")
            pistas = []
            if s["sospechoso"] != culpable["nombre"]:
                pistas.append("El sospechoso no coincide.")
            if s["arma"] != arma:
                pistas.append("El arma no coincide.")
            if s["lugar"] != lugar:
                pistas.append("El lugar no coincide.")
            self.txt.insert(tk.END, "\n".join(pistas)+"\n")

            if self.controller.intentos_restantes <= 0:
                self.txt.insert(tk.END, "\n💀 Sin intentos. La verdad fue:\n")
                self.txt.insert(tk.END, f"Culpable: {culpable['nombre']} ({culpable['profesion']})\nArma: {arma}\nLugar: {lugar}\n")
                for h in historias:
                    if culpable["nombre"] in h:
                        self.txt.insert(tk.END, "\n📜 Historia final:\n"+h+"\n")
                        break
                self.btn_retry.config(state="disabled")

        self.txt.config(state="disabled")

    def retry(self):
        if self.controller.intentos_restantes > 0:
            self.controller.seleccion = {"sospechoso": None, "arma": None, "lugar": None}
            self.controller.mostrar(PantallaSospechoso)
        else:
            messagebox.showinfo("Fin del juego", "No quedan intentos.")
            self.controller.destroy()

if __name__ == "__main__":
    app = ClueApp()
    app.mainloop()

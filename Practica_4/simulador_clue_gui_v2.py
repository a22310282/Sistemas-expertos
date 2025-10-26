# -*- coding: utf-8 -*-
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox

# --- Cargar base de conocimiento ---
with open("Practica_4/base_conocimiento_clue.json", "r", encoding="utf-8") as f:
    base = json.load(f)

personajes = base["personajes"]
lugares = base["lugares"]
armas = base["armas"]
historias = base["historias"]

# --- Datos aleatorios del caso ---
culpable = random.choice(personajes)
arma = random.choice(armas)
lugar = random.choice(lugares)


class ClueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador CLUE – Misterio y Mentiras (v2)")
        self.geometry("900x650")
        self.config(bg="#101820")

        self.intentos_restantes = 5
        self.seleccion = {"sospechoso": None, "arma": None, "lugar": None}

        container = tk.Frame(self, bg="#101820")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (PantallaInicio, PantallaInfo, PantallaSospechoso, PantallaArma, PantallaLugar, PantallaResultado):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar(PantallaInicio)

    def mostrar(self, pantalla):
        self.frames[pantalla].tkraise()


class PantallaInicio(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#101820")
        tk.Label(self, text="🕵️ CLUE: Misterio y Mentiras 🕵️",
                 font=("Verdana", 28, "bold"), fg="white", bg="#101820").pack(pady=80)
        tk.Label(self, text="Descubre al culpable, el arma y el lugar del crimen.",
                 font=("Arial", 14), fg="#CCCCCC", bg="#101820").pack(pady=10)
        ttk.Button(self, text="Iniciar partida",
                   command=lambda: controller.mostrar(PantallaInfo)).pack(pady=40)


class PantallaInfo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#101820")

        tk.Label(self, text="⚡ Información del Caso ⚡",
                 font=("Verdana", 22, "bold"), fg="white", bg="#101820").pack(pady=20)

        txt = tk.Text(self, width=90, height=18, bg="#202830", fg="white",
                      font=("Consolas", 12), wrap="word")
        txt.pack(padx=20, pady=10)
        txt.insert(tk.END, "POSIBLES SOSPECHOSOS:\n")
        for p in personajes:
            txt.insert(tk.END, f" - {p['nombre']} ({p['profesion']})\n")
        txt.insert(tk.END, "\nPOSIBLES ARMAS:\n")
        for a in armas:
            txt.insert(tk.END, f" - {a}\n")
        txt.insert(tk.END, "\nPOSIBLES LUGARES:\n")
        for l in lugares:
            txt.insert(tk.END, f" - {l}\n")
        txt.config(state="disabled")

        ttk.Button(self, text="Comenzar investigación",
                   command=lambda: controller.mostrar(PantallaSospechoso)).pack(pady=20)


class PantallaSospechoso(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#101820")
        tk.Label(self, text="Selecciona un sospechoso:",
                 font=("Arial", 18, "bold"), fg="white", bg="#101820").pack(pady=20)

        for p in personajes:
            ttk.Button(self, text=p["nombre"],
                       command=lambda n=p["nombre"]: self.elegir(controller, n)).pack(pady=5, ipadx=15)

    def elegir(self, controller, nombre):
        controller.seleccion["sospechoso"] = nombre
        controller.mostrar(PantallaArma)


class PantallaArma(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#101820")
        tk.Label(self, text="Selecciona el arma:",
                 font=("Arial", 18, "bold"), fg="white", bg="#101820").pack(pady=20)

        for a in armas:
            ttk.Button(self, text=a,
                       command=lambda n=a: self.elegir(controller, n)).pack(pady=5, ipadx=15)

    def elegir(self, controller, arma_sel):
        controller.seleccion["arma"] = arma_sel
        controller.mostrar(PantallaLugar)


class PantallaLugar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#101820")
        tk.Label(self, text="Selecciona el lugar:",
                 font=("Arial", 18, "bold"), fg="white", bg="#101820").pack(pady=20)

        for l in lugares:
            ttk.Button(self, text=l,
                       command=lambda n=l: self.elegir(controller, n)).pack(pady=5, ipadx=15)

    def elegir(self, controller, lugar_sel):
        controller.seleccion["lugar"] = lugar_sel
        controller.mostrar(PantallaResultado)


class PantallaResultado(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#101820")
        self.controller = controller
        self.lbl_result = tk.Label(self, text="", font=("Arial", 16), fg="white", bg="#101820")
        self.lbl_result.pack(pady=30)

        self.txt_detalle = tk.Text(self, width=90, height=15, bg="#202830", fg="white",
                                   font=("Consolas", 12), wrap="word")
        self.txt_detalle.pack(padx=20, pady=10)
        self.txt_detalle.config(state="disabled")

        self.btn_retry = ttk.Button(self, text="Intentar de nuevo", command=self.reintentar)
        self.btn_retry.pack(pady=10)
        self.btn_salir = ttk.Button(self, text="Salir", command=self.controller.destroy)
        self.btn_salir.pack()

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.mostrar_resultado()

    def mostrar_resultado(self):
        self.txt_detalle.config(state="normal")
        self.txt_detalle.delete("1.0", tk.END)

        s = self.controller.seleccion
        c = (s["sospechoso"] == culpable["nombre"]
             and s["arma"] == arma
             and s["lugar"] == lugar)

        if c:
            self.lbl_result.config(text="🎉 ¡Has resuelto el misterio!", fg="#00FFAA")
            self.txt_detalle.insert(tk.END, f"Culpable: {culpable['nombre']} ({culpable['profesion']})\n")
            self.txt_detalle.insert(tk.END, f"Arma: {arma}\nLugar: {lugar}\n\n")
            for h in historias:
                if culpable["nombre"] in h:
                    self.txt_detalle.insert(tk.END, "📜 Historia final:\n" + h + "\n")
                    break
            self.btn_retry.config(state="disabled")
        else:
            self.controller.intentos_restantes -= 1
            self.lbl_result.config(
                text=f"❌ Incorrecto. Intentos restantes: {self.controller.intentos_restantes}",
                fg="#FF5555"
            )
            pistas = []
            if s["sospechoso"] != culpable["nombre"]:
                pistas.append("El sospechoso no coincide.")
            if s["arma"] != arma:
                pistas.append("El arma no coincide.")
            if s["lugar"] != lugar:
                pistas.append("El lugar no coincide.")
            if pistas:
                self.txt_detalle.insert(tk.END, "\n".join(pistas) + "\n")

            if self.controller.intentos_restantes <= 0:
                self.txt_detalle.insert(tk.END, "\n💀 Se acabaron los intentos. La verdad fue:\n")
                self.txt_detalle.insert(tk.END, f"Culpable: {culpable['nombre']} ({culpable['profesion']})\n")
                self.txt_detalle.insert(tk.END, f"Arma: {arma}\nLugar: {lugar}\n")
                for h in historias:
                    if culpable["nombre"] in h:
                        self.txt_detalle.insert(tk.END, "\n📜 Historia final:\n" + h + "\n")
                        break
                self.btn_retry.config(state="disabled")

        self.txt_detalle.config(state="disabled")

    def reintentar(self):
        # Limpiar sólo las selecciones (no el secreto) y volver a la primera pantalla de selección
        self.controller.seleccion = {"sospechoso": None, "arma": None, "lugar": None}
        if self.controller.intentos_restantes > 0:
            self.controller.mostrar(PantallaSospechoso)
        else:
            messagebox.showinfo("Fin del juego", "No quedan intentos.")
            self.controller.destroy()


if __name__ == "__main__":
    app = ClueApp()
    app.mainloop()

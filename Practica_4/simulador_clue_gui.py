# -*- coding: utf-8 -*-
import json
import random
import tkinter as tk
from tkinter import messagebox, ttk

# --- Cargar base de conocimiento ---
with open("Practica_4/base_conocimiento_clue.json", "r", encoding="utf-8") as f:
    base = json.load(f)

personajes = base["personajes"]
lugares = base["lugares"]
armas = base["armas"]
historias = base["historias"]

# --- Selección aleatoria ---
culpable = random.choice(personajes)
arma = random.choice(armas)
lugar = random.choice(lugares)

intentos_restantes = 5
seleccion = {"sospechoso": None, "arma": None, "lugar": None}

# --- Funciones de lógica del juego ---
def seleccionar(tipo, valor):
    seleccion[tipo] = valor
    actualizar_estado()

def actualizar_estado():
    lbl_seleccion.config(
        text=f"Sospechoso: {seleccion['sospechoso'] or '-'} | "
             f"Arma: {seleccion['arma'] or '-'} | "
             f"Lugar: {seleccion['lugar'] or '-'}"
    )

def comprobar():
    global intentos_restantes

    if None in seleccion.values():
        messagebox.showwarning("Incompleto", "Selecciona sospechoso, arma y lugar antes de continuar.")
        return

    sospechoso = seleccion["sospechoso"]
    arma_sel = seleccion["arma"]
    lugar_sel = seleccion["lugar"]

    if (sospechoso == culpable["nombre"] and arma_sel == arma and lugar_sel == lugar):
        mostrar_historia()
        return
    else:
        intentos_restantes -= 1
        pistas = []
        if sospechoso != culpable["nombre"]:
            pistas.append("❌ El sospechoso no coincide.")
        if arma_sel != arma:
            pistas.append("🔫 El arma no coincide.")
        if lugar_sel != lugar:
            pistas.append("🏠 El lugar no coincide.")

        salida_text.insert(tk.END, f"\nIntento fallido. Pistas:\n" + "\n".join(pistas) + "\n")
        salida_text.see(tk.END)

        if intentos_restantes <= 0:
            salida_text.insert(tk.END, "\n💀 Se acabaron los intentos. El caso ha sido resuelto automáticamente.\n")
            mostrar_historia()

def mostrar_historia():
    salida_text.insert(tk.END, "\n🔍 La verdad del caso:\n")
    salida_text.insert(tk.END, f"Culpable: {culpable['nombre']} ({culpable['profesion']})\n")
    salida_text.insert(tk.END, f"Arma: {arma}\nLugar: {lugar}\n\n")
    for h in historias:
        if culpable["nombre"] in h:
            salida_text.insert(tk.END, "📜 Historia final:\n" + h + "\n")
            break
    salida_text.see(tk.END)
    btn_comprobar.config(state="disabled")

# --- Construcción de la interfaz ---
root = tk.Tk()
root.title("Simulador CLUE – Misterio y Mentiras")
root.geometry("900x650")
root.config(bg="#101820")

style = ttk.Style()
style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
style.map("TButton",
          background=[("active", "#89CFF0"), ("!active", "#DAEAF1")])

titulo = tk.Label(root, text="🕵️ CLUE: Misterio y Mentiras 🕵️",
                  font=("Verdana", 20, "bold"), bg="#101820", fg="white")
titulo.pack(pady=10)

lbl_instr = tk.Label(root, text="Selecciona un sospechoso, un arma y un lugar.",
                     font=("Arial", 12), bg="#101820", fg="#CCCCCC")
lbl_instr.pack()

lbl_seleccion = tk.Label(root, text="", font=("Arial", 12, "bold"),
                         bg="#101820", fg="#00FFAA")
lbl_seleccion.pack(pady=5)

frame_botones = tk.Frame(root, bg="#101820")
frame_botones.pack(pady=10)

# --- Sección Sospechosos ---
frame_sospechosos = tk.LabelFrame(frame_botones, text="Sospechosos", fg="white", bg="#101820",
                                  font=("Arial", 12, "bold"), labelanchor="n", padx=10, pady=10)
frame_sospechosos.grid(row=0, column=0, padx=15)
for p in personajes:
    ttk.Button(frame_sospechosos, text=p["nombre"],
               command=lambda n=p["nombre"]: seleccionar("sospechoso", n)).pack(pady=3, fill="x")

# --- Sección Armas ---
frame_armas = tk.LabelFrame(frame_botones, text="Armas", fg="white", bg="#101820",
                            font=("Arial", 12, "bold"), labelanchor="n", padx=10, pady=10)
frame_armas.grid(row=0, column=1, padx=15)
for a in armas:
    ttk.Button(frame_armas, text=a,
               command=lambda n=a: seleccionar("arma", n)).pack(pady=3, fill="x")

# --- Sección Lugares ---
frame_lugares = tk.LabelFrame(frame_botones, text="Lugares", fg="white", bg="#101820",
                              font=("Arial", 12, "bold"), labelanchor="n", padx=10, pady=10)
frame_lugares.grid(row=0, column=2, padx=15)
for l in lugares:
    ttk.Button(frame_lugares, text=l,
               command=lambda n=l: seleccionar("lugar", n)).pack(pady=3, fill="x")

# --- Botón comprobar ---
btn_comprobar = ttk.Button(root, text="Comprobar sospecha", command=comprobar)
btn_comprobar.pack(pady=10)

# --- Cuadro de salida ---
salida_text = tk.Text(root, wrap="word", width=100, height=15, bg="#202830",
                      fg="white", font=("Consolas", 11))
salida_text.pack(padx=15, pady=10)
salida_text.insert(tk.END, "🕵️ ¡Un crimen ha ocurrido! Tienes 5 intentos para resolver el misterio...\n")

def cerrar():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", cerrar)
actualizar_estado()
root.mainloop()

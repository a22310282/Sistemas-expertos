# -*- coding: utf-8 -*-
import json
import random
import time

with open("Practica_4/base_conocimiento.json", "r", encoding="utf-8") as f:
    base = json.load(f)

personajes = base["personajes"]
lugares = base["lugares"]
armas = base["armas"]
historias = base["historias"]

culpable = random.choice(personajes)
arma = random.choice(armas)
lugar = random.choice(lugares)

print("🕵️‍♂️ Bienvenido al juego CLUE: Misterio y Mentiras")
time.sleep(0.8)
print("Un crimen ha ocurrido... tu deber es descubrir al culpable.")
time.sleep(1.2)

MAX_INTENTOS = 5
for intento in range(MAX_INTENTOS):
    print(f"\nIntento {intento+1}/{MAX_INTENTOS}")
    sospechoso = input("¿Quién es el culpable?: ").strip()
    arma_sel = input("¿Con qué arma?: ").strip()
    lugar_sel = input("¿Dónde?: ").strip()

    if (sospechoso.lower() == culpable["nombre"].lower() and
        arma_sel.lower() == arma.lower() and
        lugar_sel.lower() == lugar.lower()):
        print("\n🎉 ¡Felicidades! Has resuelto el misterio.")
        break
    else:
        pistas = []
        if sospechoso.lower() != culpable["nombre"].lower():
            pistas.append("El sospechoso no coincide.")
        if arma_sel.lower() != arma.lower():
            pistas.append("El arma no coincide.")
        if lugar_sel.lower() != lugar.lower():
            pistas.append("El lugar no coincide.")
        print("❌ No exactamente... ", " | ".join(pistas))

print("\n🔍 La verdad del caso:")
print(f"Culpable: {culpable['nombre']} ({culpable['profesion']})")
print(f"Arma: {arma}")
print(f"Lugar: {lugar}")

for h in historias:
    if culpable["nombre"] in h:
        print("\n📜 Historia final:")
        print(h)
        break

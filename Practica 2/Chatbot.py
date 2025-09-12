import json
import os

#archivo para guardar el conocimiento
BASE_FILE = "base_conocimiento.json"

#Cargar conocimiento previo si existe
if os.path.exists(BASE_FILE):
    with open(BASE_FILE, "r", encoding="utf-8") as f:
        base_conocimiento = json.load(f)
else:
    #base precargada mínima
    base_conocimiento = {
        "hola" : "¡Hola! ¿Cómo estás?",
        "como estas": "Muy bien, gracias. ¿Yú?",
        "de que te gustaria hablar": "Podemos hablar de teconología, ciencia o lo que quieras."
    }
print("🤖 Chatbot iniciado. Escribe salir para terminar.\n")

while True:
    user_input = input("Tú: ").strip().lower()

    if user_input == "salir":
        print(" Chatbot: ¡Hasta luego!")
        break

    #Buscar una respuesta
    if user_input in base_conocimiento:
        print("🤖 Chatbot", base_conocimiento[user_input])
    else:
        print("🤖 Chatbot: No sé cómo responder a eso.")
        new_response = input("¿Qué debería responder cuando me digas eso?")

        #Guardar el nuevo conocimiento
        base_conocimiento[user_input] = new_response

        with open(BASE_FILE, "w", encoding="utf-8") as f:
            json.dump(base_conocimiento, f, indent=4, ensure_ascii=False)

        print("🤖 Chatbot: ¡Gracias! Ahora ya lo aprendí.")
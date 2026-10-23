
import tkinter as tk
from tkinter import ttk
import threading
import queue
import re
import time

cola = queue.Queue()

def registrar(mensaje):
    print(mensaje, flush=True)
    cola.put(("consola", mensaje))

def analizar_longitud(contrasena):
    registrar("[HILO 1] Analizando longitud...")
    time.sleep(0.5)

    resultados = {
        "8 caracteres o más": len(contrasena) >= 8,
        "12 caracteres o más": len(contrasena) >= 12
    }

    registrar("[HILO 1] Analisis de longitud terminado.")
    cola.put(("resultado", resultados))

def analizar_letras(contrasena):
    registrar("[HILO 2] Analizando letras...")
    time.sleep(0.5)

    resultados = {
        "Contiene mayusculas": bool(re.search(r"[A-Z]", contrasena)),
        "Contiene minusculas": bool(re.search(r"[a-z]", contrasena))
    }

    registrar("[HILO 2] Analisis de letras terminado.")
    cola.put(("resultado", resultados))

def analizar_numeros_simbolos(contrasena):
    registrar("[HILO 3] Analizando numeros y simbolos...")
    time.sleep(0.5)

    resultados = {
        "Contiene numeros": bool(re.search(r"[0-9]", contrasena)),
        "Contiene simbolos": bool(re.search(r"[^a-zA-Z0-9]", contrasena))
    }

    registrar("[HILO 3] Analisis terminado.")
    cola.put(("resultado", resultados))

def mostrar_consola(mensaje):
    consola.config(state="normal")
    consola.insert(tk.END, mensaje + "\n")
    consola.see(tk.END)
    consola.config(state="disabled")

def procesar_cola():
    global resultados_actuales, hilos_pendientes

    while not cola.empty():
        tipo, datos = cola.get()

        if tipo == "consola":
            mostrar_consola(datos)

        elif tipo == "resultado":
            resultados_actuales.update(datos)
            hilos_pendientes -= 1

    if hilos_pendientes == 0 and analisis_activo[0]:
        finalizar_analisis()

    ventana.after(100, procesar_cola)

def alternar_contrasena():
    if entrada.cget("show") == "*":
        entrada.config(show="")
        boton_ojo.config(text="Ocultar")
    else:
        entrada.config(show="*")
        boton_ojo.config(text="Mostrar")

def iniciar_analisis():
    global resultados_actuales, hilos_pendientes

    if analisis_activo[0]:
        return

    contrasena = entrada.get()

    if not contrasena:
        estado.config(
            text="Escribe una contraseña para analizarla.",
            foreground="orange"
        )
        entrada.focus_set()
        return

    resultados_actuales = {}
    hilos_pendientes = 3
    analisis_activo[0] = True

    boton_analizar.config(state="disabled")
    boton_borrar.config(state="disabled")
    estado.config(text="Analizando...", foreground="blue")
    fortaleza.config(text="Esperando resultados...", foreground="black")

    lista_resultados.delete(0, tk.END)

    consola.config(state="normal")
    consola.delete("1.0", tk.END)
    consola.config(state="disabled")

    registrar("[SISTEMA] Iniciando analisis.")
    registrar("[SISTEMA] Creando tres hilos de trabajo.")

    threading.Thread(
        target=analizar_longitud,
        args=(contrasena,),
        daemon=True
    ).start()

    threading.Thread(
        target=analizar_letras,
        args=(contrasena,),
        daemon=True
    ).start()

    threading.Thread(
        target=analizar_numeros_simbolos,
        args=(contrasena,),
        daemon=True
    ).start()

def finalizar_analisis():
    analisis_activo[0] = False

    puntaje = sum(resultados_actuales.values())

    for criterio, cumple in resultados_actuales.items():
        simbolo = "SI" if cumple else "NO"
        lista_resultados.insert(tk.END, f"{simbolo} - {criterio}")

    longitud_correcta = resultados_actuales.get(
        "8 caracteres o más", False
    )
    longitud_larga = resultados_actuales.get(
        "12 caracteres o más", False
    )

    if puntaje >= 5 and longitud_larga:
        nivel = "FUERTE"
        color = "green"
    elif puntaje >= 3 and longitud_correcta:
        nivel = "MEDIA"
        color = "#B8860B"
    else:
        nivel = "DEBIL"
        color = "red"

    fortaleza.config(
        text=f"Fortaleza: {nivel} ({puntaje}/6)",
        foreground=color
    )

    recomendaciones = [
        criterio
        for criterio, cumple in resultados_actuales.items()
        if not cumple
    ]

    if recomendaciones:
        estado.config(
            text="Mejora: " + ", ".join(recomendaciones),
            foreground="#B8860B"
        )
    else:
        estado.config(
            text="La contraseña cumple todos los criterios.",
            foreground="green"
        )

    registrar(f"[SISTEMA] Analisis finalizado. Nivel: {nivel}.")
    registrar("[SISTEMA] Los tres hilos han terminado.")

    boton_analizar.config(state="normal")
    boton_borrar.config(state="normal")

def borrar_contrasena():
    if analisis_activo[0]:
        return

    entrada.delete(0, tk.END)
    entrada.config(show="*")
    boton_ojo.config(text="Mostrar")

    lista_resultados.delete(0, tk.END)

    consola.config(state="normal")
    consola.delete("1.0", tk.END)
    consola.config(state="disabled")

    fortaleza.config(
        text="Fortaleza: sin analizar",
        foreground="black"
    )

    estado.config(
        text="Listo para analizar una nueva contraseña.",
        foreground="#444444"
    )

    entrada.focus_set()
    print("[SISTEMA] Campo y resultados borrados.", flush=True)

ventana = tk.Tk()
ventana.title("Analizador de contraseñas")
ventana.geometry("650x700")
ventana.minsize(550, 650)
ventana.configure(bg="#EAF0F6")

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure(
    "TButton",
    font=("Arial", 10, "bold"),
    padding=8
)

resultados_actuales = {}
hilos_pendientes = 0
analisis_activo = [False]

titulo = tk.Label(
    ventana,
    text="ANALIZADOR DE CONTRASEÑAS",
    font=("Arial", 18, "bold"),
    bg="#EAF0F6",
    fg="#203864"
)
titulo.pack(pady=(18, 8))

descripcion = tk.Label(
    ventana,
    text="Evaluacion concurrente mediante tres hilos de Python",
    font=("Arial", 10),
    bg="#EAF0F6",
    fg="#444444"
)
descripcion.pack(pady=4)

marco_entrada = tk.Frame(ventana, bg="#EAF0F6")
marco_entrada.pack(fill="x", padx=35, pady=12)

tk.Label(
    marco_entrada,
    text="Introduce tu contraseña:",
    font=("Arial", 11, "bold"),
    bg="#EAF0F6"
).pack(anchor="w")

fila_entrada = tk.Frame(marco_entrada, bg="#EAF0F6")
fila_entrada.pack(fill="x", pady=8)

entrada = ttk.Entry(
    fila_entrada,
    show="*",
    font=("Arial", 12)
)
entrada.pack(side="left", fill="x", expand=True)

boton_ojo = ttk.Button(
    fila_entrada,
    text="Mostrar",
    command=alternar_contrasena
)
boton_ojo.pack(side="left", padx=(8, 0))

fila_botones = tk.Frame(marco_entrada, bg="#EAF0F6")
fila_botones.pack(fill="x", pady=4)

boton_analizar = ttk.Button(
    fila_botones,
    text="Analizar contraseña",
    command=iniciar_analisis
)
boton_analizar.pack(side="left", fill="x", expand=True, padx=(0, 4))

boton_borrar = ttk.Button(
    fila_botones,
    text="Borrar contraseña",
    command=borrar_contrasena
)
boton_borrar.pack(side="left", fill="x", expand=True, padx=(4, 0))

entrada.bind("<Return>", lambda evento: iniciar_analisis())

fortaleza = tk.Label(
    ventana,
    text="Fortaleza: sin analizar",
    font=("Arial", 14, "bold"),
    bg="#EAF0F6"
)
fortaleza.pack(pady=8)

estado = tk.Label(
    ventana,
    text="Listo para comenzar.",
    font=("Arial", 9),
    bg="#EAF0F6",
    wraplength=570,
    justify="center"
)
estado.pack(pady=4)

tk.Label(
    ventana,
    text="Resultados del analisis",
    font=("Arial", 11, "bold"),
    bg="#EAF0F6"
).pack(anchor="w", padx=35, pady=(8, 3))

lista_resultados = tk.Listbox(
    ventana,
    height=6,
    font=("Consolas", 10),
    relief="solid",
    bd=1
)
lista_resultados.pack(fill="x", padx=35, pady=4)

tk.Label(
    ventana,
    text="Consola de actividad",
    font=("Arial", 11, "bold"),
    bg="#EAF0F6"
).pack(anchor="w", padx=35, pady=(8, 3))

consola = tk.Text(
    ventana,
    height=7,
    bg="#17202A",
    fg="#7CFC98",
    insertbackground="white",
    font=("Consolas", 9),
    state="disabled"
)
consola.pack(fill="both", expand=True, padx=35, pady=(0, 15))

ventana.after(100, procesar_cola)
ventana.mainloop()

import pyautogui
import webbrowser
import time
import pandas as pd
import random

# Leer CSV
df = pd.read_csv("D:\! 4Geeks\proyecto_personal_1\ML_Job_Search\scraping\ofertas_infojobs.csv")
urls = df['url'].tolist()

# Parámetros configurables
inicio_en = 0
espera_carga = (5, 8)         # rango en segundos para que cargue la oferta
espera_guardado = (3, 5)      # espera después de guardar
descanso_cada = 50            # cuántas ofertas antes de descansar
tiempo_descanso = (120, 200)  # rango de descanso entre bloques (segundos)

# Scroll simulado
def scroll():
    pyautogui.moveTo(600, 400)
    for _ in range(3):
        pyautogui.scroll(-500)
        time.sleep(random.uniform(0.5, 1.5))

# Bucle principal
for i, url in enumerate(urls[inicio_en:], start=inicio_en):
    print(f"\n[{i+1}] Abriendo: {url}")
    webbrowser.open(url)
    time.sleep(random.uniform(*espera_carga))

    scroll()  # simula que "lees" la oferta

    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.typewrite(f"oferta_{i+1:04}.html")
    pyautogui.press('enter')
    time.sleep(random.uniform(*espera_guardado))

    pyautogui.hotkey('ctrl', 'w')  # cerrar pestaña
    time.sleep(1)

    # Descanso cada X ofertas
    if (i + 1) % descanso_cada == 0:
        pausa = random.randint(*tiempo_descanso)
        print(f"\n⏸️  Descansando {pausa} segundos...\n")
        time.sleep(pausa)

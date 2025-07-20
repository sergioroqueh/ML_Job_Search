import csv
import webbrowser
import time

# Ruta del archivo CSV
csv_path = 'scraping\\ofertas_infojobs.csv'  

# Leer las URLs desde el CSV
urls = []
with open(csv_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        url = row.get('url', '').strip()
        if url:
            # Asegurar que la URL comience con "https://"
            if not url.startswith("http"):
                url = "https://" + url.lstrip("/")
            urls.append(url)

# Abrir una a una esperando que presiones Enter
for i, url in enumerate(urls, 1):
    print(f"\n[{i}/{len(urls)}] Abriendo: {url}")
    webbrowser.open(url)
    input("🔔 Presiona Enter para continuar al siguiente...")
    time.sleep(1)  # Espera opcional, por si el navegador necesita un segundo

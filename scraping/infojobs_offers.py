import requests
import pandas as pd
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

df = pd.read_csv("ofertas_infojobs.csv")
urls = df["url"].tolist()
os.makedirs("html_ofertas", exist_ok=True)

for i, url in enumerate(urls):
    try:
        print(f"Descargando {i+1}/{len(urls)}")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(f"html_ofertas/oferta_{i+1:05}.html", "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            print(f"⚠️ Código HTTP {response.status_code} en {url}")
        time.sleep(1.5)  # Respeta un ritmo humano
    except Exception as e:
        print(f"❌ Error en {url}: {e}")

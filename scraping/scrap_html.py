import os
import pandas as pd
from bs4 import BeautifulSoup
import re

def extraer_secciones_desde_descripcion(descripcion_parrafos):
    texto = "\n".join(descripcion_parrafos)
    requisitos = []

    match = re.search(r"(?i)requisitos:\s*(.*?)(?=\n\S|$)", texto, re.DOTALL)
    if match:
        bloque = match.group(1)
        requisitos = [line.strip("·•- ").strip() for line in bloque.strip().split("\n") if line.strip()]

    return requisitos

def parsear_oferta(path_html):
    try:
        with open(path_html, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        titulo_tag = soup.find("h1", class_="ij-Heading-title1")
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""

        empresa_tag = soup.find("a", class_="ij-Heading-headline2")
        empresa = empresa_tag.get_text(strip=True) if empresa_tag else ""

        items = soup.find_all("div", class_="ij-Box ij-OfferDetailHeader-detailsList-item")
        localizacion = items[0].get_text(strip=True) if len(items) > 0 else ""
        modalidad = items[1].get_text(strip=True) if len(items) > 1 else ""
        contrato = items[4].get_text(strip=True) if len(items) > 4 else ""

        requisitos_minimos = []
        dl = soup.find("dl", class_="ij-Box")
        if dl:
            dt_tags = dl.find_all("dt")
            dd_tags = dl.find_all("dd")
            for dt, dd in zip(dt_tags, dd_tags):
                clave = dt.get_text(strip=True)
                if clave.lower() == "requisitos mínimos":
                    if dd.find("ul"):
                        requisitos_minimos = [li.get_text(strip=True) for li in dd.find_all("li")]
                    elif dd.find_all("p"):
                        requisitos_minimos = [p.get_text(strip=True) for p in dd.find_all("p")]
                    else:
                        requisitos_minimos = [dd.get_text(strip=True)]

        descripcion_div = soup.find("div", class_="ij-Box mb-xl mt-l")
        descripcion = []
        if descripcion_div:
            parrafos = descripcion_div.find_all("p", class_="ij-OfferDetailDescription-Paragarph")
            descripcion = [p.get_text(strip=True) for p in parrafos]

        if not requisitos_minimos:
            requisitos_minimos = extraer_secciones_desde_descripcion(descripcion)

        descripcion_texto = "\n".join(descripcion)

        extra_info = {}
        bloques_dl = soup.find_all("dl", class_="ij-Box")
        if len(bloques_dl) > 1:
            dl_extra = bloques_dl[1]
            dt_tags = dl_extra.find_all("dt")
            dd_tags = dl_extra.find_all("dd")
            for dt, dd in zip(dt_tags, dd_tags):
                clave = dt.get_text(strip=True)
                if dd.find("ul"):
                    contenido = [li.get_text(strip=True) for li in dd.find_all("li")]
                elif dd.find("a"):
                    contenido = [a.get_text(strip=True) for a in dd.find_all("a")]
                elif dd.find_all("p"):
                    contenido = [p.get_text(strip=True) for p in dd.find_all("p")]
                else:
                    contenido = [dd.get_text(strip=True)]
                extra_info[clave] = contenido

        return {
            "titulo": titulo,
            "empresa": empresa,
            "localizacion": localizacion,
            "modalidad": modalidad,
            "contrato": contrato,
            "requisitos_minimos": requisitos_minimos,
            "descripcion": descripcion_texto,
            "tipo_industria": extra_info.get("Tipo de industria de la oferta", []),
            "categoria": extra_info.get("Categoría", []),
            "nivel": extra_info.get("Nivel", []),
            "vacantes": extra_info.get("Vacantes", []),
            "salario": extra_info.get("Salario", []),
            "beneficios_sociales": extra_info.get("Beneficios sociales", [])
        }

    except Exception as e:
        print(f"❌ Error al procesar {path_html}: {e}")
        return None

# =========================
# Bucle principal
# =========================

carpeta = "data/html_offers"
csv_salida = "data/ofertas_infojobs_details.csv"

registros = []

for nombre_archivo in os.listdir(carpeta):
    if nombre_archivo.endswith(".html"):
        ruta = os.path.join(carpeta, nombre_archivo)
        datos = parsear_oferta(ruta)
        if datos:
            registros.append(datos)
            # os.remove(ruta)  # 🔥 Borra el HTML tras procesarlo

# Cargar CSV existente si ya existe
if os.path.exists(csv_salida):
    df_existente = pd.read_csv(csv_salida, encoding="utf-8", sep=";")
else:
    df_existente = pd.DataFrame()

# Convertir a DataFrame y unir
df_nuevo = pd.DataFrame(registros)
df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)

# Guardar CSV
df_final.to_csv(csv_salida, index=False, encoding="utf-8", sep=";")

print(f"✅ Guardadas {len(df_nuevo)} nuevas ofertas en el CSV.")

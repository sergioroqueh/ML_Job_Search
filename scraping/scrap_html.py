import os
import pandas as pd
from bs4 import BeautifulSoup

# === FUNCIÓN PARA PARSEAR UNA OFERTA ===
def parsear_oferta(path_html):
    with open(path_html, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    try:
        titulo_tag = soup.find("h1", class_="ij-Heading-title1")
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""

        empresa_tag = soup.find("a", class_="ij-Heading-headline2")
        empresa = empresa_tag.get_text(strip=True) if empresa_tag else ""

        items = soup.find_all("div", class_="ij-Box ij-OfferDetailHeader-detailsList-item")
        localizacion = items[0].get_text(strip=True) if len(items) > 0 else ""
        modalidad     = items[1].get_text(strip=True) if len(items) > 1 else ""
        contrato      = items[4].get_text(strip=True) if len(items) > 4 else ""

        # Requisitos
        bloques_dl = soup.find_all("dl", class_="ij-Box")
        requisitos_dict = {}
        if bloques_dl:
            dl_requisitos = bloques_dl[0]
            for dt, dd in zip(dl_requisitos.find_all("dt"), dl_requisitos.find_all("dd")):
                clave = dt.get_text(strip=True)
                if dd.find("ul"):
                    contenido = [li.get_text(strip=True) for li in dd.find_all("li")]
                elif dd.find("a"):
                    contenido = [a.get_text(strip=True) for a in dd.find_all("a")]
                elif dd.find_all("p"):
                    contenido = [p.get_text(strip=True) for p in dd.find_all("p")]
                else:
                    contenido = [dd.get_text(strip=True)]
                requisitos_dict[clave] = contenido

        estudios_minimos      = requisitos_dict.get("Estudios mínimos", [])
        experiencia_minima    = requisitos_dict.get("Experiencia mínima", [])
        idiomas_requeridos    = requisitos_dict.get("Idiomas requeridos", [])
        conocimientos_neces   = requisitos_dict.get("Conocimientos necesarios", [])
        requisitos_minimos    = requisitos_dict.get("Requisitos mínimos", [])
        requisitos_deseados   = requisitos_dict.get("Requisitos deseados", [])

        # Descripción
        descripcion = []
        descripcion_div = soup.find("div", class_="ij-Box mb-xl mt-l")
        if descripcion_div:
            descripcion = [p.get_text(strip=True) for p in descripcion_div.find_all("p", class_="ij-OfferDetailDescription-Paragarph")]

        # Info extra (industria, categoría, etc.)
        extra_info = {}
        if len(bloques_dl) > 1:
            dl_extra = bloques_dl[1]
            for dt, dd in zip(dl_extra.find_all("dt"), dl_extra.find_all("dd")):
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

        tipo_industria     = extra_info.get("Tipo de industria de la oferta", [])
        categoria          = extra_info.get("Categoría", [])
        nivel              = extra_info.get("Nivel", [])
        vacantes           = extra_info.get("Vacantes", [])
        salario            = extra_info.get("Salario", [])
        beneficios_sociales = extra_info.get("Beneficios sociales", [])

        return {
            "titulo": titulo,
            "empresa": empresa,
            "localizacion": localizacion,
            "modalidad": modalidad,
            "contrato": contrato,
            "estudios_minimos": estudios_minimos,
            "experiencia_minima": experiencia_minima,
            "idiomas_requeridos": idiomas_requeridos,
            "conocimientos_necesarios": conocimientos_neces,
            "requisitos_minimos": requisitos_minimos,
            "requisitos_deseados": requisitos_deseados,
            "descripcion": descripcion,
            "tipo_industria": tipo_industria,
            "categoria": categoria,
            "nivel": nivel,
            "vacantes": vacantes,
            "salario": salario,
            "beneficios_sociales": beneficios_sociales
        }

    except Exception as e:
        print(f"❌ Error al procesar {path_html}: {e}")
        return None


# === RECORRER TODOS LOS HTML Y GUARDAR EN CSV ===

carpeta = "data\\html_offers"         # Ruta a la carpeta
csv_salida = "ofertas_infojobs_details.csv"   # Archivo destino

nuevos_datos = []

for archivo in os.listdir(carpeta):
    if archivo.endswith(".html"):
        ruta = os.path.join(carpeta, archivo)
        datos = parsear_oferta(ruta)
        if datos:
            nuevos_datos.append(datos)

if nuevos_datos:
    df_nuevo = pd.DataFrame(nuevos_datos)

    if os.path.exists(csv_salida):
        df_existente = pd.read_csv(csv_salida)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_csv(csv_salida, index=False)
    print(f"✅ Guardadas {len(nuevos_datos)} nuevas ofertas en el CSV.")
else:
    print("⚠️ No se procesó ninguna nueva oferta.")

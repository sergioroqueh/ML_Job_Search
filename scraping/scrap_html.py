import os
import pandas as pd
from bs4 import BeautifulSoup

# Ruta local donde tienes guardados los .html descargados
CARPETA_HTML = "D:\! 4Geeks\proyecto_personal_1\ML_Job_Search\data\html_offers"  # <-- cambia si tu carpeta tiene otro nombre
ARCHIVO_SALIDA = "infojobs_parseados.csv"

# Función auxiliar para extraer lista de textos
def get_text_list(elements):
    return [el.get_text(strip=True) for el in elements]

# Función principal de parseo
def parsear_html(path):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    def extrae_dd(label):
        dt = soup.find("dt", string=lambda s: s and label in s)
        return dt.find_next("dd").get_text(strip=True) if dt else ""

    def extrae_dd_multilinea(label):
        dt = soup.find("dt", string=lambda s: s and label in s)
        return dt.find_next("dd").get_text(separator="\n", strip=True) if dt else ""

    cabecera = soup.select(".ij-OfferDetailHeader-detailsList-item p")

    return {
        "archivo": os.path.basename(path),
        "titulo": soup.find("h1", class_="ij-Heading-title1").get_text(strip=True) if soup.find("h1", class_="ij-Heading-title1") else "",
        "empresa": soup.find("a", class_="ij-Heading-headline2").get_text(strip=True) if soup.find("a", class_="ij-Heading-headline2") else "",
        "localizacion": cabecera[0].get_text(strip=True) if len(cabecera) > 0 else "",
        "modalidad": cabecera[1].get_text(strip=True) if len(cabecera) > 1 else "",
        "salario": cabecera[2].get_text(strip=True) if len(cabecera) > 2 else "",
        "experiencia_minima": cabecera[3].get_text(strip=True) if len(cabecera) > 3 else "",
        "tipo_contrato": cabecera[4].get_text(strip=True) if len(cabecera) > 4 else "",
        "estudios_minimos": extrae_dd("Estudios mínimos"),
        "idiomas": extrae_dd("Idiomas"),
        "conocimientos": get_text_list(soup.select(".ij-OfferDetailRequirements-requiredSkills .sui-AtomTag-label")),
        "requisitos_minimos": extrae_dd_multilinea("Requisitos mínimos"),
        "requisitos_deseados": extrae_dd_multilinea("Requisitos deseados"),
        "descripcion": soup.find("div", class_="ij-Box mb-xl mt-l").get_text(separator="\n", strip=True) if soup.find("div", class_="ij-Box mb-xl mt-l") else "",
        "industria": extrae_dd("Tipo de industria"),
        "categoria": extrae_dd("Categoría"),
        "nivel": extrae_dd("Nivel"),
        "vacantes": extrae_dd("Vacantes"),
        "beneficios_sociales": extrae_dd_multilinea("Beneficios sociales")
    }

# Recorre todos los HTMLs
def procesar_carpeta(carpeta):
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith(".html")]
    print(f"Procesando {len(archivos)} archivos HTML...\n")
    return [parsear_html(f) for f in archivos]

# Ejecutar y guardar
if __name__ == "__main__":
    resultados = procesar_carpeta(CARPETA_HTML)
    df = pd.DataFrame(resultados)
    df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")
    print(f"\n✅ Guardado como: {ARCHIVO_SALIDA}")

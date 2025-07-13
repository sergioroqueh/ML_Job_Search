import time
import random
import math
import os
import pandas as pd
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ================================
# CONFIGURACIÓN DEL NAVEGADOR
# ================================

def iniciar_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """
    })

    return driver

# ================================
# ESPERA SI HAY CAPTCHA
# ================================

def esperar_captcha(driver, check_interval=2, timeout_total=180):
    print("⏳ Comprobando si hay captcha...")

    inicio = time.time()

    while True:
        try:
            textos = driver.find_elements(By.XPATH, "//*[contains(text(), 'necesitamos comprobar que no eres una máquina')]")
            visible = any(el.is_displayed() for el in textos)
        except:
            visible = False

        if visible:
            print("🔒 Captcha detectado. Esperando que lo resuelvas manualmente...")
            time.sleep(check_interval)
        else:
            break

        if time.time() - inicio > timeout_total:
            print("⛔ Tiempo agotado esperando el captcha.")
            return

    print("✅ Captcha resuelto. Esperando carga completa de ofertas...")

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ij-OfferCardContent-description-title-link"))
        )
        print("📄 Ofertas detectadas. Continuamos.")
    except:
        print("⚠️ No se detectaron ofertas tras el captcha.")

# ================================
# SCROLL HUMANO
# ================================

def scroll_humano(driver, max_scrolls=25, altura_max=800, pausa_min=0.5, pausa_max=2.0):
    ultima_pos = 0
    for i in range(max_scrolls):
        delta_scroll = random.randint(200, altura_max)
        nueva_pos = ultima_pos + delta_scroll
        driver.execute_script(f"window.scrollTo(0, {nueva_pos});")
        print(f"Scroll #{i+1}: +{delta_scroll}px → total: {nueva_pos}px")
        time.sleep(random.uniform(pausa_min, pausa_max))
        ultima_pos = nueva_pos
        altura_pagina = driver.execute_script("return document.body.scrollHeight")
        if nueva_pos >= altura_pagina:
            print("Llegamos al final de la página.")
            break
    print("Scroll humano completado.")

# ================================
# SCRAPE DE UNA KEYWORD
# ================================

def scrape_keyword(driver, keyword, nombre_archivo="ofertas_infojobs.csv", max_paginas=100):
    print(f"\n🔍 Buscando: {keyword}")
    base_url = "https://www.infojobs.net/jobsearch/search-results/list.xhtml"
    pagina = 1
    total_links = set()
    keyword_encoded = quote(keyword)

    # Leer CSV existente si hay
    if os.path.exists(nombre_archivo):
        df_existente = pd.read_csv(nombre_archivo)
        existentes = set(df_existente['url'])
    else:
        existentes = set()

    while pagina <= max_paginas:
        url = f"{base_url}?keyword={keyword_encoded}&page={pagina}"
        print(f"\n➡️ Página {pagina} → {url}")

        driver.get(url)
        time.sleep(random.uniform(3, 5))
        esperar_captcha(driver)

        # Aceptar cookies si aparecen
        try:
            aceptar = driver.find_element(By.ID, "didomi-notice-agree-button")
            if aceptar.is_displayed():
                aceptar.click()
                print("✅ Cookies aceptadas.")
                time.sleep(random.uniform(1, 2))
        except:
            pass

        scroll_humano(driver)

        # Extraer links
        links = driver.find_elements(By.CLASS_NAME, "ij-OfferCardContent-description-title-link")
        nuevas_urls = []
        for link in links:
            href = link.get_attribute("href")
            if href:
                if href.startswith("//"):
                    href = "https:" + href
                nuevas_urls.append(href)

        nuevas_unicas = list(set(nuevas_urls) - total_links)
        nuevas_unicas = [url for url in nuevas_unicas if url not in existentes]

        print(f"🔗 Nuevas ofertas en esta página: {len(nuevas_unicas)}")

        if len(nuevas_unicas) == 0:
            print("✅ Fin del listado de páginas.")
            break

        total_links.update(nuevas_unicas)

        # Guardar CSV
        if nuevas_unicas:
            df_nuevo = pd.DataFrame(nuevas_unicas, columns=["url"])
            modo = 'a' if os.path.exists(nombre_archivo) else 'w'
            header = not os.path.exists(nombre_archivo)
            df_nuevo.to_csv(nombre_archivo, index=False, mode=modo, header=header)
            existentes.update(nuevas_unicas)
            print(f"💾 Guardadas {len(nuevas_unicas)} nuevas al CSV.")

        pagina += 1
        time.sleep(random.uniform(4, 7))

    print(f"✅ Finalizada búsqueda para: {keyword} | Total enlaces únicos: {len(total_links)}")

# ================================
# LISTA DE KEYWORDS Y EJECUCIÓN
# ================================

if __name__ == "__main__":
    keywords = [
    "software developer",
    "desarrollador de software",
    "desarrollador backend",
    "backend developer",
    "desarrollador fullstack",
    "full stack developer",
    "programador java",
    "java developer",
    "programador python",
    "python developer",
    "node.js developer",
    "programador node.js",
    "desarrollador .net",
    "desarrollador php",
    "php developer",
    "frontend engineer",
    "backend engineer",
    "web programmer",
    "desarrollador react",
    "react developer"
]





    driver = iniciar_driver()
    try:
        for kw in keywords:
            scrape_keyword(driver, keyword=kw)
            time.sleep(random.uniform(10, 20))  # Pausa entre keywords
    finally:
        driver.quit()

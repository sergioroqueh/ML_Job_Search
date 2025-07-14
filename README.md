# 📊 ML Job Market Analysis

Este proyecto tiene como objetivo analizar el mercado laboral en sectores tecnológicos como *Data Science*, *Desarrollo Web* y *Ciberseguridad*, utilizando técnicas de web scraping, almacenamiento en SQL y modelos de Machine Learning.

## 🚀 Objetivos del proyecto

- Obtener una gran cantidad de ofertas laborales reales (20,000+)
- Almacenar los datos estructurados en una base de datos SQL
- Analizar la evolución de la demanda, tecnologías requeridas y salarios (si están disponibles)
- Entrenar modelos para:
  - Clasificar las ofertas según categoría
  - Predecir salario (si se puede obtener)
  - Detectar tecnologías clave por sector

## 🛠️ Tecnologías usadas

- **Python** (BeautifulSoup, Selenium, Playwright)
- **SQL** (SQLite inicialmente, con posibilidad de migrar a PostgreSQL o MySQL)
- **Pandas / NumPy**
- **Scikit-learn / XGBoost / CatBoost**
- **Flask o Streamlit** (para visualización futura)
- **Git / GitHub** (control de versiones)

## 🔍 Fuentes de datos

- [InfoJobs](https://www.infojobs.net/)
- [Indeed](https://www.indeed.com/)

> *El scraping se realiza respetando los Términos de Uso de cada sitio y únicamente con fines educativos y de investigación.*

## 📦 Estructura inicial del proyecto

```plaintext
ML_Job_Search/
│
├── scraping/
│   ├── infojobs_scraper.py
│   ├── indeed_scraper.py
│   └── urls_colectadas.csv
│
├── data/
│   └── ofertas_laborales.db
│
├── notebooks/
│   └── analisis_exploratorio.ipynb
│
├── models/
│   └── clasificador_ofertas.pkl
│
├── app/
│   └── dashboard.py
│
└── README.md

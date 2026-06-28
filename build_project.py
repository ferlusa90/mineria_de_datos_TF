import json
import shutil
from datetime import datetime
from pathlib import Path

import nbformat as nbf
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
RAW_SOURCE = ROOT / "streaming_users_dirty.json"
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
NOTEBOOKS_DIR = ROOT / "notebooks"
APP_DIR = ROOT / "app"
PAGES_DIR = APP_DIR / "pages"
REPORTS_DIR = ROOT / "reports"
LOGS_DIR = ROOT / "logs"


def ensure_dirs():
    for path in [RAW_DIR, PROCESSED_DIR, NOTEBOOKS_DIR, PAGES_DIR, REPORTS_DIR, LOGS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def normalize_text(value):
    if pd.isna(value):
        return np.nan
    return str(value).strip().lower()


def parse_login_dates(series):
    parsed = pd.to_datetime(series, errors="coerce", format="%Y-%m-%d")
    missing = parsed.isna() & series.notna()
    parsed.loc[missing] = pd.to_datetime(series.loc[missing], errors="coerce", dayfirst=True)
    missing = parsed.isna() & series.notna()
    parsed.loc[missing] = pd.to_datetime(series.loc[missing], errors="coerce")
    return parsed


def order_user_duplicates(df):
    login_tmp = parse_login_dates(df["last_login_date"])
    valid_login_tmp = login_tmp.notna() & (login_tmp <= pd.Timestamp("2026-06-28"))
    valid_watch_tmp = df["monthly_watch_time_mins"].between(0, 14400, inclusive="both")
    typical_watch = df.loc[valid_watch_tmp, "monthly_watch_time_mins"].median()
    watch_distance = (df["monthly_watch_time_mins"] - typical_watch).abs()
    watch_distance = watch_distance.where(valid_watch_tmp, np.inf)
    completeness_tmp = df.notna().sum(axis=1)
    return (
        pd.DataFrame(
            {
                "_idx": df.index,
                "_valid_login": valid_login_tmp.astype(int),
                "_valid_watch": valid_watch_tmp.astype(int),
                "_watch_distance": watch_distance,
                "_login": login_tmp,
                "_complete": completeness_tmp,
            }
        )
        .sort_values(
            ["_valid_login", "_valid_watch", "_watch_distance", "_login", "_complete", "_idx"],
            ascending=[False, False, True, False, False, True],
        )["_idx"]
    )


def run_pipeline():
    raw = pd.DataFrame(json.loads(RAW_SOURCE.read_text(encoding="utf-8")))
    df = raw.copy()
    initial_rows = len(df)
    log_rows = []

    def register(step, description):
        log_rows.append(
            {
                "Paso": step,
                "Descripción": description,
                "Filas": len(df),
                "Nulos": int(df.isna().sum().sum()),
                "Retención (%)": round(len(df) / initial_rows * 100, 2),
            }
        )

    register("00", "Carga del dataset original en una copia de trabajo.")

    df = df.drop_duplicates().reset_index(drop=True)
    register("01", "Eliminación de duplicados exactos sin modificar columnas.")

    order = order_user_duplicates(df)
    df = df.loc[order].drop_duplicates(subset="user_id", keep="first").sort_values("user_id").reset_index(drop=True)
    register("02", "Resolución de user_id repetidos priorizando fecha real, consumo mensual plausible, cercanía al consumo típico y completitud.")

    plan_map = {
        "estándar": "Estándar",
        "estandar": "Estándar",
        "std": "Estándar",
        "standard": "Estándar",
        "básico": "Básico",
        "basico": "Básico",
        "basic": "Básico",
        "premium": "Premium",
        "premium": "Premium",
        "premiun": "Premium",
    }
    country_map = {
        "argentina": "Argentina",
        "arg": "Argentina",
        "brasil": "Brasil",
        "brazil": "Brasil",
        "bra": "Brasil",
        "chile": "Chile",
        "chl": "Chile",
        "colombia": "Colombia",
        "col": "Colombia",
        "méxico": "México",
        "mexico": "México",
        "mex": "México",
        "perú": "Perú",
        "peru": "Perú",
        "per": "Perú",
        "uruguay": "Uruguay",
        "ury": "Uruguay",
    }
    genre_map = {
        "acción": "Acción",
        "accion": "Acción",
        "action": "Acción",
        "comedia": "Comedia",
        "comedy": "Comedia",
        "crime": "Crimen",
        "crimen": "Crimen",
        "documental": "Documental",
        "documentary": "Documental",
        "doc": "Documental",
        "drama": "Drama",
        "romance": "Romance",
        "thriller": "Thriller",
        "thriler": "Thriller",
    }
    df["subscription_plan"] = df["subscription_plan"].map(lambda x: plan_map.get(normalize_text(x), x))
    df["country"] = df["country"].map(lambda x: country_map.get(normalize_text(x), x))
    df["favorite_genre"] = df["favorite_genre"].map(lambda x: genre_map.get(normalize_text(x), np.nan if pd.isna(x) else x))
    register("03", "Estandarización de categorías en plan, país y género favorito.")

    df.loc[(df["age"] < 13) | (df["age"] > 100), "age"] = np.nan
    df.loc[df["monthly_watch_time_mins"] < 0, "monthly_watch_time_mins"] = np.nan
    df.loc[df["customer_support_tickets"] < 0, "customer_support_tickets"] = np.nan
    login = parse_login_dates(df["last_login_date"])
    login.loc[login > pd.Timestamp("2026-06-28")] = pd.NaT
    df["last_login_date"] = login
    register("04", "Conversión de valores imposibles a nulos: edades fuera de 13-100, tiempos negativos, tickets negativos y fechas inválidas/futuras.")

    for col in ["age", "monthly_watch_time_mins"]:
        df[col] = df.groupby(["subscription_plan", "country"], observed=True)[col].transform(lambda s: s.fillna(s.median()))
        df[col] = df[col].fillna(df[col].median())
    df["customer_support_tickets"] = df["customer_support_tickets"].fillna(df["customer_support_tickets"].median())
    df["favorite_genre"] = df.groupby(["subscription_plan", "country"], observed=True)["favorite_genre"].transform(
        lambda s: s.fillna(s.mode().iloc[0] if not s.mode().empty else np.nan)
    )
    df["favorite_genre"] = df["favorite_genre"].fillna(df["favorite_genre"].mode().iloc[0])
    median_date = df["last_login_date"].dropna().median()
    df["last_login_date"] = df["last_login_date"].fillna(median_date)
    register("05", "Imputación justificada con medianas/modas segmentadas y fecha mediana global.")

    watch_cap = df.loc[df["monthly_watch_time_mins"] <= 14400, "monthly_watch_time_mins"].quantile(0.99)
    ticket_cap = df.loc[df["customer_support_tickets"] <= 30, "customer_support_tickets"].quantile(0.99)
    df["monthly_watch_time_mins"] = df["monthly_watch_time_mins"].clip(upper=watch_cap)
    df["customer_support_tickets"] = df["customer_support_tickets"].clip(upper=ticket_cap)
    register("06", f"Winsorización superior: monthly_watch_time_mins cap={watch_cap:.1f}; customer_support_tickets cap={ticket_cap:.0f}.")

    df["age"] = df["age"].round().astype(int)
    df["customer_support_tickets"] = df["customer_support_tickets"].round().astype(int)
    df["monthly_watch_time_mins"] = df["monthly_watch_time_mins"].round(1)
    df["last_login_date"] = pd.to_datetime(df["last_login_date"]).dt.strftime("%Y-%m-%d")
    df = df[raw.columns]
    register("07", "Normalización final de tipos y exportación del dataset procesado con las mismas columnas originales.")

    df.to_csv(PROCESSED_DIR / "streaming_users_processed.csv", index=False, encoding="utf-8")
    df.to_json(PROCESSED_DIR / "streaming_users_processed.json", orient="records", force_ascii=False, indent=2)
    pd.DataFrame(log_rows).to_csv(LOGS_DIR / "pipeline_log.csv", index=False, encoding="utf-8")
    return raw, df, pd.DataFrame(log_rows), watch_cap, ticket_cap


def code_cell(source):
    return nbf.v4.new_code_cell(source.strip() + "\n")


def md_cell(source):
    return nbf.v4.new_markdown_cell(source.strip() + "\n")


COMMON_IMPORTS = """
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
ROOT = Path("..").resolve()
"""


def write_notebook(path, cells):
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb["metadata"]["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    nbf.write(nb, path)


def create_notebooks():
    pipeline_code = r'''
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path("..").resolve()
raw_path = ROOT / "data" / "raw" / "streaming_users_dirty.json"
processed_path = ROOT / "data" / "processed" / "streaming_users_processed.csv"
log_path = ROOT / "logs" / "pipeline_log.csv"

def normalizar_texto(valor):
    """Limpia espacios y pasa texto a minúsculas para mapear variantes."""
    if pd.isna(valor):
        return np.nan
    return str(valor).strip().lower()

def parsear_fechas_login(serie):
    """Intenta leer fechas en formatos frecuentes sin guardar columnas auxiliares."""
    parsed = pd.to_datetime(serie, errors="coerce", format="%Y-%m-%d")
    faltan = parsed.isna() & serie.notna()
    parsed.loc[faltan] = pd.to_datetime(serie.loc[faltan], errors="coerce", dayfirst=True)
    faltan = parsed.isna() & serie.notna()
    parsed.loc[faltan] = pd.to_datetime(serie.loc[faltan], errors="coerce")
    return parsed

def ordenar_usuarios_repetidos(df):
    """Ordena filas duplicadas por calidad sin agregar columnas al dataset final."""
    login_tmp = parsear_fechas_login(df["last_login_date"])
    login_valido_tmp = login_tmp.notna() & (login_tmp <= pd.Timestamp("2026-06-28"))
    consumo_valido_tmp = df["monthly_watch_time_mins"].between(0, 14400, inclusive="both")
    consumo_tipico = df.loc[consumo_valido_tmp, "monthly_watch_time_mins"].median()
    distancia_consumo = (df["monthly_watch_time_mins"] - consumo_tipico).abs()
    distancia_consumo = distancia_consumo.where(consumo_valido_tmp, np.inf)
    completitud_tmp = df.notna().sum(axis=1)
    return (
        pd.DataFrame({
            "_idx": df.index,
            "_login_valido": login_valido_tmp.astype(int),
            "_consumo_valido": consumo_valido_tmp.astype(int),
            "_distancia_consumo": distancia_consumo,
            "_login": login_tmp,
            "_complete": completitud_tmp
        })
        .sort_values(
            ["_login_valido", "_consumo_valido", "_distancia_consumo", "_login", "_complete", "_idx"],
            ascending=[False, False, True, False, False, True]
        )["_idx"]
    )

raw = pd.read_json(raw_path)
df = raw.copy()
filas_iniciales = len(df)
log = []

def registrar(paso, descripcion):
    """Guarda trazabilidad: paso aplicado, tamaño, nulos y retención."""
    log.append({
        "Paso": paso,
        "Descripción": descripcion,
        "Filas": len(df),
        "Nulos": int(df.isna().sum().sum()),
        "Retención (%)": round(len(df) / filas_iniciales * 100, 2)
    })

registrar("00", "Carga del dataset original en una copia de trabajo.")

# 1. Duplicados exactos: no aportan información nueva.
df = df.drop_duplicates().reset_index(drop=True)
registrar("01", "Eliminación de duplicados exactos sin modificar columnas.")

# 2. user_id repetidos: se conserva la fila con mayor calidad observable.
# Prioridad: fecha real, consumo mensual plausible, cercanía al consumo típico,
# fecha más reciente y completitud. Las columnas auxiliares son temporales.
orden = ordenar_usuarios_repetidos(df)
df = df.loc[orden].drop_duplicates(subset="user_id", keep="first").sort_values("user_id").reset_index(drop=True)
registrar("02", "Resolución de user_id repetidos priorizando fecha real, consumo mensual plausible, cercanía al consumo típico y completitud.")

# 3. Estandarización de categorías equivalentes.
mapa_plan = {"estándar":"Estándar", "estandar":"Estándar", "std":"Estándar", "standard":"Estándar",
             "básico":"Básico", "basico":"Básico", "basic":"Básico", "premium":"Premium", "premiun":"Premium"}
mapa_pais = {"argentina":"Argentina", "arg":"Argentina", "brasil":"Brasil", "brazil":"Brasil", "bra":"Brasil",
             "chile":"Chile", "chl":"Chile", "colombia":"Colombia", "col":"Colombia", "méxico":"México",
             "mexico":"México", "mex":"México", "perú":"Perú", "peru":"Perú", "per":"Perú",
             "uruguay":"Uruguay", "ury":"Uruguay"}
mapa_genero = {"acción":"Acción", "accion":"Acción", "action":"Acción", "comedia":"Comedia", "comedy":"Comedia",
               "crime":"Crimen", "crimen":"Crimen", "documental":"Documental", "documentary":"Documental",
               "doc":"Documental", "drama":"Drama", "romance":"Romance", "thriller":"Thriller", "thriler":"Thriller"}

df["subscription_plan"] = df["subscription_plan"].map(lambda x: mapa_plan.get(normalizar_texto(x), x))
df["country"] = df["country"].map(lambda x: mapa_pais.get(normalizar_texto(x), x))
df["favorite_genre"] = df["favorite_genre"].map(lambda x: mapa_genero.get(normalizar_texto(x), np.nan if pd.isna(x) else x))
registrar("03", "Estandarización de categorías en plan, país y género favorito.")

# 4. Valores imposibles: se convierten a nulo para imputarlos con criterios explícitos.
df.loc[(df["age"] < 13) | (df["age"] > 100), "age"] = np.nan
df.loc[df["monthly_watch_time_mins"] < 0, "monthly_watch_time_mins"] = np.nan
df.loc[df["customer_support_tickets"] < 0, "customer_support_tickets"] = np.nan
login = parsear_fechas_login(df["last_login_date"])
login.loc[login > pd.Timestamp("2026-06-28")] = pd.NaT
df["last_login_date"] = login
registrar("04", "Conversión de valores imposibles a nulos: edades fuera de 13-100, tiempos negativos, tickets negativos y fechas inválidas/futuras.")

# 5. Imputación: medianas para numéricas y modas para categóricas.
for col in ["age", "monthly_watch_time_mins"]:
    df[col] = df.groupby(["subscription_plan", "country"], observed=True)[col].transform(lambda s: s.fillna(s.median()))
    df[col] = df[col].fillna(df[col].median())

df["customer_support_tickets"] = df["customer_support_tickets"].fillna(df["customer_support_tickets"].median())
df["favorite_genre"] = df.groupby(["subscription_plan", "country"], observed=True)["favorite_genre"].transform(
    lambda s: s.fillna(s.mode().iloc[0] if not s.mode().empty else np.nan)
)
df["favorite_genre"] = df["favorite_genre"].fillna(df["favorite_genre"].mode().iloc[0])
df["last_login_date"] = df["last_login_date"].fillna(df["last_login_date"].dropna().median())
registrar("05", "Imputación justificada con medianas/modas segmentadas y fecha mediana global.")

# 6. Winsorización: se capean extremos superiores que distorsionan media, correlaciones y PCA.
cap_watch = df.loc[df["monthly_watch_time_mins"] <= 14400, "monthly_watch_time_mins"].quantile(0.99)
cap_tickets = df.loc[df["customer_support_tickets"] <= 30, "customer_support_tickets"].quantile(0.99)
df["monthly_watch_time_mins"] = df["monthly_watch_time_mins"].clip(upper=cap_watch)
df["customer_support_tickets"] = df["customer_support_tickets"].clip(upper=cap_tickets)
registrar("06", f"Winsorización superior: monthly_watch_time_mins cap={cap_watch:.1f}; customer_support_tickets cap={cap_tickets:.0f}.")

# 7. Tipos finales. Se respeta la estructura original: no se agregan columnas al dataset procesado.
df["age"] = df["age"].round().astype(int)
df["customer_support_tickets"] = df["customer_support_tickets"].round().astype(int)
df["monthly_watch_time_mins"] = df["monthly_watch_time_mins"].round(1)
df["last_login_date"] = pd.to_datetime(df["last_login_date"]).dt.strftime("%Y-%m-%d")
df = df[raw.columns]
registrar("07", "Normalización final de tipos y exportación del dataset procesado con las mismas columnas originales.")

df.to_csv(processed_path, index=False, encoding="utf-8")
pd.DataFrame(log).to_csv(log_path, index=False, encoding="utf-8")
pd.DataFrame(log)
'''

    write_notebook(
        NOTEBOOKS_DIR / "01_inspeccion_inicial.ipynb",
        [
            md_cell("# 01 - Inspección inicial\n\nObjetivo: comprender la estructura y calidad inicial del dataset sin aplicar transformaciones definitivas."),
            code_cell(COMMON_IMPORTS + '\nraw = pd.read_json(ROOT / "data" / "raw" / "streaming_users_dirty.json")\nraw.head()'),
            code_cell('print(f"Filas: {raw.shape[0]} | Columnas: {raw.shape[1]}")\nraw.info()'),
            code_cell('raw.isna().sum().to_frame("nulos")'),
            code_cell('pd.DataFrame({"duplicados_exactos": [raw.duplicated().sum()], "user_id_repetidos": [raw.duplicated("user_id").sum()]})'),
            code_cell('raw.describe(include="all").T'),
            code_cell('for col in ["subscription_plan", "country", "favorite_genre"]:\n    print(f"\\n{col}")\n    print(raw[col].value_counts(dropna=False).head(30))'),
            code_cell('for col in ["age", "monthly_watch_time_mins", "customer_support_tickets"]:\n    q1, q3 = raw[col].quantile([0.25, 0.75])\n    iqr = q3 - q1\n    print(f"{col}: Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}, límite superior={q3 + 1.5*iqr:.2f}")'),
            md_cell("## Observaciones iniciales\n\n- El dataset tiene usuarios de streaming con variables demográficas, consumo, plan, país, género favorito, fecha de último login y tickets de soporte.\n- Hay duplicados exactos y `user_id` repetidos, por lo que la unicidad del registro debe revisarse.\n- Las categorías presentan variantes de escritura (`Std`, `Basic`, `Premiun`, países abreviados y géneros en inglés/español).\n- Se observan edades imposibles, tiempos de visualización negativos o extremadamente altos, tickets negativos/extremos y fechas inválidas o futuras.\n- Estas evidencias orientan la limpieza; todavía no se elimina ni imputa nada en esta etapa."),
        ],
    )

    write_notebook(
        NOTEBOOKS_DIR / "02_calidad_y_limpieza.ipynb",
        [
            md_cell("# 02 - Calidad, limpieza y preparación\n\nCada decisión se documenta con evidencia, acción e impacto. La base original se preserva en `data/raw/`; todas las transformaciones se aplican sobre una copia de trabajo."),
            code_cell(pipeline_code),
            code_cell('print("Columnas originales:", list(raw.columns))\nprint("Columnas procesadas:", list(df.columns))\nprint("¿Se agregaron columnas?", list(raw.columns) != list(df.columns))'),
            code_cell('pd.read_csv(log_path)'),
            md_cell("## Decisiones principales\n\n- Duplicados: se eliminaron duplicados exactos y se resolvieron `user_id` repetidos priorizando fecha real, consumo mensual plausible, cercanía al consumo típico y completitud.\n- Categorías: se estandarizaron valores equivalentes sin crear columnas nuevas.\n- Imposibles: valores fuera de rango razonable se trataron como nulos antes de imputar.\n- Imputación: se usaron medianas por plan y país para numéricas, moda segmentada para género y fecha mediana para login.\n- Winsorización: se aplicó en consumo mensual y tickets porque los extremos distorsionaban la escala y no representaban comportamiento normal."),
        ],
    )

    write_notebook(
        NOTEBOOKS_DIR / "03_eda.ipynb",
        [
            md_cell("# 03 - Análisis exploratorio\n\nPreguntas guía: ¿cómo se distribuye el consumo?, ¿cómo se relacionan edad y consumo?, ¿qué cambia cuando agregamos soporte y plan al análisis?"),
            code_cell(COMMON_IMPORTS + '\ndf = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")\ndf.head()'),
            code_cell('df[["age", "monthly_watch_time_mins", "customer_support_tickets"]].describe().round(2)'),
            md_cell("## Análisis univariado: distribución del tiempo mensual\n\nPermite evaluar el comportamiento típico de consumo y si la winsorización dejó una escala interpretable."),
            code_cell('plt.figure(figsize=(8,4))\nsns.histplot(df["monthly_watch_time_mins"], bins=35, kde=True, color="#2f6f73")\nplt.title("Distribución del tiempo mensual de visualización")\nplt.xlabel("Minutos mensuales")\nplt.ylabel("Usuarios")\nplt.show()'),
            md_cell("Interpretación: la mayoría de usuarios se concentra en consumos medios, con una cola derecha moderada. Esto sugiere que existen usuarios intensivos, pero el consumo extremo original ya no domina la lectura."),
            md_cell("## Análisis multivariado de 2 variables: edad y consumo\n\nEvalúa si usuarios de distintas edades muestran cambios en el tiempo mensual de visualización."),
            code_cell('plt.figure(figsize=(8,5))\nsns.regplot(data=df, x="age", y="monthly_watch_time_mins", scatter_kws={"alpha":0.25, "s":18}, line_kws={"color":"#d95f02"})\nplt.title("Relación entre edad y tiempo mensual de visualización")\nplt.xlabel("Edad")\nplt.ylabel("Minutos mensuales")\nplt.show()\nprint("Correlación edad-consumo:", round(df["age"].corr(df["monthly_watch_time_mins"]), 3))'),
            md_cell("Interpretación: este gráfico permite evaluar si el consumo aumenta o disminuye con la edad. Si la correlación es baja, la edad por sí sola no explica el nivel de consumo y conviene incorporar otras variables."),
            md_cell("## Análisis multivariado de 3 variables: edad, consumo y soporte por plan\n\nAgrega `customer_support_tickets` como tamaño del punto y `subscription_plan` como color para observar perfiles más completos."),
            code_cell('plt.figure(figsize=(9,6))\nsns.scatterplot(\n    data=df,\n    x="age",\n    y="monthly_watch_time_mins",\n    hue="subscription_plan",\n    size="customer_support_tickets",\n    sizes=(20, 180),\n    alpha=0.45\n)\nplt.title("Edad, consumo mensual y tickets de soporte por plan")\nplt.xlabel("Edad")\nplt.ylabel("Minutos mensuales")\nplt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")\nplt.show()'),
            md_cell("Interpretación: al sumar plan y tickets se observa si los usuarios con mayor consumo también concentran más consultas de soporte y si ese patrón cambia entre planes. Esto es multivariado porque la lectura depende simultáneamente de edad, consumo, soporte y segmento de plan."),
            md_cell("## Análisis multivariado adicional: edad, consumo y género favorito\n\nEste cruce permite ver si los patrones de consumo por edad cambian según el contenido preferido por los usuarios."),
            code_cell('plt.figure(figsize=(10,6))\nsns.scatterplot(\n    data=df,\n    x="age",\n    y="monthly_watch_time_mins",\n    hue="favorite_genre",\n    alpha=0.38,\n    s=28\n)\nplt.title("Edad y consumo mensual según género favorito")\nplt.xlabel("Edad")\nplt.ylabel("Minutos mensuales")\nplt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")\nplt.show()'),
            code_cell('resumen_genero = (\n    df.groupby("favorite_genre")\n      .agg(\n          usuarios=("user_id", "count"),\n          edad_mediana=("age", "median"),\n          consumo_mediano=("monthly_watch_time_mins", "median"),\n          consumo_promedio=("monthly_watch_time_mins", "mean")\n      )\n      .sort_values("consumo_mediano", ascending=False)\n      .round(2)\n)\nresumen_genero'),
            md_cell("Interpretación: si un género muestra mayor consumo mediano, puede indicar una preferencia asociada a usuarios más intensivos. La edad mediana ayuda a distinguir si esa diferencia parece vinculada al perfil etario o al tipo de contenido preferido."),
            md_cell("## Apoyo multivariado: matriz de correlación\n\nResume las relaciones lineales entre las variables numéricas usadas en el EDA y PCA."),
            code_cell('corr = df[["age", "monthly_watch_time_mins", "customer_support_tickets"]].corr()\nplt.figure(figsize=(6,4))\nsns.heatmap(corr, annot=True, cmap="vlag", vmin=-1, vmax=1)\nplt.title("Correlación entre edad, consumo y soporte")\nplt.show()'),
            md_cell("Interpretación: el heatmap ayuda a confirmar si las relaciones observadas visualmente son fuertes o débiles. Correlación no implica causalidad; funciona como evidencia exploratoria."),
        ],
    )

    write_notebook(
        NOTEBOOKS_DIR / "04_pca.ipynb",
        [
            md_cell("# 04 - Escalamiento y PCA\n\nPCA se aplica sobre variables numéricas comparables luego de estandarizar. No se guardan columnas nuevas en el dataset procesado; la matriz escalada existe solo para este análisis."),
            code_cell('from pathlib import Path\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.decomposition import PCA\n\nsns.set_theme(style="whitegrid")\nROOT = Path("..").resolve()\ndf = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")\nvariables = ["age", "monthly_watch_time_mins", "customer_support_tickets"]\nX = df[variables].copy()\nX.head()'),
            md_cell("## Escalamiento\n\nLas variables tienen unidades distintas: edad en años, visualización en minutos y tickets como conteo. Se usa Z-score para que PCA no quede dominado por la variable de mayor magnitud."),
            code_cell('scaler = StandardScaler()\nX_scaled = pd.DataFrame(scaler.fit_transform(X), columns=variables)\nX_scaled.describe().round(3)'),
            code_cell('pca = PCA(n_components=3, random_state=42)\ncomponentes = pca.fit_transform(X_scaled)\nvarianza = pd.DataFrame({\n    "componente": ["PC1", "PC2", "PC3"],\n    "varianza_explicada": pca.explained_variance_ratio_,\n    "varianza_acumulada": np.cumsum(pca.explained_variance_ratio_)\n})\nvarianza'),
            code_cell('plt.figure(figsize=(7,4))\nsns.barplot(data=varianza, x="componente", y="varianza_explicada", color="#4c78a8")\nplt.plot(varianza["componente"], varianza["varianza_acumulada"], marker="o", color="#f58518")\nplt.ylim(0, 1.05)\nplt.title("Varianza explicada por componente")\nplt.ylabel("Proporción")\nplt.show()'),
            code_cell('loadings = pd.DataFrame(pca.components_.T, index=variables, columns=["PC1", "PC2", "PC3"])\nloadings.round(3)'),
            code_cell('pc_df = pd.DataFrame(componentes[:, :2], columns=["PC1", "PC2"])\npc_df["subscription_plan"] = df["subscription_plan"]\nplt.figure(figsize=(8,5))\nsns.scatterplot(data=pc_df, x="PC1", y="PC2", hue="subscription_plan", alpha=0.45, s=28)\nplt.title("Usuarios proyectados en las dos primeras componentes")\nplt.show()'),
            md_cell("## Interpretación\n\nLa varianza explicada indica cuánta información resume cada componente. Las cargas (`loadings`) muestran qué variables empujan cada eje: si `monthly_watch_time_mins` pesa fuerte en PC1, esa componente resume intensidad de consumo; si `customer_support_tickets` pesa en otra, representa fricción o necesidad de asistencia. La proyección por plan permite observar si los planes forman grupos diferenciados en el espacio numérico estandarizado."),
        ],
    )

    write_notebook(
        NOTEBOOKS_DIR / "05_conclusiones.ipynb",
        [
            md_cell("# 05 - Conclusiones\n\nLas conclusiones se apoyan en la inspección, limpieza, EDA y PCA. Se separa evidencia observada de interpretación."),
            code_cell(COMMON_IMPORTS + '\ndf = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")\nlog = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")\nlog'),
            code_cell('resumen = {\n    "usuarios_finales": len(df),\n    "retencion_final": log.iloc[-1]["Retención (%)"],\n    "consumo_mediano": df["monthly_watch_time_mins"].median(),\n    "edad_mediana": df["age"].median(),\n    "tickets_promedio": round(df["customer_support_tickets"].mean(), 2)\n}\nresumen'),
            md_cell("## Hallazgos\n\n- La base requería preparación antes del análisis: duplicados, categorías inconsistentes, nulos y extremos podían sesgar resultados.\n- El consumo mensual presenta una concentración central y una cola de usuarios intensivos; por eso la mediana y visualizaciones robustas son más informativas que mirar solo la media.\n- Las diferencias por plan y país ayudan a formular hipótesis operativas sobre uso y soporte.\n- PCA resume las variables numéricas estandarizadas sin reemplazar el análisis exploratorio; sirve para ver si consumo, edad y soporte describen perfiles diferenciados."),
            md_cell("## Limitaciones\n\n- El dataset no incluye ingresos, antigüedad del usuario, precio real pagado ni churn, por lo que no se pueden inferir causas comerciales completas.\n- La imputación reduce pérdida de datos, pero introduce supuestos documentados.\n- Las fechas de login se corrigen por calidad, no por validación externa contra sistemas reales."),
            md_cell("## Próximos pasos\n\n- Incorporar métricas temporales reales de sesiones y permanencia.\n- Analizar retención o cancelación si se agrega una variable objetivo.\n- Validar las reglas de limpieza con responsables del negocio antes de usarlas en producción."),
        ],
    )


def write_text_files(raw, processed, log_df, watch_cap, ticket_cap):
    readme = f"""# Proyecto Integrador - Minería de Datos 1

## Información general
Análisis reproducible de usuarios de una plataforma de streaming. El trabajo sigue la guía del proyecto final: inspección, calidad, EDA, PCA, aplicación Streamlit e informe.

## Objetivo del proyecto
Comprender la calidad y estructura del dataset de usuarios de streaming.
Preparar una base limpia sin modificar el archivo original.
Analizar patrones de consumo, soporte y segmentación por plan, país y género favorito.
Aplicar escalamiento y PCA sobre variables numéricas.
Comunicar resultados de forma clara y reproducible.

## Dataset
El dataset original es `streaming_users_dirty.json`.
Cada fila representa un usuario de streaming.
Incluye edad, plan, país, género favorito, tiempo mensual visto, fecha de último login y tickets de soporte.
La base original queda preservada en `data/raw/`.
La base procesada queda en `data/processed/`.
El dataset procesado conserva las mismas columnas originales.
No se agregan columnas al archivo final.

## Estructura del repositorio
`data/raw/`: dataset original.
`data/processed/`: dataset preparado.
`notebooks/`: desarrollo técnico por etapa.
`app/`: aplicación Streamlit.
`reports/`: informe final.
`logs/`: log ETL.

## Preparación y calidad de datos
Se trabajó siempre sobre una copia del dataset.
Se eliminaron duplicados exactos.
Se resolvieron `user_id` repetidos priorizando fecha real, consumo plausible, cercanía al consumo típico y completitud.
Se estandarizaron categorías de plan, país y género.
Se trataron edades imposibles, tiempos negativos, tickets negativos y fechas inválidas/futuras.
Se imputaron numéricas con medianas segmentadas y categóricas con modas.
Se aplicó winsorización superior a consumo mensual y tickets de soporte.
El proceso completo está registrado en `logs/pipeline_log.csv`.

## Resumen del análisis exploratorio
El consumo mensual muestra concentración central y cola derecha.
El análisis de 2 variables revisa edad y consumo mensual.
El análisis de 3 variables incorpora edad, consumo, tickets de soporte y plan.
Las correlaciones entre edad, consumo y soporte ayudan a evaluar relaciones lineales.
Cada resultado se interpreta en `notebooks/03_eda.ipynb` y en la app.

## Reducción de dimensionalidad
PCA se aplicó sobre `age`, `monthly_watch_time_mins` y `customer_support_tickets`.
Antes de PCA se utilizó estandarización Z-score.
El escalamiento se usó solo como matriz temporal de análisis.
No se guardaron columnas estandarizadas en el dataset final.
Los resultados están en `notebooks/04_pca.ipynb`.

## Visualización interactiva
La aplicación está en `app/`.
Enlace Streamlit Cloud: pendiente de despliegue.
Enlace GitHub: https://github.com/ferlusa90/mineria_de_datos_TF

## Cómo ejecutar localmente
Crear un entorno Python e instalar dependencias:
`pip install -r requirements.txt`
Ejecutar la aplicación:
`streamlit run app/Home.py`

## Conclusiones
La limpieza fue necesaria para evitar sesgos por duplicados, categorías inconsistentes y extremos.
La base procesada mantiene trazabilidad y conserva la estructura original.
El análisis identifica patrones de consumo y soporte útiles para preguntas comerciales.
PCA aporta una síntesis de perfiles numéricos, pero no reemplaza la interpretación exploratoria.
Las conclusiones quedan limitadas por las variables disponibles.
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    requirements = """pandas
numpy
matplotlib
seaborn
scikit-learn
plotly
streamlit
reportlab
nbformat
"""
    (ROOT / "requirements.txt").write_text(requirements, encoding="utf-8")

    home = '''from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Streaming Users - Minería de Datos", layout="wide")

st.title("Usuarios de Streaming")
st.subheader("Proyecto Integrador - Minería de Datos 1")

st.markdown("""
**Integrantes:** completar con los nombres del grupo.

**Comisión:** completar.

**Fecha:** junio de 2026.

Este proyecto analiza una base de usuarios de streaming con foco en calidad de datos,
patrones de consumo, soporte y reducción de dimensionalidad mediante PCA.

Repositorio GitHub: https://github.com/ferlusa90/mineria_de_datos_TF
""")
'''
    (APP_DIR / "Home.py").write_text(home, encoding="utf-8")

    dataset_page = '''from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
log = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")

st.title("Dataset")
st.write("Base procesada de usuarios de streaming. El archivo original se preserva sin modificaciones en `data/raw/`.")

col1, col2, col3 = st.columns(3)
col1.metric("Filas", f"{len(df):,}")
col2.metric("Columnas", df.shape[1])
col3.metric("Nulos finales", int(df.isna().sum().sum()))

st.subheader("Vista previa")
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Transformaciones principales")
st.dataframe(log, use_container_width=True)
'''
    (PAGES_DIR / "01_Dataset.py").write_text(dataset_page, encoding="utf-8")

    eda_page = '''from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")

st.title("EDA")
st.write("Análisis principal: univariado, multivariado de 2 variables y multivariado de 3 variables.")

fig1 = px.histogram(df, x="monthly_watch_time_mins", nbins=35, title="1. Univariado: distribución del tiempo mensual")
st.plotly_chart(fig1, use_container_width=True)
st.write("La mayoría de usuarios se concentra en consumos medios, con una cola derecha moderada.")

fig2 = px.scatter(df, x="age", y="monthly_watch_time_mins", opacity=0.45, title="2. Multivariado de 2 variables: edad y consumo mensual")
st.plotly_chart(fig2, use_container_width=True)
st.write("Permite evaluar si el consumo cambia con la edad. Una relación débil indica que la edad sola no explica el consumo.")

fig3 = px.scatter(df, x="age", y="monthly_watch_time_mins", color="subscription_plan", size="customer_support_tickets", opacity=0.55, title="3. Multivariado de 3 variables: edad, consumo y soporte por plan")
st.plotly_chart(fig3, use_container_width=True)
st.write("Al sumar plan y tickets se observa si los usuarios con mayor consumo también concentran mayor necesidad de soporte.")

fig4 = px.scatter(df, x="age", y="monthly_watch_time_mins", color="favorite_genre", opacity=0.5, title="4. Multivariado adicional: edad, consumo y género favorito")
st.plotly_chart(fig4, use_container_width=True)
st.write("Este cruce permite observar si los patrones de consumo por edad cambian según el género favorito.")

resumen_genero = (
    df.groupby("favorite_genre")
      .agg(
          usuarios=("user_id", "count"),
          edad_mediana=("age", "median"),
          consumo_mediano=("monthly_watch_time_mins", "median"),
          consumo_promedio=("monthly_watch_time_mins", "mean")
      )
      .sort_values("consumo_mediano", ascending=False)
      .round(2)
)
st.dataframe(resumen_genero, use_container_width=True)

corr = df[["age", "monthly_watch_time_mins", "customer_support_tickets"]].corr()
fig5 = px.imshow(corr, text_auto=True, zmin=-1, zmax=1, color_continuous_scale="RdBu_r", title="Apoyo: correlación entre variables numéricas")
st.plotly_chart(fig5, use_container_width=True)
st.write("El heatmap resume relaciones lineales entre variables numéricas; no implica causalidad.")
'''
    (PAGES_DIR / "02_EDA.py").write_text(eda_page, encoding="utf-8")

    pca_page = '''from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_processed.csv")
variables = ["age", "monthly_watch_time_mins", "customer_support_tickets"]

st.title("PCA")
st.write("Variables utilizadas:", ", ".join(variables))
st.write("Escalamiento aplicado: Z-score con `StandardScaler`.")

X_scaled = StandardScaler().fit_transform(df[variables])
pca = PCA(n_components=3, random_state=42)
pcs = pca.fit_transform(X_scaled)
varianza = pd.DataFrame({
    "componente": ["PC1", "PC2", "PC3"],
    "varianza_explicada": pca.explained_variance_ratio_,
    "varianza_acumulada": np.cumsum(pca.explained_variance_ratio_)
})

fig1 = px.bar(varianza, x="componente", y="varianza_explicada", title="Varianza explicada")
st.plotly_chart(fig1, use_container_width=True)

pc_df = pd.DataFrame(pcs[:, :2], columns=["PC1", "PC2"])
pc_df["subscription_plan"] = df["subscription_plan"]
fig2 = px.scatter(pc_df, x="PC1", y="PC2", color="subscription_plan", opacity=0.55, title="Proyección PC1-PC2 por plan")
st.plotly_chart(fig2, use_container_width=True)

st.write("Interpretación: PCA sintetiza edad, consumo y soporte en ejes comparables. La lectura depende de la varianza explicada y de las cargas de cada variable.")
'''
    (PAGES_DIR / "03_PCA.py").write_text(pca_page, encoding="utf-8")

    conclusions_page = '''import streamlit as st

st.title("Conclusiones")

st.subheader("Hallazgos")
st.write("""
La base requería limpieza antes de cualquier análisis: duplicados, categorías inconsistentes,
fechas inválidas y extremos podían distorsionar resultados. Luego de la preparación, el consumo
mensual y los tickets de soporte permiten comparar perfiles por plan y país.
""")

st.subheader("Limitaciones")
st.write("""
No se cuenta con variables como churn, antigüedad, precio pagado o satisfacción. Por eso el análisis
describe patrones, pero no permite afirmar causas comerciales completas.
""")

st.subheader("Próximos pasos")
st.write("""
Incorporar métricas temporales, variables de retención y validación de reglas de negocio para ampliar
el análisis y fortalecer las conclusiones.
""")
'''
    (PAGES_DIR / "04_Conclusiones.py").write_text(conclusions_page, encoding="utf-8")


def write_report(raw, processed, log_df):
    doc = SimpleDocTemplate(str(REPORTS_DIR / "informe_final.pdf"), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []
    sections = [
        ("Informe final - Usuarios de streaming", "Proyecto Integrador de Minería de Datos 1. Objetivo: analizar calidad, consumo, soporte y perfiles numéricos de usuarios de streaming."),
        ("Dataset y calidad inicial", f"La base original contiene {len(raw)} filas y {raw.shape[1]} columnas. Se observaron duplicados, user_id repetidos, categorías inconsistentes, nulos, fechas inválidas/futuras y valores extremos."),
        ("Limpieza y preparación", f"Se preservó el JSON original en data/raw. El dataset procesado tiene {len(processed)} filas, conserva las mismas columnas y queda documentado en logs/pipeline_log.csv. Se estandarizaron categorías, se imputaron nulos y se aplicó winsorización superior cuando los extremos distorsionaban el análisis."),
        ("Hallazgos EDA", "El consumo mensual presenta concentración central y cola derecha. El análisis de 2 variables revisa edad y consumo; el análisis de 3 variables incorpora soporte y plan para observar perfiles de uso y fricción operativa."),
        ("PCA", "Se aplicó PCA sobre age, monthly_watch_time_mins y customer_support_tickets luego de estandarizar con Z-score. PCA se usó como síntesis exploratoria y no como modelo predictivo."),
        ("Conclusiones y limitaciones", "La preparación era necesaria para lograr resultados interpretables. Las conclusiones están limitadas por la falta de variables como churn, antigüedad, precio y satisfacción. GitHub: https://github.com/ferlusa90/mineria_de_datos_TF. Streamlit queda pendiente de despliegue público."),
    ]
    for title, text in sections:
        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Paragraph(text, styles["BodyText"]))
        story.append(Spacer(1, 8))
    doc.build(story)


def main():
    ensure_dirs()
    shutil.copy2(RAW_SOURCE, RAW_DIR / "streaming_users_dirty.json")
    raw, processed, log_df, watch_cap, ticket_cap = run_pipeline()
    create_notebooks()
    write_text_files(raw, processed, log_df, watch_cap, ticket_cap)
    write_report(raw, processed, log_df)


if __name__ == "__main__":
    main()

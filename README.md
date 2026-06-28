# Proyecto Integrador - Minería de Datos 1

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

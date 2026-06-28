# Proyecto Integrador - Mineria de Datos 1

## Informacion general
Este proyecto analiza usuarios de una plataforma de streaming a partir de un dataset con problemas reales de calidad. El trabajo sigue un proceso completo: inspeccion inicial, limpieza documentada, analisis exploratorio, PCA, comunicacion en Streamlit e informe final. La idea central no es solo "hacer graficos", sino justificar cada decision con evidencia.

Repositorio GitHub: https://github.com/ferlusa90/mineria_de_datos_TF
Aplicacion Streamlit: https://mineriadedatostf-a4hvlnmrwzjjvazcprcx7q.streamlit.app/
Integrante: Sanchez Luna Fernando Emmanuel
Comision: tarde
Fecha: 28/06/2026

## Objetivo del proyecto
Comprender la estructura y calidad inicial del dataset.
Preparar una base confiable sin modificar el archivo original.
Analizar patrones de consumo, soporte y preferencias de contenido.
Comparar perfiles por plan, pais, edad y genero favorito.
Aplicar escalamiento y PCA sobre variables numericas.
Comunicar resultados de forma clara, reproducible y defendible.

## Dataset
El archivo original es `streaming_users_dirty.json`.
Cada fila representa un usuario de una plataforma de streaming.
Las variables incluyen edad, plan, pais, genero favorito, consumo mensual, ultimo login y tickets de soporte.
La base original queda preservada en `data/raw/`.
La base procesada queda en `data/processed/`.
El dataset final conserva las mismas columnas originales.
No se agregaron columnas nuevas al archivo procesado.
Las columnas estandarizadas son las categoricas: plan, pais y genero favorito.

## Estructura del repositorio
`data/raw/`: dataset original sin modificaciones.
`data/processed/`: dataset final usado en el analisis.
`notebooks/`: desarrollo tecnico por etapa.
`app/`: aplicacion Streamlit.
`reports/`: informe final en PDF.
`logs/`: registro ETL con trazabilidad del proceso.
`requirements.txt`: librerias necesarias para ejecutar el proyecto.

## Preparacion y calidad de datos
Se trabajo sobre una copia para preservar el JSON original.
Se eliminaron duplicados exactos.
Los `user_id` repetidos se resolvieron priorizando fecha real, consumo mensual plausible, cercania al consumo tipico y completitud.
Se normalizaron variantes de escritura en plan, pais y genero favorito.
Las edades fuera de 13-100, tiempos negativos, tickets negativos y fechas invalidas/futuras se trataron como nulos.
La imputacion uso medianas segmentadas para numericas y modas para categoricas.
Se aplico winsorizacion superior en consumo mensual y tickets de soporte.
El impacto de cada paso esta documentado en `logs/pipeline_log.csv`.

## Resumen del analisis exploratorio
El consumo mensual muestra una concentracion central y una cola de usuarios intensivos.
La edad por si sola no alcanza para explicar completamente el consumo.
El analisis por plan y soporte permite observar perfiles de uso con distinta friccion operativa.
El cruce entre edad, consumo y genero favorito ayuda a interpretar preferencias de contenido.
Las visualizaciones tienen interpretaciones asociadas en `notebooks/03_eda.ipynb` y en Streamlit.

## Reduccion de dimensionalidad
PCA se aplico sobre `age`, `monthly_watch_time_mins` y `customer_support_tickets`.
Antes de PCA se uso estandarizacion Z-score con `StandardScaler`.
El escalamiento fue necesario porque las variables tienen unidades distintas.
La matriz escalada se uso solo para el analisis, no se guardo como columnas nuevas.
Los resultados e interpretaciones estan en `notebooks/04_pca.ipynb`.

## Visualizacion interactiva
La aplicacion esta en `app/`.
Archivo principal: `app/Home.py`.
Repositorio GitHub: https://github.com/ferlusa90/mineria_de_datos_TF
Enlace Streamlit Cloud: https://mineriadedatostf-a4hvlnmrwzjjvazcprcx7q.streamlit.app/

## Como ejecutar localmente
Instalar dependencias:
`pip install -r requirements.txt`

Ejecutar la aplicacion:
`streamlit run app/Home.py`

Revisar notebooks:
abrir la carpeta `notebooks/` y ejecutar los archivos en orden del 01 al 05.

## Conclusiones
La limpieza fue necesaria para evitar decisiones basadas en ruido.
La base final queda trazable, sin nulos, sin duplicados y con estructura original preservada.
El consumo mensual, el soporte y las preferencias de genero permiten describir perfiles de usuario.
PCA ayuda a resumir variables numericas, pero no reemplaza la interpretacion del EDA.
Las conclusiones son descriptivas y quedan limitadas por las variables disponibles.

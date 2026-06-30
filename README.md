# Proyecto Integrador - Mineria de Datos 1

## Informacion general
Este proyecto analiza usuarios de una plataforma de streaming a partir de un dataset con problemas reales de calidad. El trabajo sigue un proceso completo: inspeccion inicial, limpieza documentada, analisis exploratorio, PCA, comunicacion en Streamlit e informe final.

La idea central es trabajar como un analista de datos junior: antes de limpiar se revisa la evidencia, despues se aplica una regla explicita y finalmente se controla el impacto de la decision.

Repositorio GitHub: https://github.com/ferlusa90/mineria_de_datos_TF  
Aplicacion Streamlit: https://mineriadedatostf-a4hvlnmrwzjjvazcprcx7q.streamlit.app/

Integrante: Sanchez Luna Fernando Emmanuel  
Comision: ITSE NODO TARDE  
Fecha: 28/06/2026

## Objetivo del proyecto
Comprender la estructura y calidad inicial del dataset.  
Preparar una base confiable sin modificar el archivo original.  
Mostrar el codigo usado para detectar problemas antes de corregirlos.  
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

## Estructura del repositorio
`data/raw/`: dataset original sin modificaciones.  
`data/processed/`: dataset final usado en el analisis.  
`notebooks/`: desarrollo tecnico por etapa.  
`app/`: aplicacion Streamlit.  
`reports/`: informe final en PDF.  
`logs/`: registro ETL con trazabilidad del proceso.  
`requirements.txt`: librerias necesarias para ejecutar el proyecto.

## Preparacion y calidad de datos
El notebook principal de limpieza es `notebooks/02_calidad_y_limpieza.ipynb`.

La limpieza se documento con una secuencia de trabajo:

1. Diagnosticar el problema.
2. Mostrar codigo de inspeccion.
3. Aplicar una regla de limpieza.
4. Registrar el impacto en `logs/pipeline_log.csv`.
5. Controlar que el resultado final no tenga nulos ni duplicados.

Ejemplo: antes de eliminar duplicados se ejecuta codigo para ver cuantas filas estan repetidas:

```python
duplicados_exactos = raw[raw.duplicated(keep=False)]
user_id_repetidos = raw[raw.duplicated("user_id", keep=False)]

print(raw.duplicated().sum())
print(raw.duplicated("user_id").sum())
user_id_repetidos.sort_values("user_id").head(20)
```

Luego se eliminan duplicados exactos porque no aportan informacion nueva. Para `user_id` repetidos se usa un criterio de calidad, no una eliminacion al azar:

1. Fecha de login valida y no futura.
2. Consumo mensual plausible.
3. Consumo mas cercano al consumo tipico.
4. Login mas reciente.
5. Mayor completitud de campos.

Tambien se estandarizaron categorias equivalentes, se marcaron valores imposibles como nulos, se imputaron faltantes con medianas/modas y se aplico winsorizacion superior para reducir el efecto de extremos.

Resultado final:

- Filas originales: 8160.
- Filas finales: 8000.
- Nulos finales: 0.
- Duplicados exactos finales: 0.
- `user_id` repetidos finales: 0.
- Retencion final: 98.04%.

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

La pagina Dataset de Streamlit incluye diagnostico inicial, logica de limpieza y fragmentos de codigo para que el proceso sea auditable.

## Como ejecutar localmente
Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicacion:

```bash
streamlit run app/Home.py
```

Revisar notebooks: abrir la carpeta `notebooks/` y ejecutar los archivos en orden del 01 al 05.

## Conclusiones
La limpieza fue necesaria para evitar decisiones basadas en ruido.  
La base final queda trazable, sin nulos, sin duplicados y con estructura original preservada.  
El consumo mensual, el soporte y las preferencias de genero permiten describir perfiles de usuario.  
PCA ayuda a resumir variables numericas, pero no reemplaza la interpretacion del EDA.  
Las conclusiones son descriptivas y quedan limitadas por las variables disponibles.

La conclusion metodologica es la mas importante: en mineria de datos no conviene interpretar sin antes revisar calidad, justificar transformaciones y validar el resultado.

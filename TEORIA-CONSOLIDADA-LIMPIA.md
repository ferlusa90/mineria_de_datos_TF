# Teoria consolidada - Mineria de datos

---



---

# Clase 1 — Datos vs Información

Fuente: Clase 1 — Datos vs Información

## Titulos detectados
- Sin titulos detectados

## Texto importante
- Requisitos de finalización Haga clic en MD1 - Clase 1.pdf para ver el archivo.


---

# Clase 2 — Análisis Univariado

Fuente: Clase 2 — Análisis Univariado

## Titulos detectados
- 🎯 Objetivo
- 🚀 Comencemos

## Texto importante
- Calcular e interpretar estadísticos descriptivos sobre variables numéricas, distinguiendo cuándo cada medida es apropiada y qué información aporta sobre los datos.

- En la clase anterior aprendimos a clasificar variables. Hoy damos el siguiente paso: medirlas.

- Cuando tenemos un conjunto de datos con cientos o miles de filas, no podemos leer cada valor uno por uno. Necesitamos formas de resumir esa información en unos pocos números que capturen lo esencial. Eso es lo que hacen los estadísticos descriptivos.

- Pero hay una trampa frecuente: calcular sin interpretar. Un promedio sin contexto es solo un número. El objetivo de esta clase no es saber usar las funciones de Python, es saber leer lo que los resultados están diciendo.

- Vamos a trabajar con el dataset Titanic. No porque sea el más moderno, sino porque cada fila representa una persona real. Eso cambia la forma en que miramos los números.

- Calcular e interpretar medidas de tendencia central

- Calcular e interpretar medidas de dispersión

- Usar describe() para obtener un resumen completo de un dataset

- Identificar cuándo el promedio engaña y qué usar en su lugar


---

# Clase 6 — Limpieza y preparación de datos

Fuente: 2. Capítulo 2 — Detección y Tratamiento de Datos Faltantes

## Titulos detectados
- 2. Capítulo 2 — Detección y Tratamiento de Datos Faltantes

## Texto importante

- Detección y Tratamiento de Datos Faltantes

- Un dato faltante es una celda sin valor en un conjunto de datos. El elemento central no es cuántos faltantes hay, sino por qué faltan. El mecanismo se describe mediante la probabilidad de que un valor esté ausente, explicando si esa ausencia depende de otros datos observados, del propio valor faltante o de nada. Esto define si un tratamiento (como imputar o eliminar) será válido o introducirá un sesgo grave.

- MCAR — Missing Completely At Random La probabilidad de falta es independiente de cualquier dato, observado o no. Es el escenario más favorable: eliminar filas con valores faltantes no introduce sesgo. Sin embargo, es el menos frecuente en la práctica. Ejemplo: un técnico olvidó registrar una medición al azar durante el turno.

- MAR — Missing At Random La probabilidad de falta depende de variables observadas, no del valor faltante en sí. La imputación es válida si se condicionan correctamente esas variables. Ejemplo: en un dataset de sensores, la falta de temperatura ocurre principalmente durante el turno nocturno (variable "turno" está disponible). Controlando por turno, la falta es explicable.

- MNAR — Missing Not At Random La probabilidad de falta depende del propio valor no observado. Es el caso más problemático: cualquier imputación sin modelar el mecanismo introduce sesgo. Ejemplo: pacientes con ingresos más altos no declaran su salario porque consideran la pregunta intrusiva. La variable "ingreso" está correlacionada con su propia ausencia.

- Utilizamos datos reales del Titanic para identificar patrones de valores faltantes. El objetivo es decidir cómo tratar la variable 'age' (edad) basándonos en su relación con la clase del pasajero ('pclass' 1, 2 o 3). Se considera que el orden de las clases tiene significado social y económico, no una magnitud continua.

- import pandas as pd import seaborn as sns # Cargar datos df = sns.load_dataset('titanic') # 1. Porcentaje de faltantes por variable faltantes = df.isnull().sum() porcentaje = (faltantes / len(df) * 100).round(2) print("=== Faltantes iniciales ===") print(pd.DataFrame({'Faltantes': faltantes, '%': porcentaje}).query('Faltantes > 0')) # 2. ¿La falta de 'age' depende de la clase? tasa_falta_por_clase = df.groupby('pclass')['age'].apply( lambda x: x.isnull().mean() * 100 ).round(2) print("\n=== Tasa de falta en 'age' por clase ===") print(tasa_falta_por_clase) # 3. Tratamiento diferenciado # Caso 'age': imputar con mediana de cada grupo (por clase) df['age_imputada'] = df.groupby('pclass')['age'].transform( lambda x: x.fillna(x.median()) ) # Caso 'deck': eliminar por exceso de faltantes (>70%) df_limpio = df.drop(columns=['deck'])

- import pandas as pd import seaborn as sns # Cargar datos df = sns.load_dataset('titanic') # 1. Porcentaje de faltantes por variable faltantes = df.isnull().sum() porcentaje = (faltantes / len(df) * 100).round(2) print("=== Faltantes iniciales ===") print(pd.DataFrame({'Faltantes': faltantes, '%': porcentaje}).query('Faltantes > 0')) # 2. ¿La falta de 'age' depende de la clase? tasa_falta_por_clase = df.groupby('pclass')['age'].apply( lambda x: x.isnull().mean() * 100 ).round(2) print("\n=== Tasa de falta en 'age' por clase ===") print(tasa_falta_por_clase) # 3. Tratamiento diferenciado # Caso 'age': imputar con mediana de cada grupo (por clase) df['age_imputada'] = df.groupby('pclass')['age'].transform( lambda x: x.fillna(x.median()) ) # Caso 'deck': eliminar por exceso de faltantes (>70%) df_limpio = df.drop(columns=['deck'])

- Representación simplificada de los resultados

- deck: 688 faltantes (77.22%)age: 177 faltantes (19.87%)embark_town: 2 faltantes (0.22%)embarked: 2 faltantes (0.22%)

- Tabla 2: Tasa de falta en 'age' según clase del pasajero

- Clase 1 (primera): 5.65% de edades faltantesClase 2 (segunda): 11.37%Clase 3 (tercera): 26.38%

- ¿Qué significa este resultado?La tasa de falta en edad no es uniforme: los pasajeros de tercera clase tienen cinco veces más probabilidad de tener su edad faltante que los de primera clase. Esto descarta el mecanismo MCAR (aleatorio completo). Como la falta depende de una variable observada (la clase), el mecanismo es MAR (Missing At Random). El porcentaje global del 19.87% ocultaba completamente este patrón.

- ¿Qué decisión permite tomar?No se debe imputar con la mediana global de edad. Eso mezclaría distribuciones etarias muy distintas. La decisión correcta es imputar por grupo (dentro de cada clase).Consecuencia de no hacerlo: Los pasajeros de tercera clase (mayoría jóvenes) recibirían edades más altas de primera clase, generando un modelo que sobreestima la edad en grupos populares y subestima en grupos privilegiados.

- Error común de interpretaciónCreer que "solo el 19.87% de faltantes es bajo, así que puedo eliminar esas filas o imputar con la media". Eliminar filas con edad faltante (177 casos) eliminaría muchos pasajeros de tercera clase justo donde hay más faltantes, destruyendo la representatividad de ese grupo social.

- Cuándo usarlo: Antes de cualquier modelo predictivo. Especialmente en datos con grupos naturales (clases sociales, regiones, turnos laborales).

- Cuándo no usarlo: Si el porcentaje de faltantes es mínimo (<1%) y el mecanismo es MCAR comprobado. Tampoco si la variable es irrelevante para el análisis.

- Limitaciones: Este diagnóstico solo detecta MAR frente a MCAR. No puede distinguir MAR de MNAR sin información externa o experimentos.

- Buenas prácticas: Siempre comparar tasas de falta entre categorías. Documentar el mecanismo inferido. Imputar con estadísticos grupales (mediana por clase) en lugar de globales.

- En el ejemplo del Titanic, ¿cómo cambiaría tu tratamiento si descubrieras que los pasajeros de tercera clase con edad faltante son en su mayoría niños no acompañados (dato no registrado en el dataset)?

- (Desafío) Si un sensor IoT de temperatura falla más cuando la temperatura exterior supera los 40°C (dato que no registra por la falla), ¿qué mecanismo es y por qué ninguna imputación simple lo solucionaría?


---

# Clase 6 — Limpieza y preparación de datos

Fuente: 3. Capítulo 3 — Detección y Tratamiento de Outliers

## Titulos detectados
- 3. Capítulo 3 — Detección y Tratamiento de Outliers

## Texto importante

- Un outlier es un valor que se aleja significativamente del patrón general de los datos. El método más común para detectarlos usa el rango intercuartílico (IQR), que mide la dispersión central. Los límites se calculan como Q1 - 1.5*IQR (inferior) y Q3 + 1.5*IQR (superior). Valores fuera de estos límites son outliers potenciales. Lo importante no es si un valor es outlier, sino por qué lo es: error, evento real explicable, o parte natural de una distribución asimétrica.

- Analizamos el monto de la cuenta ('total_bill') en un restaurante. Queremos decidir si los valores altos son errores, eventos especiales o simplemente cuentas caras normales en una distribución con asimetría positiva (más valores bajos y una cola larga hacia la derecha).

- import pandas as pd import seaborn as sns import numpy as np df = sns.load_dataset('tips') # 1. Estadísticas iniciales print("=== Estadísticas de 'total_bill' ===") print(df['total_bill'].describe().round(2)) # 2. Detectar outliers con IQR (k=1.5 y k=3.0) Q1 = df['total_bill'].quantile(0.25) Q3 = df['total_bill'].quantile(0.75) IQR = Q3 - Q1 limite_sup_k1 = Q3 + 1.5 * IQR limite_sup_k3 = Q3 + 3.0 * IQR outliers_k1 = df[df['total_bill'] > limite_sup_k1] outliers_k3 = df[df['total_bill'] > limite_sup_k3] print(f"\nLímite (k=1.5): {limite_sup_k1:.2f} → {len(outliers_k1)} outliers") print(f"Límite (k=3.0): {limite_sup_k3:.2f} → {len(outliers_k3)} outliers extremos") # 3. ¿Cuánto influyen en la media y mediana? media_con = df['total_bill'].mean() media_sin = df[df['total_bill'] <= limite_sup_k1]['total_bill'].mean() mediana_con = df['total_bill'].median() mediana_sin = df[df['total_bill'] <= limite_sup_k1]['total_bill'].median() print(f"\n=== Influencia de los 7 outliers ===") print(f"Media: con={media_con:.2f} → sin={media_sin:.2f} (diferencia: {media_con-media_sin:.2f})") print(f"Mediana: con={mediana_con:.2f} → sin={mediana_sin:.2f} (diferencia: {mediana_con-mediana_sin:.2f})") # 4. Comparar asimetría (skewness) según tratamiento df['winsorizado'] = df['total_bill'].clip(upper=limite_sup_k1) df['log_transformado'] = np.log1p(df['total_bill']) print(f"\n=== Asimetría (skewness) - cuanto más cerca de 0, más simétrica ===") print(f"Original: {df['total_bill'].skew():.3f}") print(f"Winsorizado (acotar valores altos): {df['winsorizado'].skew():.3f}") print(f"Log transformado: {df['log_transformado'].skew():.3f}")

- import pandas as pd import seaborn as sns import numpy as np df = sns.load_dataset('tips') # 1. Estadísticas iniciales print("=== Estadísticas de 'total_bill' ===") print(df['total_bill'].describe().round(2)) # 2. Detectar outliers con IQR (k=1.5 y k=3.0) Q1 = df['total_bill'].quantile(0.25) Q3 = df['total_bill'].quantile(0.75) IQR = Q3 - Q1 limite_sup_k1 = Q3 + 1.5 * IQR limite_sup_k3 = Q3 + 3.0 * IQR outliers_k1 = df[df['total_bill'] > limite_sup_k1] outliers_k3 = df[df['total_bill'] > limite_sup_k3] print(f"\nLímite (k=1.5): {limite_sup_k1:.2f} → {len(outliers_k1)} outliers") print(f"Límite (k=3.0): {limite_sup_k3:.2f} → {len(outliers_k3)} outliers extremos") # 3. ¿Cuánto influyen en la media y mediana? media_con = df['total_bill'].mean() media_sin = df[df['total_bill'] <= limite_sup_k1]['total_bill'].mean() mediana_con = df['total_bill'].median() mediana_sin = df[df['total_bill'] <= limite_sup_k1]['total_bill'].median() print(f"\n=== Influencia de los 7 outliers ===") print(f"Media: con={media_con:.2f} → sin={media_sin:.2f} (diferencia: {media_con-media_sin:.2f})") print(f"Mediana: con={mediana_con:.2f} → sin={mediana_sin:.2f} (diferencia: {mediana_con-mediana_sin:.2f})") # 4. Comparar asimetría (skewness) según tratamiento df['winsorizado'] = df['total_bill'].clip(upper=limite_sup_k1) df['log_transformado'] = np.log1p(df['total_bill']) print(f"\n=== Asimetría (skewness) - cuanto más cerca de 0, más simétrica ===") print(f"Original: {df['total_bill'].skew():.3f}") print(f"Winsorizado (acotar valores altos): {df['winsorizado'].skew():.3f}") print(f"Log transformado: {df['log_transformado'].skew():.3f}")

- Representación simplificada de los resultados

- Estadísticas de 'total_bill' (244 cuentas)Mínimo: $3.07 | 25%: $13.35 | Mediana: $17.80 | Media: $19.79 | 75%: $24.13 | Máximo: $50.81

- Detección de outliers (solo límite superior porque no hay valores mínimos anómalos)Con k=1.5 → límite $40.30 → 7 cuentas por encima (desde $40.42 hasta $50.81)Con k=3.0 → límite $56.47 → 0 outliers extremos

- Influencia de eliminar esos 7 valoresMedia baja de $19.79 a $18.96 (diferencia de $0.83)Mediana baja de $17.80 a $17.68 (diferencia de $0.12)

- Asimetría (skewness) original y transformadaOriginal: 1.125 (cola larga a la derecha)Winsorizado: 0.864Log transformado: 0.218 (prácticamente simétrica)

- ¿Qué significa este resultado?Los 7 valores entre $40 y $51 son outliers moderados, no extremos. Como no hay ningún valor que supere el límite para k=3.0 ($56.47), esto indica que no son errores de medición sino valores reales de cuentas muy altas. La asimetría original de 1.125 confirma que la variable tiene una cola natural hacia la derecha. Estos 7 valores son parte de esa cola, no anomalías aisladas.

- ¿Qué decisión permite tomar?No eliminar estos 7 registros. Eliminarlos baja la media en $0.83 pero apenas toca la mediana ($0.12). Esto significa que la mediana es robusta (no sensible a outliers) mientras que la media es sensible. El tratamiento recomendado es transformar la variable (logaritmo reduce la asimetría a 0.218) o usar la mediana como medida central, no la media.Consecuencia de eliminarlos sin justificación: Subestimar el gasto real de clientes de alto consumo, sesgando cualquier modelo de predicción de propinas o segmentación de clientes.

- Error común de interpretaciónVer "7 outliers detectados" y automáticamente eliminarlos. El número de outliers no es una decisión, solo una detección. En distribuciones asimétricas (como ingresos, precios o cuentas de restaurante), el criterio k=1.5 siempre encontrará outliers en la cola larga. Eliminarlos recorta artificialmente la variabilidad real del fenómeno.

- Cuándo usarlo: Para variables numéricas con distribución aproximadamente simétrica o cuando necesitas identificar errores de captura (ej: edad = 150 años).

- Cuándo no usarlo: En distribuciones muy asimétricas (salarios, precios de vivienda) o cuando los outliers son precisamente lo que te interesa (detección de fraude, fallas raras de maquinaria).

- Limitaciones: IQR asume simetría. Para distribuciones asimétricas, genera falsos outliers en la cola larga. Tampoco detecta outliers en múltiples dimensiones (combinaciones anómalas de dos variables).

- Buenas prácticas: Medir la influencia real (comparar media con y sin outlier). Si la mediana cambia poco, el outlier no es problemático. Preferir winsorización (acotar al límite) o transformación logarítmica sobre eliminación.

- Si estás modelando ingresos de una población donde el 1% más rico gana 100 veces más que la mediana, y el IQR detecta ese 1% como outlier, ¿deberías eliminarlos para que el modelo "funcione mejor"? ¿Qué perderías?

- (Desafío) En un estudio médico, un paciente tiene un valor de glucosa de 450 mg/dL (normal <100). Resulta que ese paciente tiene diabetes no diagnosticada previamente. ¿Qué tipo de outlier es? ¿Por qué eliminarlo sería un error ético y científico?


---

# Clase 6 — Limpieza y preparación de datos

Fuente: 4. Capítulo 4 — Preparación Práctica de Datasets para Análisis

## Titulos detectados
- 4. Capítulo 4 — Preparación Práctica de Datasets para Análisis

## Texto importante

- Preparación Práctica de Datasets para Análisis

- La preparación de datos es un proceso iterativo que transforma datos crudos en una estructura analíticamente válida. No es una lista de tareas lineales. Cada operación de limpieza puede revelar nuevos problemas ocultos que no eran visibles antes. La métrica clave es la retención estructural: qué porcentaje de la información original (filas × columnas) sobrevive al pipeline. Esto permite cuantificar el costo de la limpieza y detectar si una operación está eliminando demasiada información útil.

- Procesamos un dataset de ventas que simula problemas reales: tipos de dato incorrectos, duplicados, valores inválidos (montos negativos), outliers extremos, escrituras inconsistentes en nombres, y valores faltantes. Aplicamos un pipeline de 6 pasos, registrando el estado tras cada uno para auditar qué pierde y por qué.

- import pandas as pd import numpy as np # 1. Crear dataset sintético con problemas intencionales np.random.seed(42) df_raw = pd.DataFrame({ 'id_venta': range(1, 301), 'vendedor': np.random.choice(['Ana', 'Luis', 'ana', 'LUIS', 'Marta'], 300), 'monto': np.random.lognormal(7, 0.5, 300), 'unidades': np.random.randint(1, 50, 300).astype(str), # tipo incorrecto 'descuento': np.random.choice([0, 5, 10, 15, np.nan], 300) }) # Añadir duplicados y valores inválidos df_raw = pd.concat([df_raw, df_raw.iloc[:15]], ignore_index=True) df_raw.loc[0:4, 'monto'] = [-500, 0, 1e7, -1, 0] # inválidos df = df_raw.copy() # Preservar original log = [] # Para auditar def auditar(df, paso, desc): log.append({'Paso': paso, 'Descripción': desc, 'Filas': len(df), 'Nulos': df.isnull().sum().sum(), 'Retención %': round(len(df)/315*100, 2)}) auditar(df, 0, 'Original') # Paso 1: Corregir tipos df['unidades'] = pd.to_numeric(df['unidades'], errors='coerce') auditar(df, 1, 'Corregir tipos') # Paso 2: Eliminar duplicados (sin id_venta) df = df.drop_duplicates(subset=['vendedor', 'monto', 'unidades', 'descuento']) auditar(df, 2, 'Eliminar duplicados') # Paso 3: Normalizar texto (requiere dominio) df['vendedor'] = df['vendedor'].str.title() auditar(df, 3, 'Normalizar vendedor') # Paso 4: Eliminar montos inválidos (negativos o cero) df = df[df['monto'] > 0] auditar(df, 4, 'Eliminar monto ≤ 0') # Paso 5: Winsorizar outliers extremos (k=3.0) Q1, Q3 = df['monto'].quantile([0.25, 0.75]) limite = Q3 + 3.0 * (Q3 - Q1) df['monto'] = df['monto'].clip(upper=limite) auditar(df, 5, f'Winsorizar outliers (k=3, límite {limite:.0f})') # Paso 6: Imputar nulos en descuento (mediana por grupo) df['descuento'] = df.groupby('vendedor')['descuento'].transform( lambda x: x.fillna(x.median())) auditar(df, 6, 'Imputar descuento') # Mostrar auditoría log_df = pd.DataFrame(log) print(log_df.to_string(index=False)) print(f"\nRetención final: {log_df['Retención %'].iloc[-1]}%")

- import pandas as pd import numpy as np # 1. Crear dataset sintético con problemas intencionales np.random.seed(42) df_raw = pd.DataFrame({ 'id_venta': range(1, 301), 'vendedor': np.random.choice(['Ana', 'Luis', 'ana', 'LUIS', 'Marta'], 300), 'monto': np.random.lognormal(7, 0.5, 300), 'unidades': np.random.randint(1, 50, 300).astype(str), # tipo incorrecto 'descuento': np.random.choice([0, 5, 10, 15, np.nan], 300) }) # Añadir duplicados y valores inválidos df_raw = pd.concat([df_raw, df_raw.iloc[:15]], ignore_index=True) df_raw.loc[0:4, 'monto'] = [-500, 0, 1e7, -1, 0] # inválidos df = df_raw.copy() # Preservar original log = [] # Para auditar def auditar(df, paso, desc): log.append({'Paso': paso, 'Descripción': desc, 'Filas': len(df), 'Nulos': df.isnull().sum().sum(), 'Retención %': round(len(df)/315*100, 2)}) auditar(df, 0, 'Original') # Paso 1: Corregir tipos df['unidades'] = pd.to_numeric(df['unidades'], errors='coerce') auditar(df, 1, 'Corregir tipos') # Paso 2: Eliminar duplicados (sin id_venta) df = df.drop_duplicates(subset=['vendedor', 'monto', 'unidades', 'descuento']) auditar(df, 2, 'Eliminar duplicados') # Paso 3: Normalizar texto (requiere dominio) df['vendedor'] = df['vendedor'].str.title() auditar(df, 3, 'Normalizar vendedor') # Paso 4: Eliminar montos inválidos (negativos o cero) df = df[df['monto'] > 0] auditar(df, 4, 'Eliminar monto ≤ 0') # Paso 5: Winsorizar outliers extremos (k=3.0) Q1, Q3 = df['monto'].quantile([0.25, 0.75]) limite = Q3 + 3.0 * (Q3 - Q1) df['monto'] = df['monto'].clip(upper=limite) auditar(df, 5, f'Winsorizar outliers (k=3, límite {limite:.0f})') # Paso 6: Imputar nulos en descuento (mediana por grupo) df['descuento'] = df.groupby('vendedor')['descuento'].transform( lambda x: x.fillna(x.median())) auditar(df, 6, 'Imputar descuento') # Mostrar auditoría log_df = pd.DataFrame(log) print(log_df.to_string(index=False)) print(f"\nRetención final: {log_df['Retención %'].iloc[-1]}%")

- Representación simplificada de los resultados

- Auditoría del pipelinePaso 0 (Original): 315 filas, 87 nulos, retención 100%Paso 1 (Corregir tipos): 315 filas, 87 nulos, retención 100%Paso 2 (Eliminar duplicados): 300 filas, 78 nulos, retención 95.2%Paso 3 (Normalizar vendedor): 300 filas, 78 nulos, retención 95.2%Paso 4 (Eliminar monto ≤ 0): 295 filas, 72 nulos, retención 93.7%Paso 5 (Winsorizar outliers): 295 filas, 72 nulos, retención 93.7%Paso 6 (Imputar descuento): 295 filas, 0 nulos, retención 93.7%

- ¿Qué significa este resultado?Partimos de 315 filas y terminamos con 295 (pérdida de 20 filas). La pérdida ocurre en dos momentos justificados: 15 duplicados exactos (error de carga) y 5 montos inválidos (negativos o cero, imposibles en ventas). La retención del 93.7% es aceptable. importante: la corrección de tipos (Paso 1) no generó nuevos nulos. Si lo hubiera hecho, indicaría un problema oculto: valores no numéricos en 'unidades' que no detectamos en la inspección inicial.

- ¿Qué decisión permite tomar?El pipeline es válido para análisis descriptivo o modelos de predicción de ventas. La pérdida está concentrada en errores documentados, no en eliminaciones arbitrarias. La imputación de 'descuento' por grupo es correcta porque el mecanismo es MAR (depende del vendedor). Sin embargo, no deberíamos imputar 'satisfacción' si existiera, porque podría ser MNAR.Consecuencia de no auditar: Si un modelo futuro funciona mal, no sabríamos si el problema estaba en los datos originales o fue introducido al imputar montos inválidos o winsorizar outliers.

- Error común de interpretaciónAplicar df.dropna() al inicio "para limpiar rápido". En este dataset, dropna() eliminaría todas las filas con nulos en 'descuento' (27 filas), reduciendo la retención a 268 filas (85%), cuando la imputación por grupo permite conservar esos datos sin introducir sesgo. La eliminación prematura de nulos es una de las principales causas de pérdida innecesaria de información.

- Cuándo usarlo: Siempre. Todo proyecto de análisis debe tener un pipeline auditable. Especialmente crítico en entornos regulados (salud, finanzas) donde cada transformación debe justificarse.

- Cuándo no usarlo: En prototipos exploratorios muy rápidos con datos ya limpios. Pero incluso allí, registrar el estado inicial vs final ayuda a no confundir hallazgos reales con artefactos de limpieza.

- Limitaciones: La retención estructural no detecta sesgos sutiles. Imputar 100% de los nulos puede dar retención 100% pero un sesgo enorme si el mecanismo era MNAR y se imputó mal.

- Buenas prácticas: Preservar el original inmutable (df_raw). Auditar tras cada operación. Documentar decisiones de dominio (por qué se usa mediana y no media, por qué se elimina o winsoriza). Si una operación genera nulos nuevos, detenerse e investigar.

- En el ejemplo, el Paso 4 elimina montos negativos y ceros. ¿Qué decisión diferente tomarías si estuvieras analizando devoluciones en lugar de ventas? ¿Cómo cambiaría la interpretación de "valor inválido"?

- (Desafío) Registraste una retención del 93.7%, pero tu modelo de predicción de ventas funciona mal. El cliente exige saber si el pipeline causó el problema. ¿Qué información del log te permite defender o refutar esa acusación? ¿Qué métrica adicional auditarías?


---

# Clase 6 — Limpieza y preparación de datos

Fuente: 5. Capítulo 5 — Resumen

## Titulos detectados
- 5. Capítulo 5 — Resumen
- ✅ Lo que vimos hoy
- 📌 Datos faltantes
- 📌 Outliers
- 📌 Transformación
- 🔍 Dato aplicado

## Texto importante

- Preparamos datos reales para análisis. Aprendimos a detectar problemas, tomar decisiones conscientes y evitar caer en "limpiar por limpiar".

- Responden: ¿qué hago con lo que no está?

- Diferenciar ausencia aleatoria de ausencia sistemática

- Eliminar solo si pocos casos y al azar

- Imputar con mediana/moda, no con media en presencia de outliers

- Responden: ¿valor extremo o error de medición?

- Porcentaje de datos fuera del rango esperado

- Decidir: mantener, transformar o eliminar según contexto

- Responden: ¿cambio la escala para ver mejor?

- Logaritmo para asimetrías fuertes (edad, precio)

- Estandarizar cuando combinamos variables diferentes

- No transformar por moda, transformar por necesidad analítica

- 🎯 Regla práctica: Antes de limpiar, pregúntate: ¿este dato faltante o extremo aporta información sobre el fenómeno? Si la respuesta es sí, no lo elimines sin pensar.

- “Calcular es fácil. Decidir qué hacer con el resultado es la verdadera minería.”

- 🔜 Próxima clase: Análisis exploratorio visual. Aplicaremos estos datos ya limpios para detectar patrones e hipótesis iniciales.

- Un banco analiza solicitudes de crédito: encuentra 5% de ingresos faltantes.

- Si los faltantes son de clientes con ingresos altos, eliminarlos sesga el modelo.

- Deciden imputar con mediana por segmento laboral, no con media global.

- Resultado: el modelo final aprueba créditos con 12% menos de riesgo real.


---

# Clase 7 — Calidad y validación de datos

Fuente: Clase 7 — Calidad y validación de datos

## Titulos detectados
- 1. Capítulo 1 — Objetivo y contexto
- 🎯 Objetivo
- 🚀 Comencemos
- 📚 Al final de esta clase vas a poder:

## Texto importante

- En esta clase trabajaremos la calidad y validación de datos a partir de una situación similar a la que podría enfrentar un científico de datos en un proyecto real. El objetivo será analizar un conjunto de datos, detectar posibles problemas y reflexionar sobre cómo distintas decisiones pueden afectar la calidad de la información utilizada en etapas posteriores.

- En la práctica profesional es común recibir datos que presentan errores, inconsistencias o información incompleta. Aunque existen numerosas técnicas para tratar estas situaciones, elegir una solución adecuada requiere comprender el contexto del problema y evaluar el impacto que cada decisión tendrá sobre el análisis.

- Con frecuencia, los errores no aparecen porque una técnica sea desconocida, sino porque se aplica sin suficiente evidencia o sin considerar las características de los datos. Por este motivo, una misma situación puede admitir distintas alternativas de tratamiento, cada una con ventajas y limitaciones.

- Para explorar este desafío trabajaremos con un dataset de gastos médicos que contiene diversos problemas de calidad. A partir de su análisis deberán identificar situaciones que requieran atención, justificar sus decisiones y evaluar críticamente las acciones realizadas antes de comparar sus resultados con una propuesta de resolución.

- Identificar problemas de calidad presentes en un conjunto de datos.

- Analizar evidencia antes de decidir una estrategia de corrección.

- Justificar decisiones de limpieza utilizando criterios fundamentados.

- Evaluar el impacto de las correcciones sobre los datos.

- Reflexionar sobre distintas alternativas de tratamiento para un mismo problema.


---

# Clase 7 — Calidad y validación de datos

Fuente: 2. Capítulo 2 — Calidad y Validación de Datos

## Titulos detectados
- 2. Capítulo 2 — Calidad y Validación de Datos

## Texto importante

- La calidad de los datos es uno de los factores más importantes en cualquier proyecto de Ciencia de Datos. Un modelo puede estar correctamente implementado, pero si los datos contienen errores, inconsistencias o información faltante mal tratada, las conclusiones obtenidas pueden ser incorrectas.

- Validar datos implica mucho más que detectar problemas. También requiere comprender el origen de esos problemas, evaluar su impacto y seleccionar estrategias de tratamiento apropiadas para cada situación. Dos errores similares pueden requerir decisiones diferentes según el contexto del negocio y las características de los datos.

- En esta actividad trabajarán con un dataset que contiene información de asegurados y gastos médicos. El conjunto de datos fue modificado deliberadamente para incorporar distintos problemas de calidad que suelen encontrarse en entornos reales.

- Su tarea será asumir el rol de un científico de datos encargado de revisar el dataset antes de que sea utilizado para análisis o modelado.

- Explorar el dataset e identificar posibles problemas de calidad.

- Describir la evidencia utilizada para detectar cada problema.

- Justificar por qué cada situación identificada requiere atención.

- Proponer y aplicar estrategias de corrección utilizando Python.

- Explicar el motivo de cada decisión tomada.

- Evaluar el estado final del dataset luego de las correcciones realizadas.

- Durante el análisis considere aspectos como:

- Errores de codificación en variables categóricas.

- Valores imposibles o fuera de rango.

- Consistencia general de la información.

- El objetivo principal no es aplicar técnicas de limpieza de manera automática, sino justificar cada decisión utilizando evidencia obtenida del análisis de los datos. En proyectos reales, comprender la naturaleza del problema suele ser más importante que conocer una determinada función o algoritmo.

- Una vez finalizada la actividad, podrá consultar el notebook de resolución propuesto para comparar enfoques, analizar decisiones y discutir posibles alternativas de tratamiento.


---

# Clase 7 — Calidad y validación de datos

Fuente: 3. Capítulo 6 — Resumen

## Titulos detectados
- 3. Capítulo 6 — Resumen
- ✅ Lo que vimos hoy
- 🔍 Dato aplicado

## Texto importante

- En esta clase trabajamos sobre un aspecto fundamental del análisis de datos: preparar la información antes de extraer conclusiones. que aplicar técnicas aisladas, el objetivo fue comprender cómo distintas decisiones pueden influir en la calidad de los datos y en la confiabilidad de los resultados obtenidos.

- Permiten evaluar la completitud y confiabilidad de la información.

- No todos los faltantes tienen el mismo origen.

- La imputación requiere analizar el contexto.

- Eliminar datos también tiene consecuencias.

- Sirven para detectar observaciones poco frecuentes o inesperadas.

- Un valor extremo no siempre es un error.

- El contexto ayuda a interpretar anomalías.

- Eliminar sin analizar puede distorsionar resultados.

- Facilita el análisis y mejora la interpretación de los datos.

- Permite adaptar datos a distintos objetivos.

- Debe conservar el significado original.

- La interpretación sigue siendo prioritaria.

- Integra las decisiones necesarias antes del análisis.

- La calidad impacta en todas las etapas.

- Las decisiones deben ser justificadas.

- La documentación del proceso es esencial.

- Antes de corregir un problema, intente comprender su origen. Una técnica adecuada para una situación puede ser incorrecta para otra. La mejor decisión no siempre es la más rápida, sino la que conserva información relevante y minimiza la introducción de sesgos.

- Preparar datos correctamente requiere interpretar antes de transformar.

- Una empresa podría recibir información proveniente de múltiples sistemas de registro. Aunque cada fuente funcione correctamente por separado, diferencias en formatos, valores faltantes o registros inconsistentes pueden generar problemas durante el análisis. Por este motivo, gran parte del trabajo en Ciencia de Datos consiste en validar y preparar la información antes de utilizarla para responder preguntas de negocio o apoyar la toma de decisiones.


---

# MD1 - Clase 7 - Notebook de resolución

Fuente: MD1 - Clase 7 - Notebook de resolución

## Titulos detectados
- Sin titulos detectados

## Texto importante
- Requisitos de finalización Haga clic en MD1 - Clase 7 - Notebook de resolución para abrir el recurso.


---

# Clase 8 — Normalización y escalamiento

Fuente: Clase 8 — Normalización y escalamiento

## Titulos detectados
- 1. Capítulo 1 — Objetivo y contexto
- 🎯 Objetivo
- 🚀 Comencemos
- 📚 Al final de esta clase vas a poder:

## Texto importante
- Al finalizar esta clase, vas a poder reconocer cuándo las unidades de medida y las escalas de tus variables están distorsionando los resultados de un análisis. No solo vas a saber aplicar una transformación: vas a entender por qué es necesaria, qué problema concreto resuelve y qué le pasa a tu modelo si la omitís.

- Ya sabés calcular medidas estadísticas, construir gráficos y entender distribuciones. Ese conocimiento es el punto de partida. Pero en el análisis real de datos, calcular bien no es suficiente: el verdadero desafío está en leer lo que esos números te están diciendo sobre el fenómeno que estás estudiando.

- Imaginá que tenés dos variables: una medida en centímetros y otra en kilogramos. A simple vista parecen comparables, pero cuando un algoritmo las procesa juntas, la que tiene valores más grandes domina el resultado sin ninguna razón válida. Ese error silencioso no genera un mensaje de advertencia, pero sí distorsiona completamente tus conclusiones.

- En esta clase vamos a trabajar con el dataset Iris, un clásico del análisis de datos con mediciones reales de flores. Con él vas a ver, en datos concretos, cómo las decisiones previas al modelado determinan la calidad de todo lo que viene después. Calcular no es interpretar, y hoy el foco está puesto exactamente en esa diferencia.

- Identificar qué variables de un dataset necesitan ser escaladas y por qué.

- Interpretar qué significa cada tipo de escalamiento en términos del comportamiento de los datos.

- Comparar resultados antes y después de escalar para justificar la transformación aplicada.

- Detectar cuándo la escala original está afectando medidas de distancia o coeficientes del modelo.

- Tomar decisiones fundamentadas sobre qué técnica de escalamiento usar según el contexto del análisis.


---

# Clase 8 — Normalización y escalamiento

Fuente: 2. Capítulo 2 — Importancia del Escalamiento de Variables

## Titulos detectados
- 2. Capítulo 2 — Importancia del Escalamiento de Variables

## Texto importante
- Importancia del escalamiento de variables

- Escalar una variable es transformar sus valores numéricos para que sean comparables con los de otras variables. Cuando las variables tienen unidades o rangos muy distintos, los algoritmos que calculan distancias o ajustan parámetros pueden verse dominados artificialmente por la variable de mayor magnitud. La transformación más usada es la estandarización (Z-score):

- donde μ es la media y σ la desviación estándar de la variable. Después de aplicarla, todas las variables quedan centradas en 0 y con varianza 1, sin importar sus unidades originales. La normalización Min-Max es la alternativa cuando se necesita un rango [0, 1]:

- Ambas técnicas involucran variables numéricas continuas o discretas y responden a la pregunta: ¿mis variables contribuyen de forma equitativa al modelo, o alguna domina por su magnitud?

- Usamos el dataset Iris, donde cada flor tiene cuatro medidas: longitud y ancho del sépalo, longitud y ancho del pétalo. Calculamos la varianza de cada variable antes y después de aplicar estandarización Z-score, y luego comparamos distancias euclidianas entre las primeras cinco flores.

- import pandas as pd import numpy as np from sklearn.datasets import load_iris from sklearn.preprocessing import StandardScaler from sklearn.metrics import pairwise_distances # Cargar datos iris = load_iris() X = pd.DataFrame(iris.data, columns=iris.feature_names) # Calcular varianza antes del escalamiento print("Varianza original:") print(X.var().round(4)) # Aplicar estandarización scaler = StandardScaler() X_scaled = scaler.fit_transform(X) # Calcular varianza después X_scaled_df = pd.DataFrame(X_scaled, columns=iris.feature_names) print("Varianza después de estandarizar:") print(X_scaled_df.var().round(4)) # Comparar distancias entre primeras 5 flores obs = slice(0, 5) d_original = pairwise_distances(X.values[obs]) d_scaled = pairwise_distances(X_scaled[obs]) print("Distancias ANTES (primeras 5 flores):") print(pd.DataFrame(d_original).round(3)) print("Distancias DESPUÉS (primeras 5 flores):") print(pd.DataFrame(d_scaled).round(3))

- import pandas as pd import numpy as np from sklearn.datasets import load_iris from sklearn.preprocessing import StandardScaler from sklearn.metrics import pairwise_distances # Cargar datos iris = load_iris() X = pd.DataFrame(iris.data, columns=iris.feature_names) # Calcular varianza antes del escalamiento print("Varianza original:") print(X.var().round(4)) # Aplicar estandarización scaler = StandardScaler() X_scaled = scaler.fit_transform(X) # Calcular varianza después X_scaled_df = pd.DataFrame(X_scaled, columns=iris.feature_names) print("Varianza después de estandarizar:") print(X_scaled_df.var().round(4)) # Comparar distancias entre primeras 5 flores obs = slice(0, 5) d_original = pairwise_distances(X.values[obs]) d_scaled = pairwise_distances(X_scaled[obs]) print("Distancias ANTES (primeras 5 flores):") print(pd.DataFrame(d_original).round(3)) print("Distancias DESPUÉS (primeras 5 flores):") print(pd.DataFrame(d_scaled).round(3))

- petal length: 3.1163 → 1.0000 (la más dominante sin escalar)

- Resultado: distancia desde Flor 0 hacia las demás (primeras 5 flores)

- Antes de escalar: 0.000 | 0.539 | 0.510 | 0.648 | 0.141

- Después de escalar: 0.000 | 1.012 | 0.993 | 1.278 | 0.288

- ¿Qué significa este resultado?En los datos originales, petal length tiene varianza 3.12 y sepal width apenas 0.19. Al calcular distancias sin escalar, la longitud del pétalo pesa aproximadamente 16 veces más que el ancho del sépalo, no por relevancia biológica, sino por magnitud numérica. Después de estandarizar, todas las variables tienen varianza 1 y contribuyen por igual.

- ¿Qué decisión permite tomar?Antes de aplicar K-Means, KNN o PCA sobre este dataset, escalar con StandardScaler es obligatorio. Si se omite ese paso, los clusters o vecinos más cercanos estarán determinados casi exclusivamente por la longitud del pétalo. El modelo aprenderá una estructura que refleja las unidades de medida, no los datos.

- Error común de interpretaciónSuponer que, como todas las variables están en centímetros, ya son comparables. La misma unidad no garantiza misma escala: lo que importa es la varianza. Una variable que varía poco (sepal width) y otra que varía mucho (petal length) siguen siendo incomparables aunque ambas estén en cm.

- Cuándo usarlo: siempre que el algoritmo use distancias (KNN, K-Means, SVM, PCA) o gradiente descendente (redes neuronales, regresión regularizada).

- Cuándo no usarlo: en árboles de decisión y Random Forest, que dividen por umbrales independientes de la escala.

- Limitaciones: la estandarización es sensible a outliers, ya que estos modifican la media y la desviación estándar. En esos casos usar RobustScaler.

- Buenas prácticas: ajustar el scaler solo con datos de entrenamiento (fit_transform) y aplicarlo al conjunto de prueba con transform. Aplicar fit_transform al conjunto de prueba introduce información que el modelo no debería conocer.

- Si usaras un dataset de viviendas con variables como superficie (m²), antigüedad (años) y número de habitaciones, ¿qué variable dominaría las distancias sin escalar? ¿Cómo cambiaría eso los resultados de un K-Means?

- Si escalás con Min-Max y luego aparece un nuevo dato con un valor mayor al máximo original, ¿qué problema genera? ¿Cómo lo resolverías?


---

# Clase 8 — Normalización y escalamiento

Fuente: 3. Capítulo 3 — Caso de aplicación 1

## Titulos detectados
- 3. Capítulo 3 — Caso de aplicación 1

## Texto importante
- Caso de aplicación: selección de personal en Recursos Humanos

- Un área de Recursos Humanos recopila datos de postulantes para un puesto técnico. Por cada persona registra: años de experiencia (0–20), puntaje en evaluación técnica (0–100) y cantidad de proyectos anteriores (0–15). El objetivo es calcular qué tan similares son los perfiles entre sí para agruparlos o encontrar candidatos parecidos a uno de referencia.

- El problema concreto: estas tres variables tienen rangos muy distintos. Antes de comparar perfiles, es necesario analizar si esa diferencia de magnitud distorsiona las métricas.

- import pandas as pd import numpy as np from sklearn.preprocessing import StandardScaler from sklearn.metrics import pairwise_distances # Dataset simulado: 6 postulantes data = { 'experiencia_anios': [1, 5, 10, 3, 8, 2], 'puntaje_tecnico': [45, 78, 92, 60, 85, 50], 'proyectos_prev': [1, 4, 10, 3, 7, 2] } df = pd.DataFrame(data) nombres = ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Fabio'] df.index = nombres print("=== Varianza por variable (sin escalar) ===") print(df.var().round(2)) scaler = StandardScaler() df_scaled = pd.DataFrame( scaler.fit_transform(df), columns=df.columns, index=df.index ) print("=== Varianza por variable (estandarizado) ===") print(df_scaled.var().round(2)) d_orig = pairwise_distances(df.values) d_scaled = pairwise_distances(df_scaled.values) print("=== Distancia euclidiana desde Ana (sin escalar) ===") for i, n in enumerate(nombres[1:], 1): print(f" Ana a {n}: {d_orig[0][i]:.2f}") print("=== Distancia euclidiana desde Ana (estandarizado) ===") for i, n in enumerate(nombres[1:], 1): print(f" Ana a {n}: {d_scaled[0][i]:.2f}")

- import pandas as pd import numpy as np from sklearn.preprocessing import StandardScaler from sklearn.metrics import pairwise_distances # Dataset simulado: 6 postulantes data = { 'experiencia_anios': [1, 5, 10, 3, 8, 2], 'puntaje_tecnico': [45, 78, 92, 60, 85, 50], 'proyectos_prev': [1, 4, 10, 3, 7, 2] } df = pd.DataFrame(data) nombres = ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Fabio'] df.index = nombres print("=== Varianza por variable (sin escalar) ===") print(df.var().round(2)) scaler = StandardScaler() df_scaled = pd.DataFrame( scaler.fit_transform(df), columns=df.columns, index=df.index ) print("=== Varianza por variable (estandarizado) ===") print(df_scaled.var().round(2)) d_orig = pairwise_distances(df.values) d_scaled = pairwise_distances(df_scaled.values) print("=== Distancia euclidiana desde Ana (sin escalar) ===") for i, n in enumerate(nombres[1:], 1): print(f" Ana a {n}: {d_orig[0][i]:.2f}") print("=== Distancia euclidiana desde Ana (estandarizado) ===") for i, n in enumerate(nombres[1:], 1): print(f" Ana a {n}: {d_scaled[0][i]:.2f}")

- puntaje_tecnico: 338.67 → 1.00 (la más dominante sin escalar)

- Resultado: distancia euclidiana desde Ana hacia cada postulante

- Ana → Bruno: 34.15 (sin escalar) | 1.83 (estandarizado)

- Ana → Carla: 49.36 (sin escalar) | 2.71 (estandarizado)

- Ana → Diego: 15.43 (sin escalar) | 0.89 (estandarizado)

- Ana → Elena: 41.48 (sin escalar) | 2.37 (estandarizado)

- Ana → Fabio: 5.10 (sin escalar) | 0.25 (estandarizado)

- ¿Qué significa este resultado?La variable puntaje_tecnico tiene una varianza de 338.67, frente a 10.97 de las otras dos. Sin escalar, el 96% del valor de cualquier distancia entre postulantes está determinado por la diferencia en puntaje técnico. La experiencia y los proyectos previos son prácticamente ignorados. Dos postulantes con puntajes similares parecerán idénticos aunque tengan perfiles de experiencia muy distintos.

- ¿Qué decisión permite tomar?Escalar antes de comparar perfiles es necesario para que las tres dimensiones contribuyan por igual. Sin escalar, el sistema de búsqueda de candidatos similares funcionaría como si solo existiera una variable: el puntaje técnico. Un candidato con mucha experiencia pero puntaje medio podría quedar descartado frente a uno sin experiencia pero con puntaje alto, simplemente por efecto de la escala.

- Error común de interpretaciónConcluir que puntaje_tecnico es la variable más importante porque tiene la varianza más alta. Alta varianza no implica mayor relevancia: implica mayor magnitud numérica. La decisión de qué variable importa más es del negocio, no de la escala.

- Cuándo usarlo: siempre que se combinen variables de RR.HH. con unidades heterogéneas (años, puntajes, conteos) en análisis de distancia o clustering.

- Cuándo no usarlo: si el análisis es puramente descriptivo (ranking por puntaje), escalar puede dificultar la lectura directa de los valores.

- Limitaciones: el escalamiento no resuelve el problema de variables irrelevantes. Si proyectos_prev no tiene valor predictivo, escalarla no la vuelve útil; solo la equilibra en magnitud.

- Buenas prácticas: documentar siempre los parámetros del scaler (media y desviación estándar), ya que serán necesarios para transformar nuevos candidatos antes de compararlos con el conjunto existente.

- ¿Si agregaras una variable de salario pretendido en pesos (rango 300.000–900.000), qué pasaría con las distancias sin escalar? ¿Qué variable dominaría ahora?

- ¿Tiene sentido escalar una variable binaria como tiene_certificación (0 o 1)? ¿Qué efecto tendría sobre la distancia euclidiana?


---

# Clase 8 — Normalización y escalamiento

Fuente: 4. Capítulo 4 — Caso de aplicación 2

## Titulos detectados
- 4. Capítulo 4 — Caso de aplicación 2

## Texto importante
- Caso de aplicación: análisis de rendimiento de jugadores de fútbol

- Un cuerpo técnico registra métricas de rendimiento de 6 jugadores: distancia recorrida por partido (en metros, rango 7.000–12.000), pases completados por partido (20–80) y goles + asistencias por partido (0–2). El objetivo es comparar perfiles para detectar similitudes de rol o estilo de juego.

- El problema: las tres métricas tienen unidades completamente distintas y rangos que difieren en dos órdenes de magnitud. Sin escalar, la distancia recorrida absorberá casi todo el peso de cualquier comparación numérica.

- import pandas as pd import numpy as np from sklearn.preprocessing import StandardScaler from sklearn.metrics import pairwise_distances data = { 'distancia_m': [9500, 11200, 8000, 10800, 7500, 11000], 'pases_completados': [65, 45, 30, 55, 25, 72], 'goles_asistencias': [0.8, 1.2, 0.3, 1.5, 0.2, 0.9] } jugadores = ['Romero', 'Silva', 'Torres', 'Medina', 'Vargas', 'Ortiz'] df = pd.DataFrame(data, index=jugadores) # Varianza original y contribucion relativa var_orig = df.var() prop = (var_orig / var_orig.sum() * 100).round(1) print("=== Varianza original ===") print(var_orig.round(2)) print("\n=== Contribucion relativa a la distancia (%) ===") print(prop.to_string()) # Estandarizar scaler = StandardScaler() df_scaled = pd.DataFrame( scaler.fit_transform(df), columns=df.columns, index=df.index ) print("\n=== Varianza estandarizada ===") print(df_scaled.var().round(2)) # Distancias desde Romero d_orig = pairwise_distances(df.values) d_scaled = pairwise_distances(df_scaled.values) print("\n=== Distancia desde Romero (sin escalar) ===") for i, n in enumerate(jugadores[1:], 1): print(f" Romero a {n}: {d_orig[0][i]:.1f}") print("\n=== Distancia desde Romero (estandarizado) ===") for i, n in enumerate(jugadores[1:], 1): print(f" Romero a {n}: {d_scaled[0][i]:.3f}")

- import pandas as pd import numpy as np from sklearn.preprocessing import StandardScaler from sklearn.metrics import pairwise_distances data = { 'distancia_m': [9500, 11200, 8000, 10800, 7500, 11000], 'pases_completados': [65, 45, 30, 55, 25, 72], 'goles_asistencias': [0.8, 1.2, 0.3, 1.5, 0.2, 0.9] } jugadores = ['Romero', 'Silva', 'Torres', 'Medina', 'Vargas', 'Ortiz'] df = pd.DataFrame(data, index=jugadores) # Varianza original y contribucion relativa var_orig = df.var() prop = (var_orig / var_orig.sum() * 100).round(1) print("=== Varianza original ===") print(var_orig.round(2)) print("\n=== Contribucion relativa a la distancia (%) ===") print(prop.to_string()) # Estandarizar scaler = StandardScaler() df_scaled = pd.DataFrame( scaler.fit_transform(df), columns=df.columns, index=df.index ) print("\n=== Varianza estandarizada ===") print(df_scaled.var().round(2)) # Distancias desde Romero d_orig = pairwise_distances(df.values) d_scaled = pairwise_distances(df_scaled.values) print("\n=== Distancia desde Romero (sin escalar) ===") for i, n in enumerate(jugadores[1:], 1): print(f" Romero a {n}: {d_orig[0][i]:.1f}") print("\n=== Distancia desde Romero (estandarizado) ===") for i, n in enumerate(jugadores[1:], 1): print(f" Romero a {n}: {d_scaled[0][i]:.3f}")

- Resultado: varianza y contribución relativa (sin escalar)

- distancia_m: varianza 2.290.000 — contribución 99.7%

- pases_completados: varianza 3.436 — contribución 0.3%

- goles_asistencias: varianza 0.27 — contribución ~0.0%

- Después de estandarizar: todas con varianza 1.00

- Resultado: distancia desde Romero hacia cada jugador

- Romero → Silva: 1700.0 (sin escalar) | 1.648 (estandarizado)

- Romero → Torres: 1500.0 (sin escalar) | 1.834 (estandarizado)

- Romero → Medina: 1300.0 (sin escalar) | 1.095 (estandarizado)

- Romero → Vargas: 2000.1 (sin escalar) | 2.278 (estandarizado)

- Romero → Ortiz: 1500.1 (sin escalar) | 0.791 (estandarizado) ← perfil más similar después de escalar

- ¿Qué significa este resultado?Sin escalar, la variable distancia_m explica el 99.7% de toda la variación en las distancias calculadas. Pases completados y goles/asistencias aportan menos del 0.3% combinados. Comparar a Romero con Torres (1.500 m) y con Ortiz (1.500 m) arroja el mismo resultado numérico aunque sus perfiles técnicos sean completamente distintos. El análisis sin escalar no compara jugadores: compara cuántos metros corren.

- ¿Qué decisión permite tomar?Al estandarizar, el orden de similitud cambia: Ortiz (0.791) resulta el perfil más parecido a Romero, no Torres ni Medina. Esa diferencia es relevante para decisiones de reemplazos tácticos o agrupamiento de roles. Sin escalar, esas decisiones estarían basadas en un único factor físico, ignorando la capacidad técnica y la participación en gol.

- Error común de interpretaciónPensar que la variable con mayor varianza es la más informativa. En este caso, distancia_m tiene varianza de 2.290.000 simplemente porque está expresada en metros. Si se expresara en kilómetros, su varianza sería 2.29 y dejaría de dominar. La varianza depende de las unidades, no del contenido informativo de la variable.

- Cuándo usarlo: siempre que se combinen métricas deportivas de distinta naturaleza (físicas, técnicas, tácticas) para comparar perfiles o agrupar jugadores.

- Cuándo no usarlo: si el análisis busca comparar exclusivamente una dimensión física (ej. ranking de resistencia), escalar mezclaría dimensiones que deben mantenerse separadas.

- Limitaciones: la estandarización asume que todas las variables tienen el mismo peso conceptual. Si el cuerpo técnico considera que la distancia recorrida vale más, eso debe modelarse con ponderación explícita, no dejarlo al azar de las unidades.

- Buenas prácticas: antes de escalar, calcular la contribución relativa de cada variable (porcentaje de varianza). Si una variable aporta más del 90% de la variación total, hay un problema de escala que necesita corrección.

- ¿Si expresaras la distancia recorrida en kilómetros en lugar de metros, cambiaría el resultado del análisis sin escalar? ¿Y con estandarización? ¿Qué nos dice eso sobre la robustez del escalamiento?

- Suponé que querés darle el doble de peso a goles_asistencias porque es la más relevante tácticamente. ¿Cómo podrías hacerlo después de escalar?


---

# Clase 8 — Normalización y escalamiento

Fuente: 5. Capítulo 5 — Resumen

## Titulos detectados
- 5. Capítulo 5 — Resumen
- ✅ Lo que vimos hoy
- Magnitud relativa y distancia
- Coeficientes y unidades originales
- Rango vs. varianza
- Convergencia numérica
- 🔍 Dato aplicado

## Texto importante
- Trabajamos con el dataset Iris para entender cómo las escalas originales de las variables pueden engañarnos. Vimos que escalar no es un paso opcional: es una decisión que afecta directamente la calidad de cualquier análisis posterior.

- Una variable con valores grandes domina las medidas de distancia aunque no sea más relevante.

- La distancia no mide importancia, mide magnitud numérica.

- Variables en cm y kg no son comparables sin escalar.

- El algoritmo no distingue unidades; vos sí debés hacerlo.

- Un coeficiente grande no implica mayor influencia: depende de la escala de la variable.

- Comparar coeficientes sin escalar lleva a conclusiones falsas.

- El escalamiento hace los coeficientes comparables entre variables.

- Interpretar magnitud requiere haber normalizado primero.

- Rango amplio no equivale a alta variabilidad ni a mayor información.

- Min-Max comprime el rango, no redistribuye la varianza.

- Z-score informa sobre posición relativa dentro de la distribución.

- Elegir mal la técnica distorsiona lo que querés medir.

- Variables sin escalar pueden impedir que un algoritmo iterativo llegue a una solución estable.

- El modelo "tarda más" o diverge por diferencias de escala, no de datos.

- Escalar reduce el espacio de búsqueda del algoritmo.

- Un modelo que no converge no es malo: puede estar mal alimentado.

- Regla práctica: Usá Z-score cuando te importa la posición relativa y hay valores extremos. Usá Min-Max cuando necesitás un rango fijo y los datos están acotados. Si no sabés cuál elegir, preguntate primero qué querés preservar: la distribución o el rango.

- Entender por qué escalás vale más que saber cómo hacerlo.

- Una empresa de salud podría usar sensores para registrar variables como frecuencia cardíaca (bpm), temperatura corporal (°C) y glucosa en sangre (mg/dL). Sin escalar, la glucosa —con valores típicos diez veces mayores— dominaría cualquier modelo de riesgo. El escalamiento permite que cada variable contribuya según su variabilidad clínica real, no según su unidad de medida.

- La escala numérica no refleja importancia médica.

- Un modelo sin escalar tomaría decisiones sesgadas por las unidades.

- El profesional de datos debe justificar la transformación, no solo aplicarla.


---

# Clase 9 - Visualizaciones avanzadas - Teoria

Fuente: Clase 9 - Visualizaciones avanzadas - Teoria

## Titulos detectados
- 1. Capítulo 1 — Objetivo y contexto
- 🎯 Objetivo
- 🚀 Comencemos
- 📚 Al final de esta clase vas a poder:

## Texto importante

- En esta clase vas a aprender a construir y publicar una aplicación web interactiva con tus propios análisis de datos, sin necesidad de saber desarrollo web. Vas a poder presentar gráficos exploratorios de forma que cualquier persona pueda interactuar con ellos, tomar decisiones a partir de lo que muestran y compartir tus resultados con una URL.

- Hasta ahora trabajaste con Python en notebooks: corrés el código, ves el resultado y seguís. Ese flujo está muy bien para explorar datos, pero tiene un límite claro: los resultados quedan encerrados en tu entorno. Nadie más puede verlos, filtrarlos ni interactuar con ellos sin ejecutar código. En la práctica real del análisis de datos, eso es un problema cotidiano.

- Calcular un promedio o graficar una distribución es solo la mitad del trabajo. La otra mitad es lograr que ese resultado llegue a quien tiene que tomar una decisión, en un formato que pueda explorar sin pedirte una nueva consulta cada vez. Un número sin contexto no comunica nada. Un gráfico que nadie puede ver tampoco. Esta clase está centrada en ese segundo paso: pasar del análisis al resultado comunicable.

- Vamos a trabajar con datos reales de desarrollo mundial: expectativa de vida, riqueza y población de países a lo largo de décadas. No son datos inventados para un ejercicio: son datos que generan preguntas reales. ¿Qué continente mejoró más? ¿En qué período se amplió la brecha? Esas preguntas no se responden mirando una tabla. Se responden con herramientas que permiten explorar.

- Explicar qué problema resuelve Streamlit y cuándo tiene sentido usarlo.

- Construir una app web con título, controles interactivos y gráficos en pocas líneas de Python.

- Interpretar lo que muestra un gráfico interactivo en términos de decisiones concretas.

- Publicar tu app en internet con una URL propia usando Streamlit Community Cloud.

- Identificar los errores más comunes al presentar resultados de análisis a usuarios no técnicos.


---

# Clase 9 - Visualizaciones avanzadas - Teoria

Fuente: 2. Capítulo 2 — Visualizaciones Avanzadas con Streamlit

## Titulos detectados
- 2. Capítulo 2 — Visualizaciones Avanzadas con Streamlit

## Texto importante

- Visualizaciones Avanzadas con Streamlit

- Streamlit es un framework de Python de código abierto que permite convertir un script de análisis en una aplicación web interactiva sin necesidad de saber HTML, CSS ni JavaScript. Resuelve un problema concreto y frecuente en ciencia de datos: la brecha entre el análisis técnico realizado en Python y la comunicación de esos resultados a personas que no programan. El analista escribe código Python como siempre, agrega algunas funciones de Streamlit, ejecuta el archivo desde la terminal y obtiene una página web funcional donde cualquier usuario puede explorar los datos mediante menús, sliders y botones. No es una herramienta de análisis estadístico: es una capa de presentación e interacción que se coloca sobre el análisis ya realizado.

- El escenario más habitual es este: un analista termina su trabajo —limpió datos, construyó gráficos, calculó métricas— y ahora necesita que otras personas puedan explorar esos resultados por su cuenta. Sin Streamlit, las opciones son exportar imágenes estáticas, enviar un PDF o pedir al cliente que instale Python y ejecute un notebook. Con Streamlit, el mismo script se convierte en una herramienta de autoservicio. Un responsable de área puede filtrar por fecha, una región o una categoría y ver los gráficos actualizarse en tiempo real, sin intermediarios y sin tocar código.

- Análisis de ventas: en lugar de enviar capturas estáticas, el equipo comercial filtra por período o región desde el navegador.

- Monitoreo de producción: el técnico ajusta parámetros con un slider y observa cómo cambian los indicadores de calidad.

- Demostración de modelos: cualquier área puede ingresar valores y obtener una predicción del modelo sin ver una línea de código.

- Exploración de datasets nuevos: el analista mismo usa la app para navegar los datos más rápido que modificando el script.

- El mecanismo central que hace posible todo esto es el modelo de re-ejecución: cada vez que el usuario interactúa con un widget (elige una opción, mueve un slider, escribe un valor), Streamlit vuelve a ejecutar el script completo de arriba hacia abajo y actualiza lo que se muestra en pantalla. Esto significa que no hay que programar eventos ni gestionar estados: el comportamiento interactivo surge naturalmente del flujo del script.

- En cuanto a alcances y limitaciones, Streamlit es ideal para prototipos rápidos, dashboards internos y demostraciones. No está pensado para aplicaciones con miles de usuarios simultáneos, no reemplaza sistemas de bases de datos robustos, y el modelo de re-ejecución total puede volverse lento con datasets muy grandes si no se aplica caché correctamente.

- El siguiente script construye una aplicación mínima pero funcional. El usuario elige una especie de pingüino desde un menú desplegable y la app muestra automáticamente el histograma del largo del pico y el promedio correspondiente. Cada vez que cambia la selección, todo se recalcula y se redibuja sin recargar la página.

- Para ejecutar la app, primero instalar Streamlit desde la terminal:

- Luego crear el archivo app.py con el siguiente contenido y ejecutarlo con streamlit run app.py:

- import streamlit as st import pandas as pd import matplotlib.pyplot as plt # Título e introducción visibles en la app st.title("Explorador de Pingüinos") st.write("Distribución del largo del pico según la especie seleccionada.") # Carga del dataset desde la web url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv" df = pd.read_csv(url) df = df.dropna() # Widget: menú desplegable — la elección del usuario queda en 'especie' especie = st.selectbox("Seleccioná una especie:", df["species"].unique()) # Filtrado reactivo: se recalcula cada vez que cambia la selección datos_filtrados = df[df["species"] == especie] # Gráfico que refleja los datos filtrados fig, ax = plt.subplots() ax.hist(datos_filtrados["bill_length_mm"], bins=15, color="steelblue", edgecolor="white") ax.set_xlabel("Largo del pico (mm)") ax.set_ylabel("Frecuencia") ax.set_title(f"Distribución del pico — {especie}") st.pyplot(fig) # Métrica resumen con formato destacado st.metric("Promedio del pico (mm)", round(datos_filtrados["bill_length_mm"].mean(), 2))

- import streamlit as st import pandas as pd import matplotlib.pyplot as plt # Título e introducción visibles en la app st.title("Explorador de Pingüinos") st.write("Distribución del largo del pico según la especie seleccionada.") # Carga del dataset desde la web url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv" df = pd.read_csv(url) df = df.dropna() # Widget: menú desplegable — la elección del usuario queda en 'especie' especie = st.selectbox("Seleccioná una especie:", df["species"].unique()) # Filtrado reactivo: se recalcula cada vez que cambia la selección datos_filtrados = df[df["species"] == especie] # Gráfico que refleja los datos filtrados fig, ax = plt.subplots() ax.hist(datos_filtrados["bill_length_mm"], bins=15, color="steelblue", edgecolor="white") ax.set_xlabel("Largo del pico (mm)") ax.set_ylabel("Frecuencia") ax.set_title(f"Distribución del pico — {especie}") st.pyplot(fig) # Métrica resumen con formato destacado st.metric("Promedio del pico (mm)", round(datos_filtrados["bill_length_mm"].mean(), 2))

- Resultado aproximado según la especie seleccionada (valores redondeados del dataset):

- Especie seleccionada Promedio pico (mm) Rango aprox. (mm) ───────────────────────────────────────────────────────────── Adelie 38.79 32 – 46 Chinstrap 48.83 41 – 58 Gentoo 47.50 40 – 60

- Especie seleccionada Promedio pico (mm) Rango aprox. (mm) ───────────────────────────────────────────────────────────── Adelie 38.79 32 – 46 Chinstrap 48.83 41 – 58 Gentoo 47.50 40 – 60

- ¿Qué significa este resultado?Cuando el usuario selecciona Adelie, el histograma muestra una distribución concentrada entre 32 y 46 mm, con la mayoría de los individuos agrupados alrededor de los 38 mm. Al cambiar a Gentoo o Chinstrap, la distribución se desplaza hacia valores más altos y el rango se amplía. Esto indica que las tres especies presentan longitudes de pico claramente diferenciadas, y que esa diferencia es visible no solo en el promedio sino en la forma y posición del histograma completo. Lo relevante no es el número en sí, sino que la app permite comparar visualmente esas distribuciones en segundos, algo que en un script estático requeriría generar y guardar tres gráficos por separado.

- ¿Qué decisión permite tomar?Un investigador de campo podría usar esta app para establecer umbrales de clasificación preliminar: si la longitud del pico de un individuo medido está por debajo de 46 mm, es probable que corresponda a la especie Adelie. Si no se construye esta herramienta exploratoria y se trabaja solo con tablas de promedios, se pierde información sobre la dispersión y los solapamientos entre especies, lo que puede llevar a clasificaciones incorrectas.

- Error común de interpretaciónCreer que Streamlit analiza o transforma los datos. La app solo muestra lo que el código Python ya calculó: si el filtrado, el cálculo del promedio o la construcción del gráfico tienen errores lógicos, la app los presentará con formato atractivo pero los resultados seguirán siendo incorrectos. Streamlit no valida ni corrige el análisis; lo expone.

- Cuándo usarlo: cuando el análisis ya está validado y se necesita que otras personas puedan explorar los resultados sin ejecutar código; también como herramienta personal para explorar datasets de forma más ágil.

- Cuándo no usarlo: cuando se necesita una aplicación de producción con alto volumen de usuarios simultáneos, autenticación compleja o integraciones con sistemas empresariales; para eso existen frameworks más robustos como Flask o Django.

- Limitaciones: el modelo de re-ejecución total del script puede generar lentitud perceptible con datasets grandes; la personalización visual es limitada comparada con herramientas dedicadas de BI; no está diseñado para gestión de bases de datos.

- Buenas prácticas: usar @st.cache_data al cargar datasets para evitar que se descarguen o procesen de nuevo en cada interacción; organizar el script en secciones claras (carga → widgets → visualización → métricas); probar la app con usuarios reales antes de considerarla lista.

- Si esta misma app se le presenta a un biólogo que no sabe programar, ¿qué información adicional necesitaría ver para poder tomar una decisión de clasificación? ¿Cómo agregarías esa información al script?

- El script recalcula el promedio y regenera el gráfico cada vez que el usuario cambia la especie. ¿Qué problema podría surgir si en lugar de 333 registros el dataset tuviera 5 millones? ¿Cómo lo resolverías sin cambiar la lógica del análisis?


---

# Clase 9 - Visualizaciones avanzadas - Teoria

Fuente: 3. Capítulo 3 — Ejemplo práctico

## Titulos detectados
- 3. Capítulo 3 — Ejemplo práctico

## Texto importante

- Ejemplo práctico — Dashboard con Streamlit y Plotly

- En el capítulo anterior vimos qué es Streamlit y qué problema resuelve. Ahora vamos a construir una aplicación real: un dashboard de análisis con dos gráficos interactivos, un control deslizante (slider) y un bloque de título. El objetivo es que puedas ver cómo se conectan todos los elementos en un script concreto y ejecutable.

- Para los gráficos usaremos Plotly Express, una librería de visualización que genera gráficos interactivos en una sola línea de código. A diferencia de Matplotlib, los gráficos de Plotly permiten al usuario hacer zoom, pasar el cursor sobre los puntos para ver valores exactos y ocultar categorías con un clic, sin agregar ningún código extra. Streamlit los muestra directamente con st.plotly_chart().

- Ejecutar una sola vez desde la terminal antes de correr el script:

- El script completo — archivo dashboard.py

- El dataset que usamos es Gapminder, disponible dentro de Plotly. Contiene datos de expectativa de vida, PBI per cápita y población de países del mundo entre 1952 y 2007. Es un dataset real, conocido y libre de usar. El slider va a controlar el año que se analiza: cuando el usuario lo mueve, ambos gráficos se actualizan solos.

- import streamlit as st import plotly.express as px # ── BLOQUE DE TÍTULO ────────────────────────────────────────── # st.title() muestra el título principal de la app st.title("Dashboard de Desarrollo Mundial") # st.markdown() acepta texto con formato; lo usamos para el subtítulo st.markdown("Explorá la relación entre **riqueza**, **salud** y **población** por país.") # st.divider() dibuja una línea horizontal como separador visual st.divider() # ── CARGA DE DATOS ──────────────────────────────────────────── # Cargamos el dataset Gapminder directamente desde Plotly # Es un DataFrame con columnas: country, continent, year, # lifeExp (expectativa de vida), pop (población), gdpPercap (PBI per cápita) df = px.data.gapminder() # ── SLIDER ─────────────────────────────────────────────────── # st.slider() crea un control deslizante interactivo # Parámetros: etiqueta, valor mínimo, valor máximo, valor inicial, paso anio = st.slider("Seleccioná el año:", 1952, 2007, 2007, step=5) # Filtramos el dataset para quedarnos solo con el año elegido # Este filtrado se recalcula automáticamente cada vez que el slider cambia df_anio = df[df["year"] == anio] # ── MÉTRICA RÁPIDA ──────────────────────────────────────────── # st.metric() muestra un número destacado con etiqueta # Lo usamos para mostrar cuántos países hay en el año seleccionado st.metric("Países en el análisis", df_anio["country"].nunique()) st.divider() # ── GRÁFICO 1: dispersión ───────────────────────────────────── # px.scatter() genera un gráfico de dispersión interactivo en una línea # x: PBI per cápita (riqueza) y: expectativa de vida (salud) # size: tamaño del punto según población color: continente # hover_name: qué aparece al pasar el cursor sobre un punto fig1 = px.scatter( df_anio, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country", log_x=True, # escala logarítmica en X (el PBI tiene mucha variación) title=f"Riqueza vs. Expectativa de vida — {anio}", labels={"gdpPercap": "PBI per cápita (USD)", "lifeExp": "Expectativa de vida (años)"} ) # st.plotly_chart() renderiza el gráfico de Plotly en la app # use_container_width=True hace que ocupe todo el ancho disponible st.plotly_chart(fig1, use_container_width=True) # ── GRÁFICO 2: barras por continente ───────────────────────── # px.bar() genera un gráfico de barras interactivo en una línea # Agrupamos por continente y calculamos el promedio de expectativa de vida df_cont = df_anio.groupby("continent", as_index=False)["lifeExp"].mean().round(1) fig2 = px.bar( df_cont, x="continent", y="lifeExp", color="continent", title=f"Expectativa de vida promedio por continente — {anio}", labels={"lifeExp": "Expectativa de vida promedio (años)", "continent": "Continente"}, text="lifeExp" # muestra el valor encima de cada barra ) st.plotly_chart(fig2, use_container_width=True) # ── NOTA AL PIE ─────────────────────────────────────────────── # st.caption() muestra texto pequeño, ideal para fuentes o aclaraciones st.caption("Fuente: Gapminder Dataset — disponible en Plotly Express (px.data.gapminder())")

- import streamlit as st import plotly.express as px # ── BLOQUE DE TÍTULO ────────────────────────────────────────── # st.title() muestra el título principal de la app st.title("Dashboard de Desarrollo Mundial") # st.markdown() acepta texto con formato; lo usamos para el subtítulo st.markdown("Explorá la relación entre **riqueza**, **salud** y **población** por país.") # st.divider() dibuja una línea horizontal como separador visual st.divider() # ── CARGA DE DATOS ──────────────────────────────────────────── # Cargamos el dataset Gapminder directamente desde Plotly # Es un DataFrame con columnas: country, continent, year, # lifeExp (expectativa de vida), pop (población), gdpPercap (PBI per cápita) df = px.data.gapminder() # ── SLIDER ─────────────────────────────────────────────────── # st.slider() crea un control deslizante interactivo # Parámetros: etiqueta, valor mínimo, valor máximo, valor inicial, paso anio = st.slider("Seleccioná el año:", 1952, 2007, 2007, step=5) # Filtramos el dataset para quedarnos solo con el año elegido # Este filtrado se recalcula automáticamente cada vez que el slider cambia df_anio = df[df["year"] == anio] # ── MÉTRICA RÁPIDA ──────────────────────────────────────────── # st.metric() muestra un número destacado con etiqueta # Lo usamos para mostrar cuántos países hay en el año seleccionado st.metric("Países en el análisis", df_anio["country"].nunique()) st.divider() # ── GRÁFICO 1: dispersión ───────────────────────────────────── # px.scatter() genera un gráfico de dispersión interactivo en una línea # x: PBI per cápita (riqueza) y: expectativa de vida (salud) # size: tamaño del punto según población color: continente # hover_name: qué aparece al pasar el cursor sobre un punto fig1 = px.scatter( df_anio, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country", log_x=True, # escala logarítmica en X (el PBI tiene mucha variación) title=f"Riqueza vs. Expectativa de vida — {anio}", labels={"gdpPercap": "PBI per cápita (USD)", "lifeExp": "Expectativa de vida (años)"} ) # st.plotly_chart() renderiza el gráfico de Plotly en la app # use_container_width=True hace que ocupe todo el ancho disponible st.plotly_chart(fig1, use_container_width=True) # ── GRÁFICO 2: barras por continente ───────────────────────── # px.bar() genera un gráfico de barras interactivo en una línea # Agrupamos por continente y calculamos el promedio de expectativa de vida df_cont = df_anio.groupby("continent", as_index=False)["lifeExp"].mean().round(1) fig2 = px.bar( df_cont, x="continent", y="lifeExp", color="continent", title=f"Expectativa de vida promedio por continente — {anio}", labels={"lifeExp": "Expectativa de vida promedio (años)", "continent": "Continente"}, text="lifeExp" # muestra el valor encima de cada barra ) st.plotly_chart(fig2, use_container_width=True) # ── NOTA AL PIE ─────────────────────────────────────────────── # st.caption() muestra texto pequeño, ideal para fuentes o aclaraciones st.caption("Fuente: Gapminder Dataset — disponible en Plotly Express (px.data.gapminder())")

- La app se abre automáticamente en el navegador en http://localhost:8501

- Resultado esperado (valores aproximados del dataset para el año 2007)

- ── Gráfico 1: Dispersión Riqueza vs. Expectativa de vida (2007) ── Países con PBI alto (> 20.000 USD) tienden a mostrar expectativa > 75 años Países con PBI bajo (< 2.000 USD) concentran expectativas entre 45 y 65 años El tamaño de los puntos refleja población: China e India dominan visualmente Los continentes se distinguen por color: Europa arriba a la derecha, África abajo a la izquierda ── Gráfico 2: Barras por continente (2007) ── Continente Expectativa de vida promedio ───────────────────────────────────────────── Africa 54.8 años Americas 73.6 años Asia 70.7 años Europe 77.6 años Oceania 80.7 años

- ── Gráfico 1: Dispersión Riqueza vs. Expectativa de vida (2007) ── Países con PBI alto (> 20.000 USD) tienden a mostrar expectativa > 75 años Países con PBI bajo (< 2.000 USD) concentran expectativas entre 45 y 65 años El tamaño de los puntos refleja población: China e India dominan visualmente Los continentes se distinguen por color: Europa arriba a la derecha, África abajo a la izquierda ── Gráfico 2: Barras por continente (2007) ── Continente Expectativa de vida promedio ───────────────────────────────────────────── Africa 54.8 años Americas 73.6 años Asia 70.7 años Europe 77.6 años Oceania 80.7 años

- ¿Qué muestra el gráfico de dispersión?La posición de cada punto en el gráfico revela la situación de un país: estar en la esquina superior derecha significa alta riqueza y larga expectativa de vida; estar en la esquina inferior izquierda indica lo contrario. La escala logarítmica en el eje X es intencional: el PBI varía enormemente entre países y sin esa escala los países pobres quedarían aplastados contra el eje. Al mover el slider hacia atrás (por ejemplo, al año 1952), el patrón se mantiene pero los valores se desplazan hacia abajo y hacia la izquierda, mostrando que en general el mundo era más pobre y vivía menos años.

- ¿Qué muestra el gráfico de barras?Permite comparar continentes de un vistazo. En 2007, la diferencia entre África (54.8 años) y Europa (77.6 años) es de casi 23 años de expectativa de vida promedio. Este número surge directamente de los datos y no requiere ningún cálculo adicional: la barra lo hace visible de inmediato. Al cambiar el año con el slider, se puede observar cómo esa brecha se fue reduciendo o ampliando a lo largo del tiempo.

- ¿Qué decisión permite tomar?Un analista de política pública podría usar este dashboard para identificar qué continentes concentran los países con mayor rezago y en qué período histórico la brecha fue más pronunciada, orientando dónde focalizar recursos o investigación. Si solo se trabajara con una tabla de promedios estática, este patrón temporal requeriría generar múltiples reportes; el slider lo hace explorable en segundos.

- Error común de interpretaciónAsumir que mayor PBI per cápita causa directamente mayor expectativa de vida. El gráfico muestra una asociación entre ambas variables, no una relación causal. Países con PBI similar pueden tener expectativas de vida muy distintas según sus sistemas de salud, desigualdad interna u otros factores que no están en este dataset. La app visualiza la correlación; la causalidad requiere otro tipo de análisis.

- st.title() — título principal de la app, texto grande y destacado

- st.markdown() — texto con formato Markdown (negrita, cursiva, listas)

- st.divider() — línea horizontal separadora entre bloques

- st.slider() — control deslizante; devuelve el valor numérico elegido por el usuario

- st.metric() — indicador numérico destacado con etiqueta

- st.plotly_chart() — renderiza cualquier figura de Plotly con interactividad completa

- st.caption() — texto pequeño para fuentes, aclaraciones o notas al pie

- px.scatter() — gráfico de dispersión interactivo (Plotly Express)

- px.bar() — gráfico de barras interactivo (Plotly Express)

- Cuándo usar Plotly con Streamlit: cuando los usuarios necesitan explorar los datos directamente sobre el gráfico (zoom, hover, filtrar categorías por clic). Es especialmente útil en dashboards de análisis exploratorio donde no se sabe de antemano qué detalle interesa.

- Cuándo no es necesario: si el gráfico es solo ilustrativo y no requiere interacción, Matplotlib o Seaborn son suficientes y más livianos. No tiene sentido agregar interactividad si el usuario solo necesita ver una imagen estática en un informe.

- Limitación del slider con muchos valores: si el eje temporal tuviera datos continuos (fechas diarias, por ejemplo), el slider puede volverse difícil de manejar. En ese caso conviene usar st.select_slider() con una lista de valores discretos, o un st.selectbox().

- Buena práctica — separar carga de lógica: la línea df = px.data.gapminder() debería estar decorada con @st.cache_data en proyectos reales, para que el dataset no se recargue en cada interacción del slider. En este ejemplo es rápido porque el dataset es pequeño y está en memoria.

- Buena práctica — nombrar el archivo con sentido: dashboard.py es más claro que app.py cuando el proyecto tiene múltiples scripts. Streamlit puede manejar proyectos multipágina, pero eso corresponde a un nivel más avanzado.

- El slider filtra el dataset por año antes de dibujar los gráficos. Si quisieras agregar un segundo filtro por continente, ¿en qué parte del script lo colocarías y qué comando de Streamlit usarías?

- El gráfico de barras muestra el promedio de expectativa de vida por continente. ¿Qué información se pierde al usar el promedio? ¿Qué gráfico alternativo mostraría mejor la distribución dentro de cada continente?


---

# Clase 9 - Visualizaciones avanzadas - Teoria

Fuente: 4. Capítulo 4 — Deploy en la nube

## Titulos detectados
- 4. Capítulo 4 — Deploy en la nube

## Texto importante

- Deploy en la nube — GitHub + Streamlit Community Cloud

- ¿Qué vamos a hacer en este capítulo?

- Una vez que tu app funciona localmente, el siguiente paso es publicarla en internet para que cualquier persona pueda acceder a ella desde un navegador, sin instalar Python ni ejecutar ningún comando. El proceso completo tiene tres etapas: subir el código a GitHub, preparar el archivo de dependencias, y crear la app desde Streamlit Community Cloud. Todo es gratuito y toma menos de diez minutos.

- ¿Por qué GitHub? Streamlit Community Cloud no recibe archivos directamente: lee el código desde un repositorio de GitHub. Cada vez que actualizás el código en GitHub, la app en la nube se actualiza automáticamente. GitHub actúa como el puente entre tu código local y la aplicación publicada.

- ── ETAPA 1 — Crear un repositorio en GitHub ──

- Ingresá a github.com con tu cuenta. Si no tenés una, creá una cuenta gratuita antes de continuar. Una vez dentro, hacé clic en el botón verde "New" para crear un repositorio nuevo.

- Completá el formulario de la siguiente manera:

- Repository name: un nombre descriptivo, por ejemplo dashboard-gapminder

- Visibility: seleccioná Public (Streamlit Community Cloud gratuito requiere repositorios públicos)

- Initialize this repository with a README: activá esta opción para que el repositorio quede listo de inmediato

- Dejá el resto de las opciones con sus valores por defecto

- ── ETAPA 2 — Subir los archivos al repositorio ──

- Necesitás subir dos archivos al repositorio: el script de la app y el archivo de dependencias. Podés hacerlo directamente desde el navegador sin usar Git ni la terminal.

- Dentro de tu repositorio recién creado, hacé clic en "Add file" → "Upload files".

- Archivo 1 — El script de la app: subí el archivo dashboard.py que construimos en el capítulo anterior.

- Archivo 2 — El archivo de dependencias: Streamlit Community Cloud necesita saber qué librerías instalar. Para eso creás un archivo de texto llamado exactamente requirements.txt con el siguiente contenido:

- No es necesario incluir streamlit ni pandas porque Streamlit Community Cloud los instala por defecto. Solo se declaran las librerías adicionales que el script importa y que no vienen incluidas. En nuestro caso, la única dependencia extra es plotly.

- Una vez que arrastraste o seleccionaste ambos archivos, escribí un mensaje de commit breve (por ejemplo: "Agrego dashboard y requirements") y hacé clic en "Commit changes".

- Tu repositorio debería verse así al terminar esta etapa:

- dashboard-gapminder/ ├── dashboard.py ← el script de la app └── requirements.txt ← las dependencias (solo "plotly")

- dashboard-gapminder/ ├── dashboard.py ← el script de la app └── requirements.txt ← las dependencias (solo "plotly")

- ── ETAPA 3 — Crear la app en Streamlit Community Cloud ──

- Ingresá a share.streamlit.io. Si es tu primera vez, el sistema te va a pedir que inicies sesión con tu cuenta de GitHub y que autorices el acceso a tus repositorios. Aceptá los permisos que solicita.

- Una vez dentro de tu workspace, hacé clic en el botón "Create app" en la esquina superior derecha.

- El sistema te pregunta si ya tenés una app. Elegí la opción "Yup, I have an app" (ya tengo una app, es decir, ya tengo el código en GitHub).

- Completá los tres campos del formulario:

- Repository: seleccioná tu-usuario/dashboard-gapminder — debería aparecer en la lista desplegable

- Branch: dejá main (rama principal por defecto)

- Main file path: escribí dashboard.py

- De forma opcional podés personalizar la URL en el campo "App URL". Por ejemplo, si escribís mi-dashboard-gapminder, tu app va a quedar disponible en https://mi-dashboard-gapminder.streamlit.app.

- https://mi-dashboard-gapminder.streamlit.app

- Hacé clic en "Deploy". Streamlit Community Cloud comienza a preparar el entorno: instala Python, instala las dependencias del requirements.txt y ejecuta el script. Podés ver el proceso en tiempo real en el panel de logs de la derecha.

- La primera vez puede tomar entre 2 y 5 minutos dependiendo de las dependencias. Cuando termina, la app reemplaza la pantalla de logs y ya está disponible en la URL asignada.

- Tu app está publicada en internet con una URL propia. Podés copiarla y compartirla con cualquier persona. Quien acceda va a ver el dashboard completo, con el slider y los gráficos interactivos de Plotly, sin necesidad de instalar nada.

- URL de tu app: https://mi-dashboard-gapminder.streamlit.app (o el nombre automático asignado si no personalizaste la URL)

- URL de tu app: https://mi-dashboard-gapminder.streamlit.app (o el nombre automático asignado si no personalizaste la URL)

- Si en el futuro modificás el código, el proceso es simple: editá el archivo en GitHub (desde el navegador o desde tu computadora), guardá los cambios con un nuevo commit, y Streamlit detecta el cambio automáticamente y actualiza la app en pocos segundos. No es necesario volver a hacer el deploy.

- Paso 1 — Crear repositorio público en github.com con README

- Paso 2 — Subir dashboard.py y requirements.txt (con plotly adentro) via "Upload files"

- Paso 3 — Ingresar a share.streamlit.io con la cuenta de GitHub

- Paso 4 — Clic en "Create app" → "Yup, I have an app"

- Paso 5 — Seleccionar repositorio, rama main, archivo dashboard.py

- Paso 6 — Clic en "Deploy" y esperar 2-5 minutos

- Resultado — URL pública y compartible de la app

- El repositorio debe ser público para usar Streamlit Community Cloud de forma gratuita. Los repositorios privados requieren un plan pago.

- El nombre del archivo importa: el archivo de dependencias debe llamarse exactamente requirements.txt (en minúsculas, sin espacios). Si tiene otro nombre, Streamlit no lo va a detectar y la app puede fallar al intentar importar Plotly.

- Errores frecuentes: si la app no arranca, lo primero que hay que revisar es el panel de logs que aparece a la derecha durante el deploy. El error más común es un nombre de librería mal escrito en requirements.txt o un error de sintaxis en el script.

- Límite de recursos: las apps en el plan gratuito se "duermen" si no reciben visitas durante varios días. Al volver a acceder, se reactivan automáticamente en unos segundos.

- El archivo requirements.txt lista las librerías que Streamlit Community Cloud debe instalar. Si tu script usara también seaborn o scikit-learn, ¿qué cambio le harías a ese archivo?

- Cada cambio que hacés en GitHub se refleja automáticamente en la app desplegada. ¿Qué ventaja tiene esto en un proyecto donde varias personas trabajan sobre el mismo código?


---

# Clase 9 - Visualizaciones avanzadas - Teoria

Fuente: 5. Capítulo 6 — Resumen

## Titulos detectados
- 5. Capítulo 6 — Resumen
- ✅ Lo que vimos hoy
- 🔍 Dato aplicado

## Texto importante

- Hoy recorrimos el camino completo desde un script de análisis hasta una aplicación publicada en internet. El foco no estuvo en calcular más, sino en comunicar mejor: convertir resultados en algo que otros puedan explorar, interpretar y usar para tomar decisiones.

- Transforma código Python en una interfaz web interactiva sin conocimientos de desarrollo web.

- El script se re-ejecuta completo con cada interacción del usuario.

- Los widgets conectan la interfaz directamente con la lógica del análisis.

- Streamlit presenta resultados; no analiza ni valida datos por sí solo.

- Permite construir gráficos exploratorios que el usuario puede manipular directamente.

- Un gráfico de dispersión revela patrones entre dos variables numéricas.

- Un slider filtra los datos en tiempo real sin modificar el código.

- La interactividad no reemplaza el análisis; lo hace accesible.

- Publica la app con una URL pública conectando GitHub con Streamlit Cloud.

- El repositorio GitHub actúa como fuente única del código desplegado.

- requirements.txt declara las dependencias que la nube debe instalar.

- Cada actualización en GitHub se refleja automáticamente en la app.

- Regla práctica: Usá Streamlit cuando el análisis ya está validado y necesitás que otros lo exploren sin ejecutar código. No es el lugar para depurar ni para descubrir errores en los datos: eso se hace antes, en el notebook.

- Calcular es el punto de partida. Comunicar el resultado es lo que genera impacto.

- En la próxima clase vamos a profundizar en cómo organizar dashboards más complejos con múltiples páginas y cómo estructurar el código para que sea mantenible cuando el proyecto crece.

- Una organización de salud pública podría construir con Streamlit un panel interno donde los equipos regionales filtren indicadores por país y año, sin depender del equipo de datos para cada consulta. Lo que hoy vimos con el dataset Gapminder —explorar la relación entre riqueza y expectativa de vida por continente— es exactamente el tipo de análisis que ese panel necesitaría: interactivo, visual y sin barreras técnicas para el usuario final.


---

# Clase 9 - Visualizaciones avanzadas

Fuente: Clase 9 - Visualizaciones avanzadas

## Titulos detectados
- Sin titulos detectados

## Texto importante
- descripciones desactivadas, seleccionado

- captions and subtitles off, seleccionado

- Comienzo de la ventana de diálogo. La tecla Escape cancelará la operación y cerrará la ventana.


---

# Clase 10 — PCA - Analisis de componentes Principales

Fuente: Clase 10 — PCA - Analisis de componentes Principales

## Titulos detectados
- 1. Capítulo 1 — Objetivo y contexto
- 🎯 Objetivo
- 🚀 Comencemos
- 📚 Al final de esta clase vas a poder:

## Texto importante

- Al finalizar esta clase vas a poder aplicar reducción de dimensionalidad sobre datos reales, interpretar cuánta información se retiene en cada transformación y decidir cuántas dimensiones son suficientes para representar un dataset sin pérdida crítica. El foco no está en ejecutar código, sino en entender qué dice el resultado y qué decisión habilita.

- Ya sabés calcular medidas estadísticas, trabajar con DataFrames y ajustar modelos básicos. Ese conocimiento es el punto de partida. Pero en análisis de datos reales el desafío no es técnico: es saber leer lo que el resultado te está diciendo y traducirlo en una decisión concreta.

- Cuando un dataset tiene muchas variables, surge un problema silencioso: no todas aportan información nueva. Algunas repiten lo que otras ya dicen. Trabajar con ese exceso de variables sin revisarlo primero puede distorsionar modelos, dificultar visualizaciones y generar conclusiones equivocadas. Calcular no es interpretar, y ese es exactamente el error que esta clase busca corregir.

- Vamos a trabajar con datos reales de análisis químico de vinos y con mediciones morfológicas de flores. Ninguno de los dos datasets es trivial: tienen variables correlacionadas, escalas distintas y estructuras que no se ven a simple vista. La pregunta que guía la clase no es "¿cómo se calcula?" sino "¿qué significa este resultado y qué hago con él?"

- Identificar cuándo un conjunto de variables tiene redundancia informativa que justifica una reducción.

- Determinar cuántos componentes principales son suficientes usando la varianza explicada como criterio.

- Interpretar los loadings para entender qué variables originales dominan cada componente.

- Reconocer el efecto del escalado previo sobre los resultados y justificar su uso.

- Distinguir entre lo que un componente principal captura matemáticamente y lo que no se puede afirmar sobre él.


---

# Clase 10 — PCA - Analisis de componentes Principales

Fuente: 2. Capítulo 2 — Análisis de Componentes Principales (PCA)

## Titulos detectados
- 2. Capítulo 2 — Análisis de Componentes Principales (PCA)

## Texto importante

- Reducción de Dimensionalidad — Análisis de Componentes Principales (PCA)

- PCA transforma un conjunto de variables numéricas continuas correlacionadas en un nuevo conjunto de variables no correlacionadas llamadas componentes principales. Cada componente es una combinación lineal de las variables originales, orientada en la dirección de máxima varianza del espacio de datos, y es ortogonal (perpendicular geométricamente) a todos los componentes anteriores. Los pesos de esa combinación lineal se llaman loadings y determinan cuánto aporta cada variable original al componente. La fórmula fundamental es:

- donde el vector de pesos tiene norma unitaria y es perpendicular al de cualquier otro componente. La técnica responde a una pregunta concreta: ¿cuántas dimensiones son suficientes para representar la mayor parte de la variabilidad del dataset sin pérdida crítica de información?

- En estudios clínicos es habitual registrar decenas de biomarcadores por paciente: glucosa, triglicéridos, presión sistólica, IMC, colesterol. Muchas de estas variables están fuertemente correlacionadas entre sí. Aplicar PCA permite identificar un número reducido de ejes que resumen el estado metabólico del paciente, eliminando redundancias que distorsionarían un clasificador posterior. En el ejemplo a continuación se usa el dataset Iris (150 flores, 4 variables numéricas) para reducir las 4 dimensiones originales al mínimo de componentes que retenga al menos el 95 % de la varianza.

- # Paso 1 — Importaciones import numpy as np import pandas as pd from sklearn.datasets import load_iris from sklearn.preprocessing import StandardScaler from sklearn.decomposition import PCA # Paso 2 — Carga del dataset iris = load_iris() df = pd.DataFrame(iris.data, columns=iris.feature_names) df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names) # Paso 3 — Escalado OBLIGATORIO antes de PCA # Sin este paso, variables con mayor rango numérico dominan artificialmente # la dirección de máxima varianza, independientemente de su relevancia real. scaler = StandardScaler() X_scaled = scaler.fit_transform(df.drop('species', axis=1)) # Paso 4 — Ajuste de PCA sobre todas las componentes posibles pca_full = PCA() pca_full.fit(X_scaled) varianza = pca_full.explained_variance_ratio_ acumulada = 0 for i in range(len(varianza)): acumulada += varianza[i] print( f"PC{i + 1}: " f"{varianza[i] * 100:.2f}% | " f"Varianza acumulada: {acumulada * 100:.2f}%" ) # Paso 5 — Proyección a 2 componentes (decisión basada en varianza acumulada) pca_2d = PCA(n_components=2) X_pca = pca_2d.fit_transform(X_scaled) # Paso 6 — Loadings: cuánto aporta cada variable original a PC1 y PC2 loadings = pd.DataFrame( pca_2d.components_.T, index=iris.feature_names, columns=['PC1', 'PC2'] ) print(loadings.round(3))

- # Paso 1 — Importaciones import numpy as np import pandas as pd from sklearn.datasets import load_iris from sklearn.preprocessing import StandardScaler from sklearn.decomposition import PCA # Paso 2 — Carga del dataset iris = load_iris() df = pd.DataFrame(iris.data, columns=iris.feature_names) df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names) # Paso 3 — Escalado OBLIGATORIO antes de PCA # Sin este paso, variables con mayor rango numérico dominan artificialmente # la dirección de máxima varianza, independientemente de su relevancia real. scaler = StandardScaler() X_scaled = scaler.fit_transform(df.drop('species', axis=1)) # Paso 4 — Ajuste de PCA sobre todas las componentes posibles pca_full = PCA() pca_full.fit(X_scaled) varianza = pca_full.explained_variance_ratio_ acumulada = 0 for i in range(len(varianza)): acumulada += varianza[i] print( f"PC{i + 1}: " f"{varianza[i] * 100:.2f}% | " f"Varianza acumulada: {acumulada * 100:.2f}%" ) # Paso 5 — Proyección a 2 componentes (decisión basada en varianza acumulada) pca_2d = PCA(n_components=2) X_pca = pca_2d.fit_transform(X_scaled) # Paso 6 — Loadings: cuánto aporta cada variable original a PC1 y PC2 loadings = pd.DataFrame( pca_2d.components_.T, index=iris.feature_names, columns=['PC1', 'PC2'] ) print(loadings.round(3))

- Resultado — varianza explicada por componente

- Sin necesidad de ejecutar el código, estos son los valores que produce el análisis sobre el dataset Iris escalado:

- PC1: 72.77 % de varianza explicada | Acumulada: 72.77 %

- PC2: 23.03 % de varianza explicada | Acumulada: 95.80 %

- PC3: 3.68 % de varianza explicada | Acumulada: 99.48 %

- PC4: 0.52 % de varianza explicada | Acumulada: 100.00 %

- Resultado — loadings (contribución de cada variable a PC1 y PC2)

- sepal length (cm): PC1 = 0.521 | PC2 = 0.377

- sepal width (cm): PC1 = −0.269 | PC2 = 0.923

- petal length (cm): PC1 = 0.580 | PC2 = −0.024

- petal width (cm): PC1 = 0.565 | PC2 = −0.067

- ¿Qué significa este resultado?Con solo 2 componentes se retiene el 95.80 % de la varianza del dataset original de 4 variables. La pérdida de información al reducir dimensiones es de apenas el 4.2 %, lo que justifica la proyección. Analizando los loadings, PC1 recibe contribuciones altas y similares de longitud de pétalo (0.58), ancho de pétalo (0.57) y longitud de sépalo (0.52): resume principalmente el tamaño general de la flor. PC2 está dominada casi exclusivamente por el ancho del sépalo (0.92) y captura una dimensión de forma del sépalo que varía de manera independiente a las demás variables.

- ¿Qué decisión permite tomar?El resultado habilita usar únicamente PC1 y PC2 como variables de entrada para un clasificador o algoritmo de clustering, reduciendo el espacio de trabajo de 4 a 2 dimensiones. Esto elimina las redundancias entre variables originales (petal length y petal width están fuertemente correlacionadas) y reduce el costo computacional sin pérdida relevante de estructura.Si no se aplica esta reducción: un modelo entrenado sobre las 4 variables originales operará con correlaciones redundantes entre ellas, lo que puede inflar artificialmente el peso de ciertos predictores y reducir la capacidad de generalización.

- Error común de interpretaciónConcluir que "PC1 mide el tamaño de la flor" como una propiedad permanente o universal. Los loadings son específicos de este dataset y de este escalado particular. Si se agregan nuevas variables, se cambia la muestra o se omite el paso de escalado, los pesos cambian completamente y la interpretación anterior deja de ser válida. Los componentes principales no tienen nombre propio: reciben sentido únicamente al analizar los loadings del caso concreto.

- Cuándo usarlo: cuando hay muchas variables numéricas correlacionadas, cuando se necesita visualizar estructura en alta dimensión, o cuando se quiere reducir ruido antes de aplicar un modelo supervisado.

- Cuándo no usarlo: cuando las variables son categóricas (PCA requiere datos numéricos continuos), cuando la interpretabilidad de las variables originales es crítica para el negocio, o cuando las relaciones entre variables son no lineales (en ese caso considerar t-SNE o UMAP).

- Limitaciones: PCA solo captura estructura lineal; es sensible a outliers, que pueden distorsionar la dirección de máxima varianza; los componentes no son directamente interpretables como las variables originales.

- Buenas prácticas: escalar siempre con StandardScaler antes de aplicar PCA; definir el número de componentes usando el scree plot y el umbral de varianza acumulada; reportar los loadings junto al gráfico de dispersión para contextualizar cualquier interpretación.

- En el ejemplo, PC2 está dominada casi exclusivamente por el ancho del sépalo (loading 0.92), mientras que las variables de pétalo prácticamente no contribuyen. ¿Esto significa que PC2 es útil para distinguir entre las tres especies de Iris, o podría estar capturando variación que no aporta poder discriminativo real? ¿Cómo lo verificarías con los datos disponibles?

- Si el dataset no estuviera escalado y la longitud del pétalo tomara valores entre 1 y 7 cm mientras que el ancho del sépalo varía entre 2 y 4 cm, ¿cuál de las dos dominaría PC1 por razones puramente numéricas? ¿Qué problema metodológico representa eso y cómo lo resolverías?


---

# Clase 10 — PCA - Analisis de componentes Principales

Fuente: 3. Capítulo 3 — Ejercicio práctico

## Titulos detectados
- 3. Capítulo 3 — Ejercicio práctico

## Texto importante

- Ejercicio práctico: Reducción de Dimensionalidad con PCA — Dataset Wine

- El dataset Wine contiene los resultados de un análisis químico de 178 vinos producidos en Italia, clasificados en 3 variedades. Para cada vino se registraron 13 variables numéricas continuas: alcohol, ácido málico, ceniza, alcalinidad de ceniza, magnesio, fenoles totales, flavonoides, fenoles no flavonoides, proantocianidinas, intensidad de color, matiz, OD280/OD315 y prolina. Las variables se encuentran en escalas muy distintas entre sí.

- A partir de este dataset se te pide:

- Aplicar el preprocesamiento necesario antes de ejecutar PCA y justificar por qué es obligatorio en este caso.

- Calcular la varianza explicada por cada componente principal y determinar cuántos componentes son suficientes para retener al menos el 80 % de la varianza total.

- Analizar los loadings de los dos primeros componentes e identificar qué variables originales tienen mayor peso en cada uno.

- Proyectar los datos sobre los dos primeros componentes y visualizar si las tres variedades de vino quedan separadas en ese nuevo espacio.

- A continuación se presenta el desarrollo completo con explicaciones paso a paso. Antes de leer cada bloque de interpretación, encontrarás una pregunta para que te detengas a pensar en el resultado antes de leer la respuesta.

- # Paso 1 — Importaciones import numpy as np import pandas as pd import matplotlib.pyplot as plt import seaborn as sns from sklearn.datasets import load_wine from sklearn.preprocessing import StandardScaler from sklearn.decomposition import PCA # Paso 2 — Carga del dataset wine = load_wine() df = pd.DataFrame(wine.data, columns=wine.feature_names) df['variety'] = pd.Categorical.from_codes(wine.target, wine.target_names) print("Shape:", df.shape) print(df.describe().round(2))

- # Paso 1 — Importaciones import numpy as np import pandas as pd import matplotlib.pyplot as plt import seaborn as sns from sklearn.datasets import load_wine from sklearn.preprocessing import StandardScaler from sklearn.decomposition import PCA # Paso 2 — Carga del dataset wine = load_wine() df = pd.DataFrame(wine.data, columns=wine.feature_names) df['variety'] = pd.Categorical.from_codes(wine.target, wine.target_names) print("Shape:", df.shape) print(df.describe().round(2))

- Resultado — estadísticas descriptivas (resumen)

- alcohol: media 13.00, rango aprox. 11.0 – 14.8

- magnesium: media 99.74, rango aprox. 70 – 162

- proline: media 746.89, rango aprox. 278 – 1680

- flavanoids: media 2.03, rango aprox. 0.34 – 5.08

- Antes de continuar — pregunta 1:Mirá los rangos de las variables. Prolina llega hasta 1680, mientras que flavonoides no supera 5.08. Si aplicaras PCA directamente sobre estos datos sin escalar, ¿qué variable dominaría la dirección de máxima varianza? ¿Eso sería un reflejo real de su importancia química, o un artefacto numérico?

- # Paso 3 — Escalado obligatorio # Las 13 variables tienen escalas radicalmente distintas. # Sin StandardScaler, prolina (valores ~700) dominaría PC1 # por razones puramente numéricas, no por relevancia real. scaler = StandardScaler() X_scaled = scaler.fit_transform(df.drop('variety', axis=1))

- # Paso 3 — Escalado obligatorio # Las 13 variables tienen escalas radicalmente distintas. # Sin StandardScaler, prolina (valores ~700) dominaría PC1 # por razones puramente numéricas, no por relevancia real. scaler = StandardScaler() X_scaled = scaler.fit_transform(df.drop('variety', axis=1))

- Respuesta a pregunta 1:Sin escalado, prolina dominaría PC1 con valores hasta 1680, frente a flavonoides con máximo 5.08. PCA maximiza varianza: una variable con mayor dispersión numérica siempre gana, aunque no sea más informativa. El escalado corrige este artefacto llevando todas las variables a media 0 y desviación estándar 1, poniendo a todas en igualdad de condiciones.

- # Paso 4 — PCA sobre todas las componentes pca_full = PCA() pca_full.fit(X_scaled) varianza = pca_full.explained_variance_ratio_ acumulada = 0 for i in range(len(varianza)): acumulada += varianza[i] print( f"PC{i + 1}: " f"{varianza[i] * 100:.2f}% | " f"Varianza acumulada: {acumulada * 100:.2f}%" )

- # Paso 4 — PCA sobre todas las componentes pca_full = PCA() pca_full.fit(X_scaled) varianza = pca_full.explained_variance_ratio_ acumulada = 0 for i in range(len(varianza)): acumulada += varianza[i] print( f"PC{i + 1}: " f"{varianza[i] * 100:.2f}% | " f"Varianza acumulada: {acumulada * 100:.2f}%" )

- Resultado — varianza explicada por componente

- PC1: 36.20 % | Varianza Acumulada: 36.20 %

- PC2: 19.33 % | Varianza Acumulada: 55.53 %

- PC3: 11.10 % | Varianza Acumulada: 66.63 %

- PC4: 7.15 % | Varianza Acumulada: 73.78 %

- PC5: 6.55 % | Varianza Acumulada: 80.33 %

- PC6: 4.97 % | Varianza Acumulada: 85.30 %

- PC7: 4.24 % | Varianza Acumulada: 89.54 %

- PC8 a PC13: restante 10.46 % distribuido

- Antes de continuar — pregunta 2:Con el dataset Iris bastaban 2 componentes para superar el 95 % de varianza. Acá, con 13 variables, ¿cuántos componentes necesitarías para llegar al 80 %? ¿Qué dice eso sobre la estructura del dataset Wine comparado con Iris?

- Respuesta a pregunta 2:Se necesitan 5 componentes para superar el 80 % de varianza (80.33 %). Iris llegaba al 95.80 % con solo 2. Esto indica que el dataset Wine tiene una estructura más distribuida: la información no está concentrada en una o dos direcciones dominantes, sino repartida entre más dimensiones. Las 13 variables químicas aportan variabilidad en múltiples ejes independientes, lo que hace la reducción más costosa en términos de componentes necesarios.

- # Paso 5 — Proyección a 2 componentes para visualización pca_2d = PCA(n_components=2) X_pca = pca_2d.fit_transform(X_scaled) df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2']) df_pca['variety'] = df['variety'] # Paso 6 — Loadings: contribución de variables originales loadings = pd.DataFrame( pca_2d.components_.T, index=wine.feature_names, columns=['PC1', 'PC2'] ) print(loadings.round(3))

- # Paso 5 — Proyección a 2 componentes para visualización pca_2d = PCA(n_components=2) X_pca = pca_2d.fit_transform(X_scaled) df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2']) df_pca['variety'] = df['variety'] # Paso 6 — Loadings: contribución de variables originales loadings = pd.DataFrame( pca_2d.components_.T, index=wine.feature_names, columns=['PC1', 'PC2'] ) print(loadings.round(3))

- Resultado — loadings PC1 y PC2 (valores aproximados)

- flavanoids: PC1 = −0.422 | PC2 = 0.159

- od280/od315_of_diluted_wines: PC1 = −0.403 | PC2 = 0.152

- total_phenols: PC1 = −0.394 | PC2 = 0.138

- proanthocyanins: PC1 = −0.313 | PC2 = 0.087

- color_intensity: PC1 = 0.302 | PC2 = 0.517

- proline: PC1 = −0.286 | PC2 = −0.198

- alcohol: PC1 = −0.234 | PC2 = −0.485

- ash, alcalinity, magnesium, malic_acid, nonflavanoid_phenols: contribuciones menores en ambos ejes

- Antes de continuar — pregunta 3:PC1 tiene loadings negativos altos en flavonoides, fenoles y OD280 (todos indicadores de compuestos polifenólicos). ¿Qué dirías que resume PC1 en términos del contenido del vino? ¿Y qué podría estar capturando PC2, donde color_intensity (0.517) y alcohol (−0.485) tienen los pesos más altos y en sentidos opuestos?

- Respuesta a pregunta 3:PC1 agrupa variables asociadas a compuestos polifenólicos (flavonoides, fenoles totales, OD280): podría interpretarse como un eje de riqueza en polifenoles. Los loadings son negativos, lo que significa que valores altos de PC1 corresponden a vinos con menor concentración de estos compuestos. PC2 opone intensidad de color (positivo alto) con alcohol (negativo alto): podría relacionarse con el perfil cromático y alcohólico del vino. Importante: estas interpretaciones son tentativas y específicas de este dataset escalado. No son propiedades universales de los componentes.

- # Paso 7 — Visualización de la proyección plt.figure(figsize=(8, 5)) sns.scatterplot( data=df_pca, x='PC1', y='PC2', hue='variety', palette='Set2', s=80, alpha=0.85 ) plt.title('Proyección PCA — Wine Dataset (2 componentes)') plt.xlabel(f"PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% varianza)") plt.ylabel(f"PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% varianza)") plt.tight_layout() plt.savefig('pca_wine_scatter.png', dpi=150) plt.show()

- # Paso 7 — Visualización de la proyección plt.figure(figsize=(8, 5)) sns.scatterplot( data=df_pca, x='PC1', y='PC2', hue='variety', palette='Set2', s=80, alpha=0.85 ) plt.title('Proyección PCA — Wine Dataset (2 componentes)') plt.xlabel(f"PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% varianza)") plt.ylabel(f"PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% varianza)") plt.tight_layout() plt.savefig('pca_wine_scatter.png', dpi=150) plt.show()

- Resultado esperado del gráfico:La variedad class_0 aparece claramente separada hacia valores negativos de PC1 (alta concentración de polifenoles). Las variedades class_1 y class_2 se distinguen principalmente sobre el eje PC2. Las tres variedades muestran separación visible con solo 2 componentes, a pesar de que estos dos componentes juntos solo explican el 55.53 % de la varianza total.

- Antes de continuar — pregunta 4:Con solo el 55.53 % de varianza explicada, los 2 componentes no capturan ni la mitad de la información original. Sin embargo, en el gráfico las tres variedades quedan visualmente separadas. ¿Cómo interpretarías esa aparente contradicción? ¿Significa que 2 componentes son suficientes para este problema?

- Respuesta a pregunta 4:No necesariamente. Que las variedades se vean separadas en 2 dimensiones indica que parte de la estructura discriminativa está concentrada en PC1 y PC2. Pero el 44.47 % de varianza restante podría contener información adicional relevante para separar casos ambiguos o mejorar un clasificador. Para visualización exploratoria, 2 componentes son útiles. Para un modelo de clasificación robusto, habría que evaluar si los 5 componentes que superan el 80 % mejoran el rendimiento frente a usar solo 2.

- Cuándo usarlo: cuando las variables tienen escalas muy distintas entre sí (como en este dataset), cuando hay correlaciones fuertes entre variables del mismo dominio (polifenoles), o cuando se quiere explorar visualmente la separación entre grupos antes de aplicar un clasificador.

- Cuándo no usarlo: cuando se necesita mantener la interpretabilidad de las variables originales para reportar al cliente o al área de negocio; cuando las relaciones entre variables son no lineales.

- Limitaciones: con 13 variables la varianza no se concentra tan fácilmente como con 4; la elección del número de componentes implica siempre un trade-off entre compresión e información retenida.

- Buenas prácticas: siempre escalar antes de PCA; no elegir el número de componentes por defecto ni de forma arbitraria; reportar el porcentaje de varianza acumulada junto a cualquier visualización de componentes.

- En este ejercicio se usaron 2 componentes para la visualización, pero 5 para superar el 80 % de varianza. Si tuvieras que entrenar un clasificador de variedades de vino usando los componentes como entrada, ¿usarías 2 o 5? ¿Qué criterio aplicarías para decidirlo y cómo lo verificarías empíricamente?

- Los loadings de PC1 agrupan variables polifenólicas con signo negativo. ¿Qué implicaría para la interpretación si al repetir el análisis con una muestra diferente de vinos esos mismos loadings aparecieran con signo positivo? ¿Cambiaría la estructura del componente o solo su orientación en el espacio?


---

# Clase 10 — PCA - Analisis de componentes Principales

Fuente: 4. Capítulo 4 — Resumen

## Titulos detectados
- 4. Capítulo 4 — Resumen
- ✅ Lo que vimos hoy
- 🔍 Dato aplicado

## Texto importante

- Trabajamos con datos reales de flores y vinos para entender cómo reducir dimensiones sin perder información crítica. El foco no estuvo en ejecutar la técnica, sino en leer sus resultados y decidir a partir de ellos.

- Varianza explicada como criterio de decisiónPermite saber cuánta información retiene cada componente y cuántos son suficientes.

- No elegir componentes por defecto: usar varianza acumulada.

- Un umbral común es 80–95 %, según el problema.

- variables no siempre significa menos componentes necesarios.

- Loadings: qué aporta cada variable originalPermiten entender qué variables dominan cada componente, en este dataset.

- Un loading alto indica fuerte contribución de esa variable al componente.

- La interpretación de un componente depende del contexto y los datos.

- Los componentes no tienen nombre propio: el analista los interpreta.

- Escalado previo: condición no negociableSin escalar, variables con mayor rango numérico dominan artificialmente.

- StandardScaler lleva todas las variables a la misma escala.

- El escalado cambia los resultados, no solo la presentación.

- Omitirlo introduce un sesgo metodológico, no un error de código.

- Regla práctica: antes de aplicar PCA, revisá las escalas de tus variables. Si hay diferencias grandes entre rangos, el escalado no es opcional. Y antes de interpretar un componente, leé sus loadings: el número solo no dice nada.

- Calcular componentes es el paso más fácil. Saber qué representan y cuántos usar es el trabajo real del analista.

- En la industria vitivinícola, una bodega podría aplicar PCA sobre perfiles químicos de sus vinos —fenoles, alcohol, color, acidez— para identificar qué combinación de variables distingue mejor sus variedades sin necesidad de análisis manual variable por variable. Con pocos componentes bien interpretados, el enólogo podría detectar lotes atípicos o agrupar vinos por perfil sensorial antes de etiquetarlos comercialmente.


---

# Proyecto Integrador

Fuente: Proyecto Integrador

## Titulos detectados
- 1. Contexto y Objetivos

## Texto importante

- El Proyecto Integrador consiste en desarrollar un análisis de datos reproducible y comunicable a partir del dataset provisto por la cátedra. El trabajo deberá evidenciar un proceso ordenado de exploración, preparación, análisis, interpretación y comunicación de resultados.

- Aplicar los contenidos de Minería de Datos 1 para construir un proyecto de análisis de datos con decisiones justificadas, trazabilidad del proceso y comunicación clara de los resultados.

- Comprender la estructura y la calidad inicial del dataset mediante una inspección documentada.

- Preparar los datos a partir de decisiones justificadas con evidencia observada.

- Realizar análisis univariado, bivariado y multivariado con interpretaciones vinculadas a los objetivos definidos por el grupo.

- Aplicar escalamiento y reducción de dimensionalidad mediante PCA, documentando las decisiones y resultados obtenidos.

- Comunicar resultados mediante una aplicación pública en Streamlit y un informe final breve.

- Construir un repositorio reproducible que permita revisar el proceso completo, desde los datos originales hasta las conclusiones.

- El proyecto incluye inspección inicial, calidad de datos, preparación, análisis exploratorio, visualización, escalamiento y PCA. No es un proyecto de modelado predictivo ni de despliegue de modelos.

- No se evaluará únicamente la aplicación de funciones, la cantidad de código o la cantidad de gráficos. Se evaluarán principalmente las decisiones justificadas con evidencia, la trazabilidad del proceso, la coherencia entre etapas y la claridad para comunicar resultados. Las decisiones deben surgir de la inspección y de la evidencia obtenida durante el proyecto, no de la aplicación automática de técnicas.


---

# Clase 2 — Análisis Univariado

Fuente: Capítulo 2 — Medidas de tendencia central

## Titulos detectados
- 🎯 ¿Dónde se concentran los datos?
- 📊 Media
- 📊 Mediana
- 📊 Moda
- 🐍 Ejemplo de aplicación
- 💡 Dato curioso
- 🔍 Medidas de tendencia central en salud pública
- Ejemplo de análisis

## Texto importante
- Las medidas de tendencia central responden una pregunta básica: ¿cuál es el valor típico de esta variable? Hay tres formas de responderla, y cada una dice algo diferente.

- Es la suma de todos los valores dividida por la cantidad de observaciones.

- Es la medida más usada, pero la más sensible a valores extremos. Si hay un valor muy alto o muy bajo en el conjunto, la media se desplaza hacia ese extremo aunque no represente al resto de los datos.

- Es el valor que divide al conjunto exactamente en dos mitades cuando los datos están ordenados. Si hay un número par de observaciones, es el promedio de los dos valores centrales.

- No le afectan los extremos. Cuando la distribución está sesgada o hay outliers, la mediana representa mejor al dato típico que la media.

- Es el valor que más se repite. Puede haber más de una moda (distribución bimodal o multimodal).

- Es la única medida de tendencia central aplicable a variables cualitativas.

- Vamos a calcular la media, mediana y moda de la edad de los pasajeros del Titanic.

- # Importar librerías import pandas as pd # Cargar el dataset df = pd.read_csv('titanic.csv') # Primeras filas df.head()

- # Importar librerías import pandas as pd # Cargar el dataset df = pd.read_csv('titanic.csv') # Primeras filas df.head()

- # Media media_edad = df['Age'].mean() print(f'Media de edad: {media_edad:.2f}') # Mediana mediana_edad = df['Age'].median() print(f'Mediana de edad: {mediana_edad:.2f}') # Moda moda_edad = df['Age'].mode()[0] print(f'Moda de edad: {moda_edad:.2f}')

- # Media media_edad = df['Age'].mean() print(f'Media de edad: {media_edad:.2f}') # Mediana mediana_edad = df['Age'].median() print(f'Mediana de edad: {mediana_edad:.2f}') # Moda moda_edad = df['Age'].mode()[0] print(f'Moda de edad: {moda_edad:.2f}')

- Media de edad: 29.70 Mediana de edad: 28.00 Moda de edad: 24.00

- Media de edad: 29.70 Mediana de edad: 28.00 Moda de edad: 24.00

- La media (29.70) es mayor que la mediana (28.00). Esa diferencia no es casualidad: indica que hay pasajeros con edades muy altas que están "tirando" la media hacia arriba, aunque la mayoría era más joven. La moda (24.00) nos dice que la edad más frecuente era 24 años.

- Cuando media > mediana, la distribución tiene cola hacia la derecha: hay valores altos que alejan la media del centro real de los datos.

- Cuando media > mediana, la distribución tiene cola hacia la derecha: hay valores altos que alejan la media del centro real de los datos.

- En salud pública, las medidas de tendencia central se utilizan para analizar el perfil de una población.

- Cuando se reporta el “promedio de edad” de los afectados por una enfermedad, ese dato puede resultar engañoso si existen valores extremos.

- - La media de edad es 45 años - La mediana es 38 años - La moda es 28 años

- La diferencia entre media y mediana indica que un grupo reducido de edades altas está elevando el promedio. La moda muestra cuál es el grupo más frecuente.

- Este tipo de análisis permite orientar decisiones, por ejemplo, al definir el público objetivo de una campaña de salud.


---

# Clase 2 — Análisis Univariado

Fuente: Capítulo 3 — Medidas de dispersión

## Titulos detectados
- 🎯 ¿Cuánto se alejan los datos del centro?
- 📊 Rango
- 📊 Varianza
- 📊 Desvío estándar
- 📊 Rango intercuartílico (IQR)
- 🐍 Ejemplo de aplicación
- 💡 Dato curioso
- 🔍 Dispersión en control de calidad industrial

## Texto importante
- Dos variables pueden tener exactamente la misma media y ser completamente distintas. La dispersión mide qué tan concentrados o esparcidos están los valores alrededor del centro.

- Es la diferencia entre el valor máximo y el mínimo.

- Simple de calcular, pero muy sensible a outliers. Un solo valor extremo lo distorsiona por completo.

- Mide el promedio de las desviaciones al cuadrado respecto a la media. El cuadrado penaliza las desviaciones grandes más que las pequeñas.

- El problema práctico: está en unidades al cuadrado. Si medimos edades en años, la varianza está en años². Difícil de interpretar directamente.

- Es la raíz cuadrada de la varianza. Vuelve a las unidades originales y es la medida de dispersión más usada en la práctica.

- Un desvío estándar alto indica que los datos están muy esparcidos alrededor de la media. Uno bajo indica que están concentrados cerca de ella.

- Es la diferencia entre el percentil 75 (Q3) y el percentil 25 (Q1). Representa el 50% central de los datos e ignora completamente los extremos.

- Es la medida de dispersión más robusta cuando hay outliers o distribuciones asimétricas.

- Vamos a calcular las medidas de dispersión sobre la variable Fare (tarifa pagada por cada pasajero).

- # Rango rango_fare = df['Fare'].max() - df['Fare'].min() print(f'Rango de tarifas: {rango_fare:.2f}') # Varianza varianza_fare = df['Fare'].var() print(f'Varianza de tarifas: {varianza_fare:.2f}') # Desvío estándar std_fare = df['Fare'].std() print(f'Desvío estándar de tarifas: {std_fare:.2f}') # IQR q1 = df['Fare'].quantile(0.25) q3 = df['Fare'].quantile(0.75) iqr_fare = q3 - q1 print(f'IQR de tarifas: {iqr_fare:.2f}')

- # Rango rango_fare = df['Fare'].max() - df['Fare'].min() print(f'Rango de tarifas: {rango_fare:.2f}') # Varianza varianza_fare = df['Fare'].var() print(f'Varianza de tarifas: {varianza_fare:.2f}') # Desvío estándar std_fare = df['Fare'].std() print(f'Desvío estándar de tarifas: {std_fare:.2f}') # IQR q1 = df['Fare'].quantile(0.25) q3 = df['Fare'].quantile(0.75) iqr_fare = q3 - q1 print(f'IQR de tarifas: {iqr_fare:.2f}')

- Rango de tarifas: 512.33 Varianza de tarifas: 2469.44 Desvío estándar de tarifas: 49.69 IQR de tarifas: 31.00

- Rango de tarifas: 512.33 Varianza de tarifas: 2469.44 Desvío estándar de tarifas: 49.69 IQR de tarifas: 31.00

- El rango (512.33) es enorme: hubo pasajeros que pagaron casi nada y otros que pagaron fortunas. Pero ese número está completamente dominado por los extremos.

- El desvío estándar (49.69) es casi igual a la media de la tarifa. Eso indica una dispersión muy alta: los datos están muy esparcidos y la media no representa bien a la mayoría.

- El IQR (31.00) es mucho más bajo. Eso significa que el 50% central de los pasajeros pagó tarifas dentro de un rango de 31 unidades. Ese es el comportamiento real de la mayoría, sin que los pasajeros de primera clase distorsionen el análisis.

- Cuando el desvío estándar es cercano o mayor a la media, el IQR es más honesto para describir la dispersión real del grupo central.

- Cuando el desvío estándar es cercano o mayor a la media, el IQR es más honesto para describir la dispersión real del grupo central.

- En manufactura, el desvío estándar es una de las métricas más críticas. No alcanza con que el producto promedio cumpla las especificaciones: si la dispersión es alta, muchas unidades van a estar fuera del rango aceptable.

- Una planta embotelladora debe llenar botellas con exactamente 500 ml. El equipo de calidad mide una muestra y obtiene:

- Desvío estándar: 8.5 ml ⚠️ — hay botellas con 491 ml y otras con 509 ml

- Aunque la media es aceptable, el desvío alto indica que muchas botellas están fuera del rango permitido (±3 ml). El problema no está en el centro, está en la dispersión. Sin medir el desvío, ese problema sería invisible.


---

# Proyecto Integrador

Fuente: 2. Entregables del proyecto y requisitos de entrega

## Titulos detectados
- 2. Entregables del proyecto y requisitos de entrega

## Texto importante
- Entregables del proyecto y requisitos de entrega

- Se admite un grupo de 3 integrantes solo con autorización excepcional.

- Cada grupo deberá presentar un repositorio público de GitHub.

- La estructura obligatoria del repositorio no debe modificarse.

- Estructura obligatoria del repositorio

- PI_Mineria_Datos_1/ │ ├── README.md ├── requirements.txt │ ├── data/ │ ├── raw/ │ └── processed/ │ ├── notebooks/ │ ├── 01_inspeccion_inicial.ipynb │ ├── 02_calidad_y_limpieza.ipynb │ ├── 03_eda.ipynb │ ├── 04_pca.ipynb │ └── 05_conclusiones.ipynb │ ├── app/ │ ├── Home.py │ └── pages/ │ ├── 01_Dataset.py │ ├── 02_EDA.py │ ├── 03_PCA.py │ └── 04_Conclusiones.py │ ├── reports/ │ └── informe_final.pdf │ └── logs/ └── pipeline_log.csv

- PI_Mineria_Datos_1/ │ ├── README.md ├── requirements.txt │ ├── data/ │ ├── raw/ │ └── processed/ │ ├── notebooks/ │ ├── 01_inspeccion_inicial.ipynb │ ├── 02_calidad_y_limpieza.ipynb │ ├── 03_eda.ipynb │ ├── 04_pca.ipynb │ └── 05_conclusiones.ipynb │ ├── app/ │ ├── Home.py │ └── pages/ │ ├── 01_Dataset.py │ ├── 02_EDA.py │ ├── 03_PCA.py │ └── 04_Conclusiones.py │ ├── reports/ │ └── informe_final.pdf │ └── logs/ └── pipeline_log.csv

- data/raw/ debe contener el dataset original sin modificaciones.

- data/processed/ debe contener el dataset final utilizado durante el análisis.

- notebooks/ debe contener el desarrollo ordenado de las etapas del proyecto.

- app/ debe contener la aplicación pública desarrollada en Streamlit.

- reports/ debe contener el informe final en PDF.

- logs/ debe contener el registro de las transformaciones realizadas durante el proceso ETL.

- README.md debe documentar técnicamente el proyecto mediante texto y enlaces.

- requirements.txt debe declarar las dependencias necesarias para ejecutar el proyecto.

- El archivo README.md debe incluir las siguientes secciones:

- Debe respetar los siguientes límites:

- Objetivo del proyecto: máximo 10 líneas.

- Preparación y calidad de datos: máximo 20 líneas.

- Resumen del análisis exploratorio: máximo 20 líneas.

- Reducción de dimensionalidad: máximo 15 líneas.

- El README debe contener solo texto y enlaces. No se permiten imágenes, capturas ni gráficos. No debe duplicar resultados ya presentados en Streamlit o en el informe. Debe referenciar notebooks, informe, log ETL y aplicación cuando corresponda, incluir instrucciones breves para ejecutar la aplicación localmente e incorporar el enlace público a Streamlit Cloud.

- app/ ├── Home.py └── pages/ ├── 01_Dataset.py ├── 02_EDA.py ├── 03_PCA.py └── 04_Conclusiones.py

- app/ ├── Home.py └── pages/ ├── 01_Dataset.py ├── 02_EDA.py ├── 03_PCA.py └── 04_Conclusiones.py

- La aplicación debe estar desplegada públicamente en Streamlit Cloud.

- Debe incluir un enlace al repositorio público de GitHub.

- Debe comunicar resultados para público general y no reemplaza la evidencia técnica del repositorio.

- El diseño, los filtros, la interacción y la narrativa visual quedan a criterio del grupo.

- Home: título del proyecto, integrantes, comisión, fecha, contexto breve y enlace al repositorio GitHub.

- Dataset: descripción general, resumen breve de calidad, vista previa simple y mención breve de las transformaciones principales.

- EDA: 2 visualizaciones univariadas, 2 visualizaciones bivariadas, 1 visualización multivariada e interpretación obligatoria para cada resultado. Total exacto: 5 visualizaciones.

- PCA: variables utilizadas, escalamiento aplicado, varianza explicada, interpretación y máximo 2 visualizaciones.

- Conclusiones: hallazgos, limitaciones y próximos pasos.

- El archivo reports/informe_final.pdf debe entregarse en formato PDF, con una extensión máxima de 2 páginas. Puede incluir solo texto, tablas pequeñas y enlaces. No debe incluir código ni repetir gráficos ya presentes en Streamlit.

- Decisiones de limpieza y preparación.

- Hallazgos del análisis exploratorio.

- Enlaces al repositorio y a Streamlit.

- El archivo logs/pipeline_log.csv debe registrar cada transformación relevante con las siguientes columnas mínimas:

- Paso | Descripción | Filas | Nulos | Retención (%)

- Paso | Descripción | Filas | Nulos | Retención (%)

- El registro debe permitir comparar el estado inicial y final del dataset.

- Dataset original preservado en data/raw/.

- Dataset procesado disponible en data/processed/.

- Dependencias declaradas en requirements.txt.

- Enlaces públicos funcionales al repositorio y a Streamlit.

- Repositorio sin credenciales, claves ni archivos sensibles.

- Repositorio sin archivos innecesarios.

- Repositorio público con la estructura obligatoria completa.

- Dataset original y dataset procesado disponibles en las carpetas correspondientes.

- README completo, dentro de los límites indicados y con enlaces funcionales.

- Aplicación pública en Streamlit Cloud con enlace al repositorio.

- Informe final en reports/informe_final.pdf.

- Log ETL disponible en logs/pipeline_log.csv.


---

# Proyecto Integrador

Fuente: 3. Guía para el desarrollo del proyecto integrador

## Titulos detectados
- 3. Guía para el desarrollo del proyecto integrador

## Texto importante
- Guía para el desarrollo del proyecto integrador

- Esta guía organiza el proceso de trabajo y define dónde debe evidenciarse cada etapa. El objetivo es construir un análisis coherente, justificable y reproducible, sin reemplazar las decisiones que correspondan al grupo.

- Revisen el dataset y la documentación disponible.

- Comprendan qué representa cada registro y cuál es el alcance de la información disponible.

- Identifiquen variables, tipos de datos y aspectos que requieran revisión posterior.

- Formulen preguntas de análisis concretas a partir de la inspección inicial.

- Cada pregunta debe poder responderse con evidencia obtenida durante el proyecto.

- La etapa debe desarrollarse en 01_inspeccion_inicial.ipynb. Presenten la estructura general, dimensiones, tipos de datos, valores faltantes, duplicados y observaciones iniciales. En esta etapa no se espera tomar decisiones definitivas, sino reunir evidencia para orientar las etapas posteriores.

- La etapa debe desarrollarse en 02_calidad_y_limpieza.ipynb. Para cada decisión de preparación, indiquen la evidencia que la motivó, la acción aplicada y el impacto observado en el dataset.

- Preserven el dataset original sin modificaciones en data/raw/.

- Guarden el resultado final utilizado en data/processed/.

- Registren cada transformación relevante en logs/pipeline_log.csv.

- Expliquen la decisión tomada, su justificación y el efecto observado luego de aplicarla.

- No presenten una decisión de preparación sin evidencia. Por ejemplo, no indiquen solamente que los datos se limpiaron porque estaban mal; expliquen qué se observó, qué acción se aplicó y qué impacto tuvo en el dataset.

- La etapa debe desarrollarse en 03_eda.ipynb. Debe incluir análisis univariado, bivariado y multivariado. Cada visualización debe incluir una interpretación vinculada con una pregunta u objetivo definido por el grupo.

- Interpretar no consiste en describir solamente colores, ejes o valores visibles. Interpretar consiste en explicar qué muestra el resultado en relación con una pregunta u objetivo del proyecto y qué evidencia aporta al análisis.

- La etapa debe desarrollarse en 04_pca.ipynb. Documenten las variables utilizadas, el escalamiento aplicado, la varianza explicada y la interpretación de las componentes obtenidas. PCA no debe presentarse solo como código ejecutado: debe incluir una explicación clara del propósito y del resultado dentro del análisis realizado.

- Las conclusiones deben desarrollarse en 05_conclusiones.ipynb y mantenerse coherentes con el informe final y la aplicación Streamlit. Deben responder a los objetivos y preguntas definidos por el grupo, diferenciando evidencia, interpretación y conclusión.

- Las limitaciones son aspectos del dataset, del proceso o del alcance que restringen lo que puede concluirse. Las mejoras futuras son acciones posibles para ampliar, fortalecer o profundizar el proyecto en una etapa posterior.

- Ejemplo de redacción de limitación: “El alcance de las conclusiones se encuentra condicionado por la información disponible y por las decisiones documentadas durante el proceso.”

- Ejemplo de redacción de mejora futura: “Una mejora futura podría consistir en incorporar información adicional que permita ampliar el alcance del análisis.”

- No presenten una limitación como si fuera un hallazgo.

- La IA puede utilizarse como apoyo para comprender conceptos, revisar código, organizar el trabajo o mejorar la redacción.

- Cada integrante debe poder explicar y defender las decisiones, resultados y conclusiones presentadas.

- No deleguen en IA la comprensión del dataset ni la justificación de decisiones.

- Todo contenido incorporado al proyecto debe ser comprendido, revisado y validado por el grupo.

- Eliminar o imputar valores automáticamente.

- Mostrar gráficos sin interpretación.

- Ejecutar PCA sin explicar variables, escalamiento o resultado.

- Duplicar contenido entre README, informe y Streamlit.

- Subir credenciales, entornos virtuales o archivos innecesarios.

- Entregar enlaces públicos que no funcionan.


---

# Clase 2 — Análisis Univariado

Fuente: Capítulo 4 — La función describe() y los percentiles

## Titulos detectados
- 🎯 Un resumen completo en una sola línea
- 📊 describe()
- 📊 Percentiles
- 🐍 Ejemplo de aplicación
- 💡 Dato curioso
- 🔍 Percentiles en educación estandarizada

## Texto importante
- En pandas, df.describe() devuelve en una sola tabla los estadísticos más importantes de todas las variables numéricas del dataset.

- Cantidad de valores no nulos. Si es menor al total de filas, hay datos faltantes.

- Primer cuartil (Q1): el 25% de los datos está por debajo de este valor.

- Mediana (Q2): el 50% de los datos está por debajo de este valor.

- Tercer cuartil (Q3): el 75% de los datos está por debajo de este valor.

- El percentil p es el valor por debajo del cual se encuentra el p% de los datos.

- El percentil 25 (Q1) significa que el 25% de los valores son menores a ese número.

- El percentil 75 (Q3) significa que el 75% de los valores son menores a ese número.

- Los percentiles permiten ubicar cualquier valor dentro de la distribución sin que los extremos interfieran.

- # Resumen estadístico completo df.describe()

- # Resumen estadístico completo df.describe()

- # Describe de una variable específica df['Age'].describe()

- # Describe de una variable específica df['Age'].describe()

- count 714.000000 mean 29.699118 std 14.526497 min 0.420000 25% 20.125000 50% 28.000000 75% 38.000000 max 80.000000

- count 714.000000 mean 29.699118 std 14.526497 min 0.420000 25% 20.125000 50% 28.000000 75% 38.000000 max 80.000000

- count es 714, no 891 (total de pasajeros). Hay 177 valores faltantes en la columna edad. describe() nos reveló un problema de calidad de datos sin que lo busquemos explícitamente.

- La diferencia entre mean (29.70) y 50% (28.00) confirma lo que vimos antes: la distribución tiene una leve asimetría hacia la derecha.

- El rango intercuartílico va de 20.12 a 38.00, es decir, el 50% central de los pasajeros tenía entre 20 y 38 años.

- El min de 0.42 corresponde a bebés. El max de 80 años nos habla de la amplitud real del dataset.

- describe() no es el punto de llegada, es el punto de partida. Cada número que llama la atención es una pregunta que vale la pena hacerse.

- describe() no es el punto de llegada, es el punto de partida. Cada número que llama la atención es una pregunta que vale la pena hacerse.

- # Percentiles personalizados df['Fare'].describe(percentiles=[0.10, 0.25, 0.50, 0.75, 0.90])

- # Percentiles personalizados df['Fare'].describe(percentiles=[0.10, 0.25, 0.50, 0.75, 0.90])

- Esto permite ajustar el análisis a los percentiles que sean relevantes para el problema. En el caso de tarifas, el percentil 90 nos dice cuánto pagaba el 10% más caro del barco.

- Los exámenes estandarizados no reportan puntajes absolutos, reportan percentiles. Decir que un estudiante está en el percentil 85 significa que superó al 85% de los que rindieron, independientemente del puntaje bruto.

- En las pruebas PISA, los países no se comparan por promedio solamente. Se analiza la distribución completa: un país puede tener una media alta pero una dispersión enorme, lo que indica una brecha educativa profunda entre sus estudiantes. Otro país puede tener una media más baja pero una distribución muy concentrada, lo que indica mayor equidad.

- Sin percentiles y medidas de dispersión, esa diferencia sería invisible.


---

# Proyecto Integrador

Fuente: 4. Rúbrica

## Titulos detectados
- 4. Rúbrica

## Texto importante
- Cumplimiento de estructura, trazabilidad y claridad documental — 10 puntos.

- Inspección inicial y comprensión del dataset — 10 puntos.

- Calidad, limpieza y preparación de datos — 20 puntos.

- Análisis exploratorio e interpretación — 25 puntos.

- Comunicación de resultados — 10 puntos.

- Defensa oral y dominio conceptual — 15 puntos.

- Cada integrante responderá una pregunta individual sobre cualquier etapa, decisión o resultado del proyecto.


---

# Clase 2 — Análisis Univariado

Fuente: Capítulo 5 — Resumen

## Titulos detectados
- ✅ Lo que vimos hoy
- 🔍 Dato curioso

## Texto importante
- A lo largo de esta clase trabajamos con dos familias de estadísticos descriptivos:

- Medidas de tendencia central — responden dónde están concentrados los datos:

- La media es la más usada pero se distorsiona con valores extremos

- La mediana es más robusta ante outliers y asimetría

- La moda es la única aplicable a variables cualitativas

- Medidas de dispersión — responden cuánto se alejan los datos del centro:

- El rango es simple pero sensible a extremos

- El desvío estándar cuantifica la dispersión en las unidades originales

- El IQR describe la dispersión del 50% central sin que los extremos interfieran

- La regla práctica más importante:Cuando media y mediana difieren significativamente, o cuando el desvío estándar es cercano a la media, los datos tienen asimetría o outliers. En esos casos el IQR y la mediana son más representativos que la media y el desvío.

- describe() es la herramienta que concentra todo esto en una sola tabla. Pero su valor está en la lectura, no en la ejecución.

- En la próxima clase vamos a visualizar todo lo que hoy calculamos. Los histogramas y boxplots van a hacer visible la asimetría, los outliers y la dispersión que hoy detectamos con números.

- En análisis de ingresos, es muy común que la media sea mayor que la mediana.

- - La media salarial es más alta - La mediana salarial es más baja

- Esto ocurre porque un grupo reducido de personas con ingresos muy altos eleva el promedio.

- Por eso, los economistas suelen usar la mediana para describir el ingreso “típico” de la población, ya que representa mejor a la mayoría.

- Este mismo fenómeno es el que observamos cuando analizamos datos con outliers o distribuciones asimétricas.


---

# Clase 2 - Desafío

Fuente: Clase 2 - Desafío

## Titulos detectados
- ⚡ Desafío: Interpretar antes que calcular
- 🎯 Objetivo
- 📝 Instrucciones
- ✅ Desafío adicional
- 💡 Importante

## Texto importante
- Aplicar medidas de tendencia central y dispersión sobre un dataset y analizar qué representan los resultados obtenidos.

- 📂 Cargar el dataset: Utilizá el dataset trabajado en clase (por ejemplo Titanic) y cargalo en un DataFrame de Pandas.

- 📂 Cargar el dataset: Utilizá el dataset trabajado en clase (por ejemplo Titanic) y cargalo en un DataFrame de Pandas.

- 📊 Seleccionar una variable numérica: Por ejemplo Age o Fare.

- 📊 Seleccionar una variable numérica: Por ejemplo Age o Fare.

- 🧮 Calcular las siguientes medidas: Media Mediana Moda Desvío estándar Rango Rango intercuartílico (IQR)

- 🔍 Interpretar los resultados (en pocas líneas): ¿La media representa bien a los datos? ¿Por qué? ¿Qué diferencia observás entre media y mediana? ¿Los datos parecen estar muy dispersos o concentrados? ¿Qué medida usarías para describir el “valor típico”? ¿Qué medida usarías para describir la dispersión real?

- 🔍 Interpretar los resultados (en pocas líneas):

- ¿La media representa bien a los datos? ¿Por qué?

- ¿Qué diferencia observás entre media y mediana?

- ¿Los datos parecen estar muy dispersos o concentrados?

- ¿Qué medida usarías para describir el “valor típico”?

- ¿Qué medida usarías para describir la dispersión real?

- Repetí el análisis con otra variable numérica del dataset.

- 👉 Compará los resultados: ¿las mismas medidas siguen siendo representativas?

- Este desafío no es para entregar. Es una práctica para reforzar lo visto en clase.

- En la próxima clase vamos a visualizar estos resultados.

- 🏆 Clave: No alcanza con calcular. Lo importante es interpretar.


---

# Clase 4 — Análisis Bivariado

Fuente: Clase 4 — Análisis Bivariado

## Titulos detectados
- 1. Capítulo 1 — Objetivo y contexto
- 🎯 Objetivo
- 🚀 Comencemos
- 📚 Al final de esta clase vas a poder:

## Texto importante

- Al finalizar esta clase, interpretarás relaciones entre dos variables en un conjunto de datos real. Podrás identificar si una variable influye sobre otra y en qué dirección. Además, tomarás decisiones basadas en patrones observados, no solo en números calculados.

- Ustedes ya saben calcular medias, frecuencias o porcentajes. Pero en la práctica real, un dato aislado no sirve para tomar decisiones. El verdadero valor aparece cuando preguntamos: "¿esto se relaciona con aquello?". Ahí comienza el análisis bivariado. Muchos estudiantes se quedan atrapados en el cálculo. Obtienen una correlación de 0.7 y dicen "está bien". Pero no saben qué implica para el negocio o la investigación. Calcular no es interpretar. Esta clase invierte ese orden: primero preguntamos qué buscamos, después analizamos. Trabajaremos con dos conjuntos clásicos: Titanic e Iris. El primero nos ayuda a entender variables categóricas (clase, supervivencia). El segundo muestra relaciones entre medidas numéricas (pétalos, sépalos). Así podrás trasladar lo aprendido a tus propios datos.

- Identificar si dos variables están relacionadas o son independientes

- Interpretar la fuerza y dirección de una correlación

- Detectar patrones no lineales en nubes de puntos

- Comparar grupos mediante agregaciones sin perder significado práctico

- Decidir qué par de variables merece un análisis más profundo


---

# Clase 4 — Análisis Bivariado

Fuente: 2. Capítulo 2 — Tablas de contingencia

## Titulos detectados
- 2. Capítulo 2 — Tablas de contingencia

## Texto importante

- Tablas de contingencia (Crosstab) para relaciones entre variables categóricas

- Es una tabla de doble entrada que muestra cuántas veces aparecen juntas las categorías de dos variables cualitativas. Permite responder si existe asociación entre ellas, por ejemplo: ¿los clientes de diferentes zonas geográficas tienen preferencias de producto distintas?

- En un estudio de marketing se quiere saber si la clase de un pasajero del Titanic se relaciona con su probabilidad de sobrevivir. Se analizan 891 pasajeros, cruzando la variable "Clase" (1ª, 2ª, 3ª) con "Supervivencia" (0 = No, 1 = Sí). Aunque la clase tiene orden (1ª > 2ª > 3ª), aquí se trata como categoría para ver patrones, no como magnitud continua.

- import pandas as pd df = pd.read_csv('https://raw.githubusercontent.com/pandas-dev/pandas/master/doc/data/titanic.csv') # Tabla de contingencia básica (frecuencias) pd.crosstab(df['Pclass'], df['Survived']) # Con totales y porcentajes por clase pd.crosstab(df['Pclass'], df['Survived'], margins=True, normalize='index')

- import pandas as pd df = pd.read_csv('https://raw.githubusercontent.com/pandas-dev/pandas/master/doc/data/titanic.csv') # Tabla de contingencia básica (frecuencias) pd.crosstab(df['Pclass'], df['Survived']) # Con totales y porcentajes por clase pd.crosstab(df['Pclass'], df['Survived'], margins=True, normalize='index')

- Representación simplificada del resultado

- Frecuencias (No / Sí): 1ª clase: 80 136 2ª clase: 97 87 3ª clase: 372 119 Porcentajes de supervivencia por clase: 1ª clase: 63% 2ª clase: 47% 3ª clase: 24%

- Frecuencias (No / Sí): 1ª clase: 80 136 2ª clase: 97 87 3ª clase: 372 119 Porcentajes de supervivencia por clase: 1ª clase: 63% 2ª clase: 47% 3ª clase: 24%

- ¿Qué significa este resultado?Hay una asociación clara: a menor clase (de 1ª a 3ª), menor porcentaje de supervivencia. El 63% de los pasajeros de 1ª clase sobrevivió, mientras que solo el 24% de 3ª clase lo hizo. La clase de pasaje no es independiente de la supervivencia en estos datos.

- ¿Qué decisión permite tomar?Si se diseñan protocolos de evacuación, se deben priorizar recursos y rutas específicas para grupos con baja supervivencia (ej. 3ª clase). Sin esta tabla, se podría invertir recursos equitativamente y perder oportunidades de salvar más vidas.

- Error común de interpretaciónMirar solo los conteos brutos: ver 372 muertos en 3ª clase y pensar "ahí murió más gente, esa clase es peligrosa". Pero en 3ª clase viajaban muchas más personas (491 vs 216 en 1ª). Lo relevante es la proporción (24% vs 63%).

- Cuándo usarlo: Para explorar si dos variables categóricas están relacionadas entre si.

- Cuándo no usarlo: Si las variables tienen muchas categorías (ej. 20+), la tabla se vuelve difícil de leer. Mejor usar mapas de calor o gráficos de barras agrupadas.

- Limitaciones: No prueba causalidad, solo asociación. Puede ocultar efectos de una tercera variable (ej. edad o género).

- Buenas prácticas: Siempre mostrar porcentajes por fila o columna si los grupos tienen tamaños desiguales. Agregar totales para contexto.

- En tu negocio, cruzas "día de la compra" con "cliente vuelve en menos de 30 días" y ves que los que compran los viernes vuelven el doble. ¿Qué otra variable deberías revisar antes de lanzar más promociones los viernes?


---

# Clase 4 — Análisis Bivariado

Fuente: 3. Capítulo 3 — Correlación y Heatmap

## Titulos detectados
- 3. Capítulo 3 — Correlación y Heatmap

## Texto importante

- Correlación y Heatmap — Análisis de relaciones entre variables numéricas

- La correlación cuantifica cómo dos variables numéricas se mueven juntas. Su coeficiente oscila entre -1 y 1: valores cercanos a 1 indican que al aumentar una variable, la otra también aumenta (relación positiva); cercanos a -1 señalan que al aumentar una, la otra disminuye (relación negativa); valores próximos a 0 sugieren ausencia de relación lineal. El heatmap es un mapa de colores que representa estos coeficientes para múltiples variables a la vez, permitiendo detectar patrones de asociación de un vistazo. Responde a la pregunta: ¿qué variables del conjunto están linealmente relacionadas entre sí?

- Analizaremos el dataset Iris, que contiene medidas de sépalos y pétalos de tres especies de flores. El objetivo es identificar qué características se relacionan entre sí.

- import pandas as pd import seaborn as sns import matplotlib.pyplot as plt from sklearn.datasets import load_iris # Cargar datos iris = load_iris() df = pd.DataFrame(iris.data, columns=iris.feature_names) # Calcular correlaciones matriz_correlacion = df.corr() # Mostrar matriz numérica print("Matriz de correlación:") print(matriz_correlacion) # Visualizar con heatmap plt.figure(figsize=(8, 6)) sns.heatmap(matriz_correlacion, annot=True, # Muestra el número dentro de cada celda cmap='coolwarm', # Rojo: positivo, azul: negativo center=0, # El blanco representa correlación cero square=True, fmt='.2f') plt.title('Heatmap de correlaciones - Dataset Iris') plt.show() # Correlaciones específicas print("\nCorrelación largo sépalo vs ancho sépalo:") print(f"{matriz_correlacion.loc['sepal length (cm)', 'sepal width (cm)']:.3f}")

- import pandas as pd import seaborn as sns import matplotlib.pyplot as plt from sklearn.datasets import load_iris # Cargar datos iris = load_iris() df = pd.DataFrame(iris.data, columns=iris.feature_names) # Calcular correlaciones matriz_correlacion = df.corr() # Mostrar matriz numérica print("Matriz de correlación:") print(matriz_correlacion) # Visualizar con heatmap plt.figure(figsize=(8, 6)) sns.heatmap(matriz_correlacion, annot=True, # Muestra el número dentro de cada celda cmap='coolwarm', # Rojo: positivo, azul: negativo center=0, # El blanco representa correlación cero square=True, fmt='.2f') plt.title('Heatmap de correlaciones - Dataset Iris') plt.show() # Correlaciones específicas print("\nCorrelación largo sépalo vs ancho sépalo:") print(f"{matriz_correlacion.loc['sepal length (cm)', 'sepal width (cm)']:.3f}")

- Representación simplificada de la matriz de correlación

- Largo sépalo Ancho sépalo Largo pétalo Ancho pétalo Largo sépalo 1.00 -0.12 0.87 0.82 Ancho sépalo -0.12 1.00 -0.43 -0.37 Largo pétalo 0.87 -0.43 1.00 0.96 Ancho pétalo 0.82 -0.37 0.96 1.00

- ¿Qué significa este resultado?La correlación de 0.96 entre largo y ancho del pétalo indica una relación positiva muy fuerte: cuando una flor tiene pétalos largos, también tiende a tener pétalos anchos. No son medidas independientes. Por el contrario, el ancho del sépalo muestra correlaciones bajas o negativas con todas las demás variables (máximo 0.37 en valor absoluto), lo que significa que varía de forma casi independiente.

- ¿Qué decisión permite tomar?Si estuvieras construyendo un modelo predictivo (por ejemplo, para clasificar especies de flores), incluir tanto largo como ancho de pétalo sería redundante. Puedes elegir solo una de ellas sin perder capacidad predictiva. Esto simplifica el modelo y evita problemas de multicolinealidad. Si no lo hicieras, el modelo podría volverse inestable y difícil de interpretar.

- Error común de interpretaciónCreer que una correlación de 0.87 entre largo de sépalo y largo de pétalo significa que uno causa al otro. En realidad, la especie de flor (variable no incluida en la matriz) determina ambas medidas. La correlación solo muestra que coexisten, no que una origine la otra.

- Cuándo usarlo: Para explorar relaciones entre muchas variables numéricas antes de modelar; para detectar redundancia entre predictores.

- Cuándo no usarlo: Con variables categóricas (usa tablas de contingencia); cuando la relación esperada es curva .

- Limitaciones: Solo detecta relaciones lineales; valores atípicos extremos pueden distorsionar el coeficiente; con muestras pequeñas (menos de 30) es inestable.

- Buenas prácticas: Complementa el heatmap con gráficos de dispersión para verificar linealidad.

- En el heatmap observas que largo de sépalo se correlaciona 0.87 con largo de pétalo. ¿Qué hipótesis sobre el crecimiento de la flor podrías formular a partir de este hallazgo?

- Si agregaras una nueva variable "área del pétalo" (largo × ancho) y calcularas su correlación con largo de pétalo, ¿esperarías un coeficiente cercano a 1, cercano a 0, o negativo? ¿Por qué?


---

# Clase 4 — Análisis Bivariado

Fuente: 4. Capítulo 4 — Scatter plot con tendencia

## Titulos detectados
- 4. Capítulo 4 — Scatter plot con tendencia

## Texto importante

- Scatter plot con tendencia — Análisis visual de relación entre variables numéricas

- Un scatter plot (gráfico de dispersión) representa cada observación como un punto en un plano, ubicándolo según sus valores en dos variables numéricas. La línea de tendencia resume el patrón general de esos puntos. Esta herramienta responde: ¿cómo se comporta una variable cuando la otra aumenta o disminuye? Permite identificar dirección (positiva/negativa), forma (lineal o no) e intensidad de la relación, sin necesidad de cálculos complejos.

- Analizamos el dataset Iris (150 flores) para responder: ¿el largo del sépalo (cáliz) se relaciona con el largo del pétalo? En el código, cada flor es un punto. La línea roja discontinua muestra la tendencia general.

- import pandas as pd import matplotlib.pyplot as plt import numpy as np from sklearn.datasets import load_iris # Cargar datos iris = load_iris() df = pd.DataFrame(iris.data, columns=iris.feature_names) # Crear scatter plot con tendencia plt.figure(figsize=(10, 6)) plt.scatter(df['sepal length (cm)'], df['petal length (cm)'], alpha=0.6, s=100, color='steelblue', edgecolors='black') # Calcular línea de tendencia (regresión lineal) z = np.polyfit(df['sepal length (cm)'], df['petal length (cm)'], 1) p = np.poly1d(z) x_line = np.linspace(df['sepal length (cm)'].min(), df['sepal length (cm)'].max(), 100) plt.plot(x_line, p(x_line), "r--", linewidth=2.5, label='Tendencia') plt.xlabel('Largo del Sépalo (cm)') plt.ylabel('Largo del Pétalo (cm)') plt.title('Relación entre largo del sépalo y largo del pétalo') plt.legend() plt.grid(True, alpha=0.3) plt.show() # Medir intensidad de la relación correlacion = df['sepal length (cm)'].corr(df['petal length (cm)']) print(f"Correlación: {correlacion:.4f}") print(f"Ecuación de tendencia: petalo = {z[0]:.4f} * sepalo + {z[1]:.4f}")

- import pandas as pd import matplotlib.pyplot as plt import numpy as np from sklearn.datasets import load_iris # Cargar datos iris = load_iris() df = pd.DataFrame(iris.data, columns=iris.feature_names) # Crear scatter plot con tendencia plt.figure(figsize=(10, 6)) plt.scatter(df['sepal length (cm)'], df['petal length (cm)'], alpha=0.6, s=100, color='steelblue', edgecolors='black') # Calcular línea de tendencia (regresión lineal) z = np.polyfit(df['sepal length (cm)'], df['petal length (cm)'], 1) p = np.poly1d(z) x_line = np.linspace(df['sepal length (cm)'].min(), df['sepal length (cm)'].max(), 100) plt.plot(x_line, p(x_line), "r--", linewidth=2.5, label='Tendencia') plt.xlabel('Largo del Sépalo (cm)') plt.ylabel('Largo del Pétalo (cm)') plt.title('Relación entre largo del sépalo y largo del pétalo') plt.legend() plt.grid(True, alpha=0.3) plt.show() # Medir intensidad de la relación correlacion = df['sepal length (cm)'].corr(df['petal length (cm)']) print(f"Correlación: {correlacion:.4f}") print(f"Ecuación de tendencia: petalo = {z[0]:.4f} * sepalo + {z[1]:.4f}")

- El gráfico muestra nubes de puntos que suben de izquierda a derecha, con puntos concentrados cerca de la línea roja. La correlación de 0.87 (cercana a 1) indica una relación positiva fuerte.

- ¿Qué significa este resultado?Flores con sépalos más largos tienden a tener pétalos más largos. La pendiente (0.75) indica que, en promedio, por cada cm adicional de sépalo, el pétalo aumenta 0.75 cm. Sin embargo, hay variación: dos flores con el mismo sépalo pueden tener pétalos de distinto largo (los puntos no están perfectamente sobre la línea).

- ¿Qué decisión permite tomar?Un agricultor podría usar el largo del sépalo (medible más temprano) como indicador para predecir el tamaño final del pétalo. Si selecciona flores con sépalos > 6.5 cm, esperará pétalos > 5 cm aproximadamente. No hacer esta selección implicaría invertir recursos en flores que probablemente darán pétalos pequeños.

- Error común de interpretaciónCreer que "sépalo largo CAUSA pétalo largo". La correlación no implica causalidad. Podría haber una tercera variable (ej. tiempo de exposición solar, genética compartida) que influya en ambas. El scatter plot solo muestra que varían juntos, no que uno sea causa del otro.

- Cuándo usarlo: Para explorar relaciones entre dos variables numéricas continuas (ej. altura vs peso, inversión vs ganancia).

- Cuándo no usarlo: Con variables categóricas (usar gráfico de barras) o cuando una variable no tiene orden implícito (ej. código postal vs temperatura).

- Limitaciones: Oculta la densidad de puntos si hay muchos solapados (usar transparencia). No detecta relaciones no lineales automáticamente. La pendiente depende de las unidades (no se puede comparar directamente entre estudios con escalas diferentes).

- Buenas prácticas: Siempre mirar el gráfico antes de interpretar la correlación. Si la nube tiene forma de U o curva, la correlación lineal será engañosa (cercana a cero aunque haya relación fuerte pero no lineal).

- Si la correlación entre horas de estudio y calificación fuera 0.2, ¿concluirías que "estudiar más no sirve"? ¿Qué otra posibilidad existe?


---

# Clase 4 — Análisis Bivariado

Fuente: 5. Capítulo 5 — Groupby y Pivot Table

## Titulos detectados
- 5. Capítulo 5 — Groupby y Pivot Table

## Texto importante

- Groupby y Pivot Table — Comparación de Métricas Entre Grupos

- Groupby y pivot table organizan datos numéricos para compararlos entre categorías. Groupby separa filas según una variable categórica (como especie o región) y calcula estadísticos (promedio, suma, conteo) dentro de cada grupo. Pivot table construye una tabla de doble entrada, con una categoría en filas, otra en columnas y la métrica en el centro. Ambos responden: ¿la métrica cambia según el grupo al que pertenece cada observación?

- Un conjunto de datos de flores Iris contiene medidas de sépalo y pétalo para tres especies. Queremos saber si el largo del sépalo varía por especie y si dentro de cada especie hay relación entre tamaño del sépalo y largo del pétalo.

- import pandas as pd # Cargar datos iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv') # 1. Groupby: largo de sépalo promedio por especie sepal_length_mean = iris.groupby('species')['sepal_length'].mean() print(sepal_length_mean) # 2. Crear categoría de tamaño de sépalo (bajo, medio, alto) iris['sepal_category'] = pd.cut(iris['sepal_length'], bins=3, labels=['Pequeño', 'Medio', 'Grande']) # 3. Pivot table: especies vs categoría de sépalo, mostrando largo de pétalo promedio pivot = iris.pivot_table(values='petal_length', index='species', columns='sepal_category', aggfunc='mean') print(pivot)

- import pandas as pd # Cargar datos iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv') # 1. Groupby: largo de sépalo promedio por especie sepal_length_mean = iris.groupby('species')['sepal_length'].mean() print(sepal_length_mean) # 2. Crear categoría de tamaño de sépalo (bajo, medio, alto) iris['sepal_category'] = pd.cut(iris['sepal_length'], bins=3, labels=['Pequeño', 'Medio', 'Grande']) # 3. Pivot table: especies vs categoría de sépalo, mostrando largo de pétalo promedio pivot = iris.pivot_table(values='petal_length', index='species', columns='sepal_category', aggfunc='mean') print(pivot)

- Largo de sépalo promedio por especie: setosa 5.01 cm versicolor 5.94 cm virginica 6.59 cm Largo de pétalo promedio (cm) por especie y categoría de sépalo: species Pequeño Medio Grande setosa 1.462 1.467 NaN versicolor 3.764 4.367 4.800 virginica 4.500 5.309 6.071

- Largo de sépalo promedio por especie: setosa 5.01 cm versicolor 5.94 cm virginica 6.59 cm Largo de pétalo promedio (cm) por especie y categoría de sépalo: species Pequeño Medio Grande setosa 1.462 1.467 NaN versicolor 3.764 4.367 4.800 virginica 4.500 5.309 6.071

- ¿Qué significa este resultado?Las tres especies tienen largos de sépalo diferentes. Setosa es la de sépalo más pequeño (5.01 cm en promedio), virginica la más grande (6.59 cm). Además, dentro de cada especie, las flores con sépalo más grande tienden a tener pétalo más largo: en virginica, el pétalo pasa de 4.50 cm (sépalo pequeño) a 6.07 cm (sépalo grande). El valor "NaN" en setosa indica que no hubo flores con sépalo grande en esa especie.

- ¿Qué decisión permite tomar?Si encuentras una flor nueva y mides su sépalo (ej: 5.2 cm), esperarás un pétalo de aproximadamente 1.46 cm si es setosa, o de ~4.4 cm si es versicolor. La tabla ayuda a construir reglas de clasificación. Consecuencia de no usarla: Usarías un promedio general de pétalo (3.76 cm) que no corresponde bien a ninguna especie, generando errores sistemáticos.

- Error común de interpretaciónCreer que porque el promedio de setosa (5.01 cm) es menor que el de virginica (6.59 cm), no hay solapamiento entre especies. En realidad, el sépalo más largo de setosa es 5.8 cm, y el más corto de virginica es 4.9 cm. Hay zona de traslape (4.9 a 5.8 cm) donde una flor podría ser de cualquiera de las dos. El promedio no cuenta esta ambigüedad.

- Cuándo usarlo: Para responder “¿esta métrica es diferente entre categorías?” (ventas por temporada, tiempos por tratamiento).

- Cuándo no usarlo: Cuando la variable categórica tiene orden implícito con intervalos desiguales (ej: “bajo/medio/alto” no es una magnitud continua; interpretar “aumenta de bajo a medio” puede ser engañoso si los cortes fueron arbitrarios).

- Limitaciones: Solo muestra promedios, no solapamientos entre grupos. Grupos con pocas observaciones generan promedios poco confiables.

- Buenas prácticas: Calcular también desviación estándar y conteo por grupo. Verificar que cada grupo tenga suficiente tamaño muestral.

- Si el promedio de versicolor (5.94 cm) es más cercano al de virginica (6.59) que al de setosa (5.01), ¿eso significa que versicolor se parece más a virginica? ¿Qué otra estadística pedirías para decidir?


---

# Clase 4 — Análisis Bivariado

Fuente: 6. Capítulo 6 — Resumen

## Titulos detectados
- 6. Capítulo 6 — Resumen
- ✅ Lo que vimos hoy
- 📊 Tabla de contingencia (crosstab)
- 📈 Correlación y heatmap
- 📉 Scatter plot con tendencia
- 🏷️ Groupby y pivot table
- 🎯 Regla práctica
- 🧠 Frase de cierre
- 🔗 Conexión próxima clase
- 🔍 Dato aplicado

## Texto importante

- Pasamos del “cómo se calcula” al “qué significa”. Aprendimos a elegir la técnica según el tipo de variable y a interpretar resultados en contexto, no en abstracto.

- Responde: ¿Hay asociación entre dos variables categóricas?

- Muestra frecuencias conjuntas, no porcentajes aislados

- Comparar perfiles de fila (porcentajes internos)

- Si una categoría cambia mucho entre grupos → hay asociación

- Responde: ¿Dos variables numéricas se mueven juntas?

- Correlación ≠ causalidad (siempre preguntar ¿por qué?)

- Cerca de +1 o -1 → relación fuerte (lineal)

- Heatmap: identifica de un vistazo qué pares explorar

- Responde: ¿Cómo es la forma de la relación?

- No lineal: correlación baja pero patrón claro

- Outliers: pueden engañar o revelar casos especiales

- Línea de tendencia: solo si tiene sentido práctico

- Responde: ¿Cómo cambia una métrica entre categorías?

- Comparar promedios, no solo contar casos

- Pivot table = groupby + reordenamiento visual

- Diferencias grandes entre grupos merecen explicación

- Si la pregunta es “¿están relacionados?” → crosstab (categóricas) o correlación (numéricas). Si es “¿cuánto cambia?” → scatter (forma) o groupby (por grupos). El método lo define la pregunta, no la herramienta.

- Saber calcular es útil. Saber interpretar es lo que toma decisiones.

- Veremos cómo detectar relaciones ocultas cuando intervienen más variables. Hoy miramos pares; mañana, redes y condicionamiento.

- Una aerolínea analiza si el tipo de comida a bordo (estándar, premium, vegetariana) influye en la puntuación de limpieza (numérica de 0 a 10). Usan pivot table para comparar promedios y scatter plot para ver tendencia por horas de vuelo. Descubren que la diferencia no es por la comida sino por la duración del vuelo. Sin interpretación, habrían cambiado el menú sin resolver el problema real.


---

# Clase 5 — Análisis multivariado

Fuente: Clase 5 — Análisis multivariado

## Titulos detectados
- 1. Capítulo 1 — Objetivo y contexto
- 🎯 Objetivo
- 🚀 Comencemos
- 📚 Al final de esta clase vas a poder:

## Texto importante
- Al finalizar esta clase, podrás interpretar relaciones entre tres variables numéricas simultáneamente. Decidirás cuál técnica gráfica se ajusta a cada pregunta de negocio o científica. Pasarás de "ver puntos" a "leer historias" en nubes de puntos multivariadas.

- Ustedes ya saben calcular correlaciones y hacer gráficos de dos variables. Pero en datos reales, rara vez todo depende de una sola relación. El problema no es sumar más cálculos, sino que los números no cuentan historias completas.

- Calcular no es interpretar. Puedo obtener una correlación de -0.7 y equivocarme si no veo agrupaciones o valores atípicos. En esta clase entrenamos el ojo analítico: queremos que los datos hablen, no solo que escupamos resultados.

- Trabajaremos con el clásico dataset de pingüinos. Altura de pico, largo de aleta y masa corporal. Tres variables biológicas relacionadas. Veremos cómo agregar información sin perder claridad, y sobre todo, cuándo cada vista es útil para decidir.

- Interpretar una tercera variable usando color y tamaño en 2D

- Comparar patrones diagonales y cruzados en una matriz de dispersión

- Identificar clusters visualmente en un gráfico 3D interactivo

- Seleccionar la mejor visualización según el tipo de pregunta

- Detectar limitaciones de cada enfoque antes de sacar conclusiones


---

# Clase 5 — Análisis multivariado

Fuente: 2. Capítulo 2 — Scatter con hue y size

## Titulos detectados
- 2. Capítulo 2 — Scatter con hue y size

## Texto importante
- Scatter con hue y size — dos formas de agregar una tercera variable a un gráfico 2D

- Un scatter plot básico muestra la relación entre dos variables numéricas (X e Y). Para incorporar una tercera variable (Z) sin añadir un eje, se utilizan dos estrategias visuales: hue (color) y size (tamaño del punto). Hue es ideal cuando Z clasifica los datos en grupos (categorías). Size funciona mejor cuando Z representa una magnitud o cantidad. La pregunta clave que responde este gráfico es: ¿cómo cambia la relación entre X e Y al considerar una tercera dimensión?

- Utilizamos el dataset de pingüinos, que contiene medidas morfológicas de tres especies diferentes. Graficamos la relación entre largo del pico (X) y largo de la aleta (Y). En el primer gráfico, coloreamos según la especie (variable categórica). En el segundo, ajustamos el tamaño del punto según la masa corporal (variable numérica).

- import seaborn as sns import matplotlib.pyplot as plt # Cargar dataset real penguins = sns.load_dataset("penguins").dropna() # Gráfico 1: color por especie fig, axes = plt.subplots(1, 2, figsize=(14, 5)) sns.scatterplot( data=penguins, x="bill_length_mm", # Largo del pico y="flipper_length_mm", # Largo de la aleta hue="species", # Especie (categórica) palette="Set2", alpha=0.8, ax=axes[0] ) axes[0].set_title("hue = especie") # Gráfico 2: tamaño por masa corporal sns.scatterplot( data=penguins, x="bill_length_mm", y="flipper_length_mm", size="body_mass_g", # Masa corporal (numérica) sizes=(20, 300), # Rango de tamaños visibles alpha=0.6, color="steelblue", ax=axes[1] ) axes[1].set_title("size = masa corporal") plt.tight_layout() plt.show()

- import seaborn as sns import matplotlib.pyplot as plt # Cargar dataset real penguins = sns.load_dataset("penguins").dropna() # Gráfico 1: color por especie fig, axes = plt.subplots(1, 2, figsize=(14, 5)) sns.scatterplot( data=penguins, x="bill_length_mm", # Largo del pico y="flipper_length_mm", # Largo de la aleta hue="species", # Especie (categórica) palette="Set2", alpha=0.8, ax=axes[0] ) axes[0].set_title("hue = especie") # Gráfico 2: tamaño por masa corporal sns.scatterplot( data=penguins, x="bill_length_mm", y="flipper_length_mm", size="body_mass_g", # Masa corporal (numérica) sizes=(20, 300), # Rango de tamaños visibles alpha=0.6, color="steelblue", ax=axes[1] ) axes[1].set_title("size = masa corporal") plt.tight_layout() plt.show()

- ¿Qué significa este resultado?En el gráfico con hue (color por especie): los pingüinos se agrupan en tres nubes separadas. La especie Gentoo (verde) aparece en la zona de pico y aleta más largos. Las especies Adelie (naranja) y Chinstrap (azul) muestran cierto solapamiento en largo del pico, pero se diferencian en el largo de la aleta. Esto indica que la especie sí está asociada con diferencias morfológicas medibles.

- En el gráfico con size (tamaño por masa corporal): los puntos más grandes (mayor masa) se concentran en la región superior derecha, donde también hay picos y aletas más largos. Esto sugiere que pingüinos más pesados tienden a tener mayor tamaño en ambas dimensiones.

- ¿Qué decisión permite tomar?Si se necesitara clasificar un pingüino de especie desconocida, medir su pico y aleta sería suficiente para ubicarlo en uno de los tres grupos con alta probabilidad. Esto justifica usar estas variables como predictoras en un modelo de clasificación. No aplicar esta decisión implicaría ignorar información visual valiosa y depender solo de una variable, reduciendo la precisión.

- Error común de interpretaciónConfundir asociación con causalidad: ver que los puntos se separan por color y concluir que "la especie causa el tamaño del pico". El gráfico muestra correlación, no relación causa-efecto. Podría haber otros factores (como la isla de origen o la dieta) que expliquen ambas diferencias.

- Cuándo usarlo: Para explorar si una tercera variable modifica o matiza la relación entre dos variables numéricas.

- Cuándo no usarlo: Cuando la tercera variable tiene más de 6 categorías (el gráfico se satura) o cuando los puntos se superponen demasiado (usar transparencia/alpha).

- Limitaciones: El tamaño del punto puede ser difícil de comparar con precisión; el color requiere buena percepción visual y accesibilidad (daltonismo).

- Buenas prácticas: Usar paletas cualitativas para categorías nominales. Fijar manualmente el rango de tamaños con sizes=(min, max). Incluir siempre leyenda.

- ¿En qué situación usarías hue con una paleta secuencial (como "Blues") en lugar de una cualitativa? Da un ejemplo concreto.

- (Desafío) Si tuvieras que representar cuatro variables en un solo scatter plot 2D, ¿cómo combinarías hue y size? ¿Qué precauciones tomarías para que el gráfico sea interpretable?


---

# Clase 5 — Análisis multivariado

Fuente: 3. Capítulo 3 — Matriz de dispersión (pairplot)

## Titulos detectados
- 3. Capítulo 3 — Matriz de dispersión (pairplot)

## Texto importante
- Matriz de dispersión (pairplot) — todas las relaciones numéricas de una sola vez

- Un pairplot organiza múltiples gráficos en una matriz. En las celdas fuera de la diagonal muestra la relación entre cada par de variables numéricas (scatter plot). En la diagonal muestra la distribución individual de cada variable (histograma o curva de densidad). La matriz es simétrica: la celda fila 1-columna 2 muestra la misma relación que fila 2-columna 1, solo con ejes intercambiados. Este gráfico responde: ¿qué pares de variables se relacionan entre sí y cómo se distribuye cada variable por separado?

- Utilizamos el dataset de pingüinos con cuatro medidas numéricas: largo del pico, profundidad del pico, largo de la aleta y masa corporal. Coloreamos los puntos por especie para ver si las relaciones cambian entre grupos. En la diagonal usamos curvas de densidad para visualizar cómo se distribuye cada medida dentro de cada especie.

- import seaborn as sns import matplotlib.pyplot as plt # Cargar y limpiar dataset penguins = sns.load_dataset("penguins").dropna() # Seleccionar variables numéricas vars_numericas = [ "bill_length_mm", # Largo del pico "bill_depth_mm", # Profundidad del pico "flipper_length_mm", # Largo de aleta "body_mass_g" # Masa corporal ] # Construir matriz de dispersión g = sns.pairplot( data=penguins, vars=vars_numericas, hue="species", # Color por especie diag_kind="kde", # Diagonal: curva de densidad plot_kws={"alpha": 0.6}, diag_kws={"fill": True} ) g.figure.suptitle("Matriz de dispersión — Pingüinos", y=1.02) plt.show()

- import seaborn as sns import matplotlib.pyplot as plt # Cargar y limpiar dataset penguins = sns.load_dataset("penguins").dropna() # Seleccionar variables numéricas vars_numericas = [ "bill_length_mm", # Largo del pico "bill_depth_mm", # Profundidad del pico "flipper_length_mm", # Largo de aleta "body_mass_g" # Masa corporal ] # Construir matriz de dispersión g = sns.pairplot( data=penguins, vars=vars_numericas, hue="species", # Color por especie diag_kind="kde", # Diagonal: curva de densidad plot_kws={"alpha": 0.6}, diag_kws={"fill": True} ) g.figure.suptitle("Matriz de dispersión — Pingüinos", y=1.02) plt.show()

- ¿Qué significa este resultado?En la diagonal (curvas de densidad): la variable "largo de aleta" muestra tres curvas completamente separadas según especie. Esto indica que, solo con esa medida, se puede diferenciar una especie de otra casi sin error. En cambio, "profundidad del pico" tiene las curvas de Adelie y Chinstrap superpuestas, por lo que esa variable sola no basta para distinguirlas.

- En las celdas fuera de la diagonal: la relación entre largo de aleta y masa corporal muestra tres nubes de puntos separadas por color, cada una con tendencia positiva (a mayor masa, aleta más larga). interesante: la relación entre largo del pico y profundidad del pico es negativa dentro de la especie Gentoo (puntos verdes), pero positiva en las otras dos especies. Si se mirara solo la nube completa sin color, la correlación global sería casi nula, ocultando patrones opuestos dentro de cada grupo.

- ¿Qué decisión permite tomar?Si se necesita clasificar pingüinos por especie, conviene priorizar "largo de aleta" y "masa corporal" como predictores, ya que muestran buena separación incluso mirando una variable por vez. En cambio, "profundidad del pico" sería un predictor débil si se usa solo. También revela que no se deben incluir largo y profundidad del pico juntos en un mismo modelo sin considerar la interacción con especie. No revisar el pairplot antes de modelar podría llevar a incluir variables redundantes o mal interpretar relaciones que solo existen al separar por grupos.

- Error común de interpretaciónTratar las celdas simétricas (fila1-col2 y fila2-col1) como dos evidencias independientes. Son exactamente los mismos puntos, solo que con los ejes intercambiados. Otro error: ver una correlación positiva en la nube completa de puntos y asumir que ocurre dentro de cada grupo, cuando podría ser negativa dentro de cada uno (como ocurre con largo vs profundidad del pico).

- Cuándo usarlo: En la fase inicial de exploración de datos, especialmente con 4 a 6 variables numéricas, para identificar correlaciones prometedoras o preocupantes.

- Cuándo no usarlo: Con más de 7 variables (la matriz se vuelve ilegible). Tampoco si hay muchas variables categóricas incluidas como numéricas (ej: códigos de región).

- Limitaciones: No muestra intensidad de correlación numérica (solo patrón visual). Los ejes tienen escalas independientes por columna, impidiendo comparar pendientes entre diferentes filas.

- Buenas prácticas: Usar diag_kind="kde" en lugar de histogramas cuando se colorea por categoría. Eliminar filas con valores faltantes con dropna(). Limitar a variables realmente relevantes para el análisis.

- Imagina que estás analizando datos de viviendas: precio, superficie, antigüedad, distancia al centro y número de habitaciones. ¿Qué patrón en el pairplot te haría sospechar que dos variables están midiendo algo muy similar? ¿Qué harías al respecto?

- (Desafío) ¿Puede ocurrir que en un pairplot sin color (sin hue) dos variables muestren correlación cercana a cero, pero al colorear por una tercera categoría aparezcan correlaciones positivas dentro de cada grupo y negativas dentro de otros? ¿Qué fenómeno estadístico se llama así y por qué es peligroso ignorarlo?


---

# Clase 5 — Análisis multivariado

Fuente: 4. Capítulo 4 — Dispersión 3D con Plotly

## Titulos detectados
- 4. Capítulo 4 — Dispersión 3D con Plotly

## Texto importante
- Dispersión 3D con Plotly — interactivo, se rota, tercera dimensión real

- Un scatter 3D asigna tres variables numéricas continuas a los ejes cartesianos X, Y y Z. A diferencia de hue (color) o size (tamaño), aquí la tercera variable Z ocupa una posición geométrica real. Esto significa que la distancia entre dos puntos en el eje Z es proporcional a la diferencia entre sus valores. La pregunta central es: ¿existe una tercera dimensión cuantitativa que organiza o separa los datos de forma no visible en 2D?

- Utilizamos nuevamente el dataset de pingüinos para comparar directamente con las técnicas anteriores. Graficamos largo del pico (X), profundidad del pico (Y) y largo de aleta (Z). Agregamos color por especie (cuarta dimensión) y tamaño por masa corporal (quinta dimensión). El gráfico es completamente interactivo: se puede rotar, hacer zoom y filtrar haciendo clic en la leyenda.

- import plotly.express as px import seaborn as sns # Cargar y limpiar dataset penguins = sns.load_dataset("penguins").dropna() # Scatter 3D: tres variables numéricas como ejes cartesianos reales fig = px.scatter_3d( penguins, x="bill_length_mm", # Largo del pico y="bill_depth_mm", # Profundidad del pico z="flipper_length_mm", # Largo de aleta (tercer eje real) color="species", # Cuarta dimensión: especie size="body_mass_g", # Quinta dimensión: masa corporal size_max=10, opacity=0.75, title="Morfología de pingüinos en espacio 3D", labels={ "bill_length_mm": "Long. pico (mm)", "bill_depth_mm": "Prof. pico (mm)", "flipper_length_mm": "Long. aleta (mm)" } ) # Ajuste de cámara inicial para mejor perspectiva fig.update_layout( scene_camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)), legend_title_text="Especie" ) fig.show() # Rotar con el mouse fig.write_html("scatter_3d_penguins.html") # Guardar interactivo

- import plotly.express as px import seaborn as sns # Cargar y limpiar dataset penguins = sns.load_dataset("penguins").dropna() # Scatter 3D: tres variables numéricas como ejes cartesianos reales fig = px.scatter_3d( penguins, x="bill_length_mm", # Largo del pico y="bill_depth_mm", # Profundidad del pico z="flipper_length_mm", # Largo de aleta (tercer eje real) color="species", # Cuarta dimensión: especie size="body_mass_g", # Quinta dimensión: masa corporal size_max=10, opacity=0.75, title="Morfología de pingüinos en espacio 3D", labels={ "bill_length_mm": "Long. pico (mm)", "bill_depth_mm": "Prof. pico (mm)", "flipper_length_mm": "Long. aleta (mm)" } ) # Ajuste de cámara inicial para mejor perspectiva fig.update_layout( scene_camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)), legend_title_text="Especie" ) fig.show() # Rotar con el mouse fig.write_html("scatter_3d_penguins.html") # Guardar interactivo

- ¿Qué significa este resultado?Desde la vista inicial, la especie Gentoo (verde) aparece separada hacia valores altos de largo de aleta (eje Z > 210 mm) y largo de pico (eje X > 45 mm). Pero lo importante ocurre al rotar el gráfico. Al girar aproximadamente 90 grados, el solapamiento entre Adelie (naranja) y Chinstrap (rojo) se resuelve: Chinstrap tiene consistentemente mayor largo de pico (X), mientras Adelie tiene mayor profundidad de pico (Y). Este patrón es imposible de ver en cualquier proyección 2D fija de estas tres variables. La interactividad no es un adorno: es el mecanismo que hace visible la estructura tridimensional real.

- Los puntos más grandes (mayor masa corporal) se concentran casi exclusivamente en Gentoo, confirmando que esta especie es más grande en todas las dimensiones.

- ¿Qué decisión permite tomar?Las tres variables numéricas, usadas como coordenadas tridimensionales, separan las tres especies mejor que cualquier par de variables aislado. Esto justifica incluir las tres como predictoras en un modelo de clasificación. También indica que no tiene sentido reducir el problema a solo dos dimensiones si se dispone de estas tres mediciones. No rotar el gráfico y quedarse con una vista fija podría llevar a concluir erróneamente que Adelie y Chinstrap son indistinguibles, cuando en realidad se separan en profundidad.

- Error común de interpretaciónRotar el gráfico hasta encontrar un ángulo donde los clusters se vean muy separados y presentar solo esa captura estática como evidencia, sin mencionar que desde otros ángulos el solapamiento es mayor. La visualización 3D exige reportar la estructura desde múltiples perspectivas, no solo la más favorable para la hipótesis propia. Otro error: asignar una variable categórica al eje Z, lo que destruye el sentido métrico de la distancia.

- Cuándo usarlo: En etapas exploratorias interactivas, con tres variables numéricas continuas donde la relación conjunta es relevante. Ideal para detectar clusters en espacios tridimensionales reales.

- Cuándo no usarlo: En reportes estáticos (PDF, papel impreso) donde la rotación no está disponible. Para audiencias no técnicas, una proyección 2D anotada suele ser más clara.

- Limitaciones: La percepción de profundidad en pantalla plana sigue siendo limitada; puntos traseros pueden ocultarse tras puntos frontales si no se usa transparencia. No es adecuado para más de tres variables métricas como ejes.

- Buenas prácticas: Definir scene_camera para controlar el ángulo inicial. Exportar con write_html() para preservar interactividad. Usar opacity menor a 1. Limitar a máximo cinco dimensiones totales (3 ejes + color + tamaño).

- Un equipo de manufactura tiene tres mediciones por producto: temperatura de proceso, presión aplicada y tasa de defectos. ¿Por qué sería engañoso usar color para representar la tasa de defectos en lugar del eje Z? ¿Qué información se perdería?

- (Desafío) En un scatter 3D interactivo, rotas el gráfico y encuentras un ángulo donde los puntos parecen alinearse en un plano inclinado. Al rotar 180 grados, ese plano desaparece y se ven como nube esférica. ¿Qué implica esto sobre la estructura real de los datos? ¿Cómo decidirías si ese "plano" es real o un artefacto de la perspectiva?


---

# Clase 5 — Análisis multivariado

Fuente: 5. Capítulo 5 — ¿Cuándo usar cada uno?

## Titulos detectados
- 5. Capítulo 5 — ¿Cuándo usar cada uno?

## Texto importante
- ¿Cuándo usar cada uno? — guía de decisión + resumen integrador + caso real

- Elegir una visualización no es una decisión estética sino analítica. La jerarquía de precisión perceptual (posición > longitud > área > color) determina qué canal usar según el tipo de variable. Los ejes X e Y son los más precisos y siempre deben llevar variables numéricas. Un tercer eje Z (3D) mantiene la precisión posicional pero requiere interactividad. Los canales como hue (color) y size (área) son menos precisos y se usan para dimensiones adicionales cuando un eje real no es posible o necesario.

- Comparamos las cuatro técnicas sobre el mismo dataset de pingüinos. Esto permite ver qué revela cada una y cuándo conviene usarla.

- import seaborn as sns import plotly.express as px import matplotlib.pyplot as plt penguins = sns.load_dataset("penguins").dropna() # Técnica 1: Scatter 2D + hue (categórica) fig, axes = plt.subplots(1, 2, figsize=(13, 5)) sns.scatterplot( data=penguins, x="bill_length_mm", y="flipper_length_mm", hue="species", palette="Set2", alpha=0.8, ax=axes[0] ) axes[0].set_title("Scatter + hue (categórica)") # Técnica 2: Scatter 2D + size (magnitud) sns.scatterplot( data=penguins, x="bill_length_mm", y="flipper_length_mm", size="body_mass_g", sizes=(20, 280), alpha=0.6, color="steelblue", ax=axes[1] ) axes[1].set_title("Scatter + size (magnitud)") plt.tight_layout() plt.show() # Técnica 3: Pairplot (exploración multivariada) sns.pairplot( penguins, vars=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"], hue="species", diag_kind="kde", plot_kws={"alpha": 0.6} ) plt.suptitle("Pairplot — todas las relaciones numéricas", y=1.02) plt.show() # Técnica 4: Scatter 3D interactivo fig3d = px.scatter_3d( penguins, x="bill_length_mm", y="bill_depth_mm", z="flipper_length_mm", # Tercera variable como eje real color="species", size="body_mass_g", size_max=10, opacity=0.75, title="Scatter 3D — tres ejes cuantitativos reales" ) fig3d.show()

- import seaborn as sns import plotly.express as px import matplotlib.pyplot as plt penguins = sns.load_dataset("penguins").dropna() # Técnica 1: Scatter 2D + hue (categórica) fig, axes = plt.subplots(1, 2, figsize=(13, 5)) sns.scatterplot( data=penguins, x="bill_length_mm", y="flipper_length_mm", hue="species", palette="Set2", alpha=0.8, ax=axes[0] ) axes[0].set_title("Scatter + hue (categórica)") # Técnica 2: Scatter 2D + size (magnitud) sns.scatterplot( data=penguins, x="bill_length_mm", y="flipper_length_mm", size="body_mass_g", sizes=(20, 280), alpha=0.6, color="steelblue", ax=axes[1] ) axes[1].set_title("Scatter + size (magnitud)") plt.tight_layout() plt.show() # Técnica 3: Pairplot (exploración multivariada) sns.pairplot( penguins, vars=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"], hue="species", diag_kind="kde", plot_kws={"alpha": 0.6} ) plt.suptitle("Pairplot — todas las relaciones numéricas", y=1.02) plt.show() # Técnica 4: Scatter 3D interactivo fig3d = px.scatter_3d( penguins, x="bill_length_mm", y="bill_depth_mm", z="flipper_length_mm", # Tercera variable como eje real color="species", size="body_mass_g", size_max=10, opacity=0.75, title="Scatter 3D — tres ejes cuantitativos reales" ) fig3d.show()

- ¿Qué significa este resultado?Cada técnica responde una pregunta diferente sobre los mismos datos:

- Scatter + hue (especie por color): Muestra que las tres especies forman grupos separados en el espacio pico-aleta. La especie Gentoo queda claramente apartada. Pregunta que responde: ¿la relación entre largo de pico y largo de aleta es diferente según la especie? Respuesta: sí, y los grupos son separables.

- Scatter + size (masa como área): Los puntos más grandes se concentran donde también hay pico y aleta más largos. Pregunta: ¿la masa corporal se asocia con el tamaño morfológico? Respuesta: sí, positivamente.

- Pairplot: Revela un patrón que ningún otro gráfico muestra: la relación entre largo de pico y profundidad de pico es negativa dentro de Gentoo (a mayor largo, menor profundidad), pero positiva dentro de Adelie y Chinstrap. Si solo se mirara el scatter simple sin separar por especie, esta diferencia quedaría oculta. Pregunta: ¿qué pares de variables se relacionan de manera inesperada? Respuesta: ese par específico invierte su correlación según la especie.

- Scatter 3D: Las tres variables numéricas como ejes reales generan clusters tridimensionales separables. Al rotar, se confirma que Chinstrap y Adelie, que en 2D se solapan, se separan en profundidad. Pregunta: ¿existe una estructura tridimensional real que organice los datos? Respuesta: sí, y es invisible en cualquier proyección 2D fija.

- ¿Qué decisión permite tomar?Para un modelo de clasificación de especies, el pairplot indica que no se debe incluir largo de pico y profundidad de pico como predictores independientes sin considerar su interacción con la especie, porque su relación cambia de signo. El scatter 3D sugiere que las tres medidas juntas tienen alta separabilidad. No hacer esta comparación entre técnicas podría llevar a elegir un gráfico por costumbre, perdiendo información crítica como la correlación invertida que solo el pairplot revela.

- Error común de interpretaciónTratar estas técnicas como intercambiables o como versiones "avanzada" y "básica" de un mismo concepto. No lo son: cada una responde una pregunta distinta. Usar scatter 3D cuando la tercera variable es categórica (asignándola al eje Z) destruye el sentido métrico. Usar hue cuando la tercera variable es magnitud continua (como masa corporal) desperdicia la información cuantitativa que size o un eje real podrían preservar.

- Scatter 2D + hue: cuando la tercera variable es categórica (especie, región, segmento). Paleta cualitativa obligatoria.

- Scatter 2D + size: cuando la tercera variable es magnitud numérica (masa, volumen, precio, frecuencia) y no se necesita precisión métrica absoluta.

- Pairplot: en fase exploratoria, con 4 a 6 variables numéricas, antes de formular hipótesis específicas. Ideal para detectar correlaciones inesperadas o relaciones que cambian por subgrupo.

- Scatter 3D (Plotly): solo cuando la tercera variable tiene significado geométrico real, la interactividad está disponible para el lector, y se necesita preservar distancia métrica en el eje Z.

- Limitaciones comunes: El pairplot escala mal (más de 7 variables es ilegible). El scatter 3D en formato estático (PDF, papel) pierde su valor principal —la rotación— y puede ser más confuso que una proyección 2D anotada.

- Buenas prácticas: Comenzar siempre con pairplot en exploración. Documentar por qué se eligió cada técnica. En reportes finales, preferir scatter 2D con hue o size bien anotados sobre capturas estáticas de 3D.

- Una empresa de logística tiene cuatro variables por ruta: distancia (km), tiempo (minutos), costo (USD) y peso de carga (toneladas). Quieren identificar rutas ineficientes. ¿Qué técnica usarías primero y por qué? ¿Qué patrón buscarías en cada gráfico?

- (Desafío) ¿Puede un pairplot con hue revelar una relación que esconde una paradoja de Simpson? Usando el ejemplo de pingüinos, explica cómo el par largo_profundidad del pico ilustra este fenómeno y por qué un scatter 2D simple sin hue llevaría a una conclusión errónea.


---

# Clase 5 — Análisis multivariado

Fuente: 6. Capítulo 6 — Resumen

## Titulos detectados
- 6. Capítulo 6 — Resumen
- ✅ Lo que vimos hoy
- 🔍 Dato aplicado

## Texto importante
- ¿Por qué una sola variable no alcanza? Hoy pasamos del análisis univariado al multivariado. El foco no fue cómo graficar, sino qué nos dice cada gráfico sobre relaciones reales entre variables.

- Scatter con hue y size (2D + 3ra variable)Responde: ¿cómo influye una categoría o magnitud adicional en la relación entre dos variables? Hue → revela agrupamientos o sesgos por categoría Size → muestra impacto de una tercera magnitud Útil cuando la tercera variable es ordinal o categórica

- Hue → revela agrupamientos o sesgos por categoría

- Size → muestra impacto de una tercera magnitud

- Útil cuando la tercera variable es ordinal o categórica

- Matriz de dispersión (pairplot)Responde: ¿qué pares de variables muestran patrones claros y cuáles no? Detecta correlaciones de un vistazo Identifica variables redundantes o poco informativas Orientación inicial antes de modelar

- Identifica variables redundantes o poco informativas

- Orientación inicial antes de modelar

- Dispersión 3D interactiva (Plotly)Responde: ¿cómo se comportan tres variables continuas simultáneamente? Rotar revela ocultamientos por proyección 2D Ideal para clusters o superficies de respuesta No abusar: demasiada información abruma

- Rotar revela ocultamientos por proyección 2D

- Ideal para clusters o superficies de respuesta

- No abusar: demasiada información abruma

- 🎯 Regla práctica: Si la tercera variable es categórica → hue. Si es continua y quiero intuir forma → 3D rotable. Si quiero explorar muchas variables → pairplot. Nunca uses 3D si el patrón ya es claro en 2D con hue.

- “Interpretar es explicar la relación, no nombrar el gráfico.”

- 🔗 Conexión con próxima clase: Veremos cómo cuantificar esas relaciones (correlación) y detectar problemas como multicolinealidad, usando lo observado hoy como guía visual.

- Una cadena de supermercados analizó ventas de frutas por:- temperatura ambiental (x)- precio (y)- día de la semana (hue)Detectaron que los miércoles se vendía más aunque hiciera calor — algo que un scatter 2D simple no mostraba. Ajustaron promociones a días reales, no a temperatura pura. Sin interpretación multivariada, el dato frio “a más calor, más venta” era engañoso.


---

# Clase 6 — Limpieza y preparación de datos

Fuente: Clase 6 — Limpieza y preparación de datos

## Titulos detectados
- 1. Capítulo 1 — Objetivo y contexto
- 🎯 Objetivo
- 🚀 Comencemos
- 📚 Al final de esta clase vas a poder:

## Texto importante

- Al finalizar esta clase, podrás examinar un dataset real, identificar por qué ciertos datos no son confiables o útiles, y decidir qué hacer con ellos. Tu enfoque estará puesto en cómo cada decisión de limpieza afecta las conclusiones que luego podrás extraer.

- Ustedes ya saben calcular medias, varianzas y correlaciones. Pero calcular no es interpretar. En la práctica real, los datos nunca vienen perfectos. Antes de cualquier modelo, debemos responder: ¿estos datos realmente representan lo que queremos analizar?

- Un valor faltante no es solo un vacío técnico. Es una posible distorsión en tu conclusión final. Un outlier no es simplemente un número grande. Es una historia que puede cambiar tu decisión. Esta clase no enseña más fórmulas. Enseña a pensar antes de actuar.

- Trabajaremos con conjuntos reales: pasajeros del Titanic, propinas en restaurantes y precios de diamantes. Cada uno tiene un problema distinto. Juntos aprenderemos a detectar qué necesita atención y, lo más importante, a justificar por qué.

- Identificar si un dato faltante debe eliminarse o imputarse según el contexto del problema

- Diferenciar un outlier real de un error de ingreso sin aplicar fórmulas automáticas

- Decidir entre transformar o no una variable según cómo afecta la interpretación final

- Justificar cada paso de limpieza como una decisión que impacta en el análisis posterior

- Evaluar si un dataset está realmente listo para responder la pregunta original


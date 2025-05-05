import pandas as pd
import matplotlib.pyplot as plt

DB = 'datos_combinados.csv'

# --- Carga de datos ---

# Especifica las columnas que deseas cargar
df = pd.read_csv(DB, encoding='latin1')

# Renombra las columnas para que sean más legibles
df.rename(columns={
    'refPeriodId': 'Year',
    'reporterISO': 'Reporter',
    'flowCode': 'Flow',
    'partnerISO': 'Partner',
    'isOriginalClassification': 'HSCode',
    'fobvalue': 'FOBValue'
}, inplace=True)

# Cambiar los tipos de datos de las columnas
df = df[df['HSCode'] != 'TOTAL']
df['HSCode'] = df['HSCode'].str[:2] # Filtrar solo por capítulo
df['HSCode'] = (df['HSCode'].astype('category'))

df['Year'] = df['Year'].astype('Int32')
df['Reporter'] = df['Reporter'].astype('category')
df['Flow'] = df['Flow'].astype('category')
df['Partner'] = df['Partner'].astype('category')

df['FOBValue'] = df['FOBValue'].astype('float64')

# --- Filtrar por periodos de tiempos y flujos ---

# 1. Importaciones de Colombia de países del EFTA (2006-2010)
imports_2000_2012 = df[
    (df['Flow'] == 'Import') &  # Filtrar importaciones
    (df['Year'] >= 2000) & (df['Year'] <= 2012) # Filtrar años
    & (df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]

# 2. Importaciones de Colombia de países del EFTA (2015-2019)
imports_2013_2022 = df[
    (df['Flow'] == 'Import') &  # Filtrar importaciones
    (df['Year'] >= 2013) & (df['Year'] <= 2022) # Filtrar años
    & (df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]

# 3. Exportaciones de Colombia hacia países del EFTA (2006-2010)
exports_2000_2012 = df[
    (df['Flow'] == 'Export') &  # Filtrar exportaciones
    (df['Year'] >= 2000) & (df['Year'] <= 2012) # Filtrar años
    & (df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]

# 4. Exportaciones de Colombia hacia países del EFTA (2015-2019)
exports_2013_2022 = df[
    (df['Flow'] == 'Export') &  # Filtrar exportaciones
    (df['Year'] >= 2013) & (df['Year'] <= 2022) # Filtrar años
    & (df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]

# --- Agrupación de datos ---

# Volumen total por año
by_year_imports_2000_2012 = imports_2000_2012.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_imports_2013_2022 = imports_2013_2022.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_exports_2000_2012 = exports_2000_2012.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_exports_2013_2022 = exports_2013_2022.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()

# Volumen total por capítulo HS
by_hs_imports_2000_2012 = imports_2000_2012.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_imports_2013_2022 = imports_2013_2022.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_exports_2000_2012 = exports_2000_2012.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_exports_2013_2022 = exports_2013_2022.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()

# --- Visualización de datos ---

# Gráfico de líneas para importaciones (2006-2010 y 2015-2019)
plt.figure(figsize=(10, 6))
plt.plot(by_year_imports_2000_2012['Year'], by_year_imports_2000_2012['FOBValue'], label='Importaciones 2000-2012', marker='o')
plt.plot(by_year_imports_2013_2022['Year'], by_year_imports_2013_2022['FOBValue'], label='Importaciones 2013-2022', marker='o')

# Etiquetas y título
plt.title('Volumen Total de Importaciones por Año', fontsize=14)
plt.xlabel('Año', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Gráfico de líneas para exportaciones (2006-2010 y 2015-2019)
plt.figure(figsize=(10, 6))
plt.plot(by_year_exports_2000_2012['Year'], by_year_exports_2000_2012['FOBValue'], label='Exportaciones 2000-2012', marker='o')
plt.plot(by_year_exports_2013_2022['Year'], by_year_exports_2013_2022['FOBValue'], label='Exportaciones 2013-2022', marker='o')

# Etiquetas y título
plt.title('Volumen Total de Exportaciones por Año', fontsize=14)
plt.xlabel('Año', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Gráfico de barras para importaciones por capítulo HS (2006-2010)
plt.figure(figsize=(12, 6))
plt.bar(by_hs_imports_2000_2012['HSCode'], by_hs_imports_2000_2012['FOBValue'], color='skyblue', label='Importaciones 2000-2012')

# Etiquetas y título
plt.title('Volumen Total de Importaciones por Capítulo HS (2000-2012)', fontsize=14)
plt.xlabel('Capítulo HS', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Gráfico de barras para exportaciones por capítulo HS (2015-2019)
plt.figure(figsize=(12, 6))
plt.bar(by_hs_exports_2013_2022['HSCode'], by_hs_exports_2013_2022['FOBValue'], color='orange', label='Exportaciones 2015-2019')

# Etiquetas y título
plt.title('Volumen Total de Exportaciones por Capítulo HS (2013-2022)', fontsize=14)
plt.xlabel('Capítulo HS', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.show()
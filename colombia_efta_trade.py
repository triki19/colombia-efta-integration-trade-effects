import pandas as pd
import matplotlib.pyplot as plt

DB = 'trade-flow-colombia-efta.csv'

# --- Carga de datos ---

# Especifica las columnas que deseas cargar
columns_to_load = ['refPeriodId', 'reporterISO', 'flowCode', 'partnerISO', 'isOriginalClassification', 'fobvalue']
df = pd.read_csv(DB, encoding='latin1', usecols=columns_to_load)

# Renombra las columnas para que sean más legibles
df.rename(columns={
    'refPeriodId': 'Year',
    'reporterISO': 'Reporter',
    'flowCode': 'Flow',
    'partnerISO': 'Partner',
    'isOriginalClassification': 'HSCode',
    'fobvalue': 'FOBValue'
}, inplace=True)

# Modificar columna HSCode para que contenga solo los dos primeros dígitos
df['HSCode'] = df['HSCode'].str[:2]

# Cambiar los tipos de datos de las columnas
df['Year'] = df['Year'].astype('Int32')
df['Reporter'] = df['Reporter'].astype('category')
df['Flow'] = df['Flow'].astype('category')
df['Partner'] = df['Partner'].astype('category')
df['HSCode'] = df['HSCode'].astype('category')
df['FOBValue'] = df['FOBValue'].astype('float64')

# --- Filtrar por periodos de tiempos y flujos ---

# 1. Importaciones de Colombia de países del EFTA (2006-2010)
imports_2006_2010 = df[
    (df['Flow'] == 'Import') &  # Filtrar importaciones
    (df['Year'] >= 2006) & (df['Year'] <= 2010) # Filtrar años
]

# 2. Importaciones de Colombia de países del EFTA (2015-2019)
imports_2015_2019 = df[
    (df['Flow'] == 'Import') &  # Filtrar importaciones
    (df['Year'] >= 2015) & (df['Year'] <= 2019) # Filtrar años
]

# 3. Exportaciones de Colombia hacia países del EFTA (2006-2010)
exports_2006_2010 = df[
    (df['Flow'] == 'Export') &  # Filtrar exportaciones
    (df['Year'] >= 2006) & (df['Year'] <= 2010) # Filtrar años
]

# 4. Exportaciones de Colombia hacia países del EFTA (2015-2019)
exports_2015_2019 = df[
    (df['Flow'] == 'Export') &  # Filtrar exportaciones
    (df['Year'] >= 2015) & (df['Year'] <= 2019) # Filtrar años
]

# --- Agrupación de datos ---

# General
total_imports_2006_2010 = imports_2006_2010.groupby(['Year', 'Reporter', 'Partner', 'HSCode']).agg({'FOBValue': 'sum'}).reset_index()
total_imports_2015_2019 = imports_2015_2019.groupby(['Year', 'Reporter', 'Partner', 'HSCode']).agg({'FOBValue': 'sum'}).reset_index()
total_exports_2006_2010 = exports_2006_2010.groupby(['Year', 'Reporter', 'Partner', 'HSCode']).agg({'FOBValue': 'sum'}).reset_index()
total_exports_2015_2019 = exports_2015_2019.groupby(['Year', 'Reporter', 'Partner', 'HSCode']).agg({'FOBValue': 'sum'}).reset_index()

# Volumen total por año
by_year_imports_2006_2010 = imports_2006_2010.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_imports_2015_2019 = imports_2015_2019.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_exports_2006_2010 = exports_2006_2010.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_exports_2015_2019 = exports_2015_2019.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()

# Volumen total por capítulo HS
by_hs_imports_2006_2010 = imports_2006_2010.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_imports_2015_2019 = imports_2015_2019.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_exports_2006_2010 = exports_2006_2010.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_exports_2015_2019 = exports_2015_2019.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()

# --- Visualización de datos ---

# Gráfico de líneas para importaciones (2006-2010 y 2015-2019)
plt.figure(figsize=(10, 6))
plt.plot(by_year_imports_2006_2010['Year'], by_year_imports_2006_2010['FOBValue'], label='Importaciones 2006-2010', marker='o')
plt.plot(by_year_imports_2015_2019['Year'], by_year_imports_2015_2019['FOBValue'], label='Importaciones 2015-2019', marker='o')

# Etiquetas y título
plt.title('Volumen Total de Importaciones por Año', fontsize=14)
plt.xlabel('Año', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Gráfico de líneas para exportaciones (2006-2010 y 2015-2019)
plt.figure(figsize=(10, 6))
plt.plot(by_year_exports_2006_2010['Year'], by_year_exports_2006_2010['FOBValue'], label='Exportaciones 2006-2010', marker='o')
plt.plot(by_year_exports_2015_2019['Year'], by_year_exports_2015_2019['FOBValue'], label='Exportaciones 2015-2019', marker='o')

# Etiquetas y título
plt.title('Volumen Total de Exportaciones por Año', fontsize=14)
plt.xlabel('Año', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Gráfico de barras para importaciones por capítulo HS (2006-2010)
plt.figure(figsize=(12, 6))
plt.bar(by_hs_imports_2006_2010['HSCode'], by_hs_imports_2006_2010['FOBValue'], color='skyblue', label='Importaciones 2006-2010')

# Etiquetas y título
plt.title('Volumen Total de Importaciones por Capítulo HS (2006-2010)', fontsize=14)
plt.xlabel('Capítulo HS', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Gráfico de barras para exportaciones por capítulo HS (2015-2019)
plt.figure(figsize=(12, 6))
plt.bar(by_hs_exports_2015_2019['HSCode'], by_hs_exports_2015_2019['FOBValue'], color='orange', label='Exportaciones 2015-2019')

# Etiquetas y título
plt.title('Volumen Total de Exportaciones por Capítulo HS (2015-2019)', fontsize=14)
plt.xlabel('Capítulo HS', fontsize=12)
plt.ylabel('FOB Value (USD)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.show()
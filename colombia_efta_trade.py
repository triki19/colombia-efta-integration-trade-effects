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
imports_to_efta = df[
    (df['Flow'] == 'Import') &  # Filtrar importaciones
    (df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]

# 2. Importaciones de Colombia de países del EFTA (2015-2019)
imports_to_world = df[
    (df['Flow'] == 'Import') &  # Filtrar importaciones
    (~df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]

# 3. Exportaciones de Colombia hacia países del EFTA (2006-2010)
exports_to_efta = df[
    (df['Flow'] == 'Export') &  # Filtrar exportaciones
    (df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]

# 4. Exportaciones de Colombia hacia países del EFTA (2015-2019)
exports_to_world = df[
    (df['Flow'] == 'Export') &  # Filtrar exportaciones
    (~df['Partner'].isin(['Switzerland', 'Norway', 'Iceland'])) # Filtra países EFTA
]
# --- Agrupación de datos ---

# Volumen total por año
by_year_imports_to_efta = imports_to_efta.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_imports_to_world = imports_to_world.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_exports_to_efta = exports_to_efta.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()
by_year_exports_to_world = exports_to_world.groupby(['Year']).agg({'FOBValue': 'sum'}).reset_index()

# Volumen total por capítulo HS
by_hs_imports_to_efta = imports_to_efta.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_imports_to_world = imports_to_world.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_exports_to_efta = exports_to_efta.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()
by_hs_exports_to_world = exports_to_world.groupby(['HSCode']).agg({'FOBValue': 'sum'}).reset_index()

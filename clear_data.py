import pandas as pd
import matplotlib.pyplot as plt
from trade_volume import tests, visualize

# --- Carga de datos ---
DB = 'datos_combinados.csv'
df_trade = pd.read_csv(DB, encoding='latin1')

# --- Limpieza de datos ---

# Renombra las columnas para que sean más legibles
df_trade.rename(columns={
    'refPeriodId': 'Year',
    'reporterISO': 'Reporter',
    'flowCode': 'Flow',
    'partnerISO': 'Partner',
    'isOriginalClassification': 'HSCode',
    'fobvalue': 'FOBValue'
}, inplace=True)

# Eliminar totales y valores para el Mundo
df_trade = df_trade[~df_trade.isin(['TOTAL']).any(axis=1)]

# Filtrar solo por capítulo
df_trade['HSCode'] = df_trade['HSCode'].str[:2]

# Modificar dtypes
df_trade['HSCode'] = (df_trade['HSCode'].astype('category'))
df_trade['Year'] = df_trade['Year'].astype('category')
df_trade['Reporter'] = df_trade['Reporter'].astype('category')
df_trade['Flow'] = df_trade['Flow'].astype('category')
df_trade['Partner'] = df_trade['Partner'].astype('category')
df_trade['FOBValue'] = df_trade['FOBValue'].astype('float64')

# Modificar valores a miles de millones (usd)
df_trade['FOBValue'] /= 1e6

print(df_trade.info())
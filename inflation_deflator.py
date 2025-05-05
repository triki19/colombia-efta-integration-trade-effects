import pandas as pd
from clear_data import df_trade

# --- Cargar índice de precios ---
DB = 'consumer-price-index.csv'
colums_to_load = ['Country Code', '2000', '2002', '2004', '2006', '2008','2010', '2012', '2014', '2016', '2018', '2020', '2022']

df_deflator = pd.read_csv(DB, usecols=colums_to_load)

# --- Limpieza de datos ---
df_deflator = df_deflator[df_deflator['Country Code'] == 'USA'] # Filtrar por Country Code
df_deflator = df_deflator.drop(columns=['Country Code']) # Eliminar la columna Country Code

# Reorganizar los años en una sola columna llamada 'year'
df_deflator = pd.melt(df_deflator, id_vars=[], var_name='Year', value_name='Index')

# --- Calcular deflactor ---
base_year = '2010'
index_base_year = df_deflator[df_deflator['Year'] == base_year]['Index'].iloc[0]

df_deflator['Deflator'] = (df_deflator['Index'] / index_base_year) * 100

# --- Combinar dataframe del comercio con el deflactor de inflación ---

# Convertir columna 'Year' a dtype: str, para compatibilidad
df_deflator['Year'] = df_deflator['Year'].astype(str)
df_trade['Year'] = df_trade['Year'].astype(str)

# Combinar dataframes
df_trade_deflated = pd.merge(df_trade, df_deflator[['Year', 'Deflator']], on='Year', how='left')

# --- Calcular la columna de valor real ---
df_trade_deflated['RealValue'] = df_trade_deflated['FOBValue'] / (df_trade_deflated['Deflator'] / 100)

# Reformatear 'Year' porque me da TOC
df_trade_deflated['Year'] = df_trade_deflated['Year'].astype('category')

# print(df_trade_deflated.info())
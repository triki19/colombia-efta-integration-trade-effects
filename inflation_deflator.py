import pandas as pd
import os

# --- Cargar datos ---
DB_TRADE = '/Data_Processed/trade_cleared.csv'
df_trade = pd.read_csv(DB_TRADE, encoding='latin1')

# --- Cargar índice de precios ---
DB_INDEX = '/Data_Processed/consumer-price-index.csv'
colums_to_load = ['Country Code', '2000', '2002', '2004', '2006', '2008','2010', '2012', '2014', '2016', '2018', '2020', '2022']

df_deflator = pd.read_csv(DB_INDEX, usecols=colums_to_load)

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

# --- Guardar el dataframe con la inflación deflactada ---
def save_deflated_file(df_trade_deflated=df_trade_deflated):
    try:
        if os.path.exists('trade_deflated.csv'):
            user_input = input('El archivo "trade_deflated.csv" ya existe. ¿Desea sobrescribirlo? (s/n): ').strip().lower()

            if user_input == 's':
                os.remove('trade_deflated.csv')
                df_trade_deflated.to_csv('trade_deflated.csv', index=False, encoding='latin1')
                print('El archivo "trade_deflated.csv" se sobrescribió.')
            elif user_input == 'n':
                print('El archivo "trade_deflated.csv" no se sobrescribió.')
            else:
                print('Opción no válida. El archivo "trade_deflated.csv" no se sobrescribió.')

        else:
            user_input = input('El archivo "trade_deflated.csv" no existe. ¿Desea crearlo? (s/n): ').strip().lower()
            if user_input == 's':
                df_trade_deflated.to_csv('trade_deflated.csv', index=False, encoding='latin1')
                print('El archivo "trade_deflated.csv" se creó.')
            else:
                print('El archivo "trade_deflated.csv" no se creó.')

    except Exception as e:
        print(f'Error al guardar el archivo: {e}')

print(df_trade_deflated.info())
save_deflated_file()
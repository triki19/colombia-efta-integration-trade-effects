import pandas as pd
import os

# --- Carga de datos ---
DB = 'Data_Processed/datos_combinados.csv'
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

# Modificar valores a miles de millones (usd)
df_trade['FOBValue'] /= 1e6

# --- Guardar el dataframe limpio ---
def save_cleared_file(df_trade=df_trade):
    try:
        if os.path.exists('Data_Processed/trade_cleared.csv'):
            user_input = input('El archivo "Data_Processed/trade_cleared.csv" ya existe. ¿Desea sobrescribirlo? (s/n): ').strip().lower()

            if user_input == 's':
                os.remove('Data_Processed/trade_cleared.csv')
                df_trade.to_csv('Data_Processed/trade_cleared.csv', index=False, encoding='latin1')
                print('El archivo "Data_Processed/trade_cleared.csv" se sobrescribió.')
            elif user_input == 'n':
                print('El archivo "Data_Processed/trade_cleared.csv" no se sobrescribió.')
            else:
                print('Opción no válida. El archivo "Data_Processed/trade_cleared.csv" no se sobrescribió.')

        else:
            user_input = input('El archivo "Data_Processed/trade_cleared.csv" no existe. ¿Desea crearlo? (s/n): ').strip().lower()
            
            if user_input == 's':
                df_trade.to_csv('Data_Processed/trade_cleared.csv', index=False, encoding='latin1')
                print('El archivo "Data_Processed/trade_cleared.csv" se creó.')
            else:
                print('El archivo "Data_Processed/trade_cleared.csv" no se creó.')
    except Exception as e:
        print(f'Error al guardar el archivo: {e}')

print(df_trade.info())
save_cleared_file()
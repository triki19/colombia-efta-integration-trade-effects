import pandas as pd
import os

# --- 1. Define la lista de archivos ---
lista_archivos = [f for f in os.listdir('.') if f.endswith('.csv')]
columns_to_load = ['refPeriodId', 'reporterISO', 'flowCode', 'partnerISO', 'isOriginalClassification', 'fobvalue']
print(f"Se encontraron los siguientes archivos: {lista_archivos}")

# --- 2. Lee cada archivo y guárdalos en una lista de DataFrames ---
dataframes = [] # Esta lista almacenará cada DataFrame leído

print("Leyendo archivos...")
for archivo in lista_archivos:
    try:
        df_temp = pd.read_csv(archivo, encoding='latin1', usecols=columns_to_load)
        dataframes.append(df_temp)
        print(f"'{archivo}' leído exitosamente. Filas: {len(df_temp)}")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo}' no fue encontrado.")
    except pd.errors.EmptyDataError:
        print(f"Advertencia: El archivo '{archivo}' está vacío y será omitido.")
    except Exception as e:
        print(f"Error al leer el archivo '{archivo}': {e}")


# --- 3. Combina todos los DataFrames en uno solo ---
if dataframes: # Verifica que la lista de dataframes no esté vacía
    print("\nCombinando DataFrames...")
    df_combinado = pd.concat(dataframes, ignore_index=True)

    print("¡Archivos combinados exitosamente!")
    print(f"El DataFrame combinado tiene {len(df_combinado)} filas y {len(df_combinado.columns)} columnas.")

    print("\nPrimeras 5 filas del DataFrame combinado:")
    print(df_combinado.head())

else:
    print("\nNo se encontraron DataFrames para combinar.")

# --- 4. Guardar csv con dataframe combinado ---
nombre_archivo_salida = 'datos_combinados.csv'
try:
    print(f"\nGuardando DataFrame combinado en '{nombre_archivo_salida}'...")
    # index=False evita escribir el índice del DataFrame como una columna en el CSV.
    df_combinado.to_csv(nombre_archivo_salida, index=False)
    print("DataFrame guardado exitosamente.")
except Exception as e:
    print(f"Error al guardar el archivo '{nombre_archivo_salida}': {e}")
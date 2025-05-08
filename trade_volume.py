import pandas as pd
import os


# --- Cargar datos ---
try:

    DB = 'Data_Processed/trade_deflated.csv'
    COLS = ['Year', 'HSCode', 'Partner', 'RealValue', 'Flow']

    df = pd.read_csv(DB, encoding='latin1', usecols=COLS, dtype={
        'Year': 'int32',
        'HSCode': 'str',
        'Flow': 'str',
        'Partner': 'str',
        'RealValue': 'float64',
    })

    print("\nEl DataFrame se cargó con éxito:\n")

except Exception as e:
    print(f"Error reading CSV file: {e}")


# --- Flujo comercial con EFTA ---
try:

    DF_TRADE_FLOW = df[df['HSCode'].str.match(r'^\d{2}$')]

    efta_imports = DF_TRADE_FLOW\
        .query(\
        'Partner in ["Switzerland", "Norway", "Iceland"] and Flow == "Import"'\
        ).reset_index()
    efta_imports = efta_imports.groupby(['Year', 'Partner'])['RealValue'].sum().reset_index()
    
    efta_exports = DF_TRADE_FLOW\
        .query(\
        'Partner in ["Switzerland", "Norway", "Iceland"] and Flow == "Export"'\
        ).reset_index()
    efta_exports = efta_exports.groupby(['Year', 'Partner'])['RealValue'].sum().reset_index()

except Exception as e:
    print(f"Error processing EFTA flows: {e}")


# --- Flujo comercial con principales socios ---
try:

    main_partners_imports = DF_TRADE_FLOW\
        .query(\
        'Partner not in ["Switzerland", "Norway", "Iceland", "World"] and Flow == "Import"'\
        ).reset_index()
    main_partners_imports = main_partners_imports.groupby(['Year', 'Partner'])['RealValue'].sum().reset_index()
    
    main_partners_exports = DF_TRADE_FLOW\
        .query(\
        'Partner not in ["Switzerland", "Norway", "Iceland", "World"] and Flow == "Export"'\
        ).reset_index()
    main_partners_exports = main_partners_exports.groupby(['Year', 'Partner'])['RealValue'].sum().reset_index()
    
except Exception as e:
    print(f"Error processing main partners flows: {e}")


# --- Flujo comercial con el mundo ---
try:
    world_imports = DF_TRADE_FLOW\
    .query(\
    'Partner == "World" and Flow == "Import"'\
    ).reset_index()
    world_imports = world_imports.groupby('Year')['RealValue'].sum().reset_index()

    world_exports = DF_TRADE_FLOW\
    .query(\
    'Partner == "World" and Flow == "Export"'\
    ).reset_index()
    world_exports = world_exports.groupby('Year')['RealValue'].sum().reset_index()

    # Restar los flujos de EFTA
    efta_imports_grouped = efta_imports.groupby('Year')['RealValue'].sum().reset_index()
    efta_exports_grouped = efta_exports.groupby('Year')['RealValue'].sum().reset_index()

    world_imports = world_imports.merge(efta_imports_grouped, on='Year', how='left', suffixes=('', '_EFTA'))
    world_imports['RealValue'] = world_imports['RealValue'] - world_imports['RealValue_EFTA']
    world_imports.drop(columns=['RealValue_EFTA'], inplace=True)

    world_exports = world_exports.merge(efta_exports_grouped, on='Year', how='left', suffixes=('', '_EFTA'))
    world_exports['RealValue'] = world_exports['RealValue'] - world_exports['RealValue_EFTA']
    world_exports.drop(columns=['RealValue_EFTA'], inplace=True)

except Exception as e:
    print(f"Error processing world flows: {e}")


# --- Comparación relativa con el comercio mundial ---
try:
    """
    Cuanto representan las importaciones/exportaciones de EFTA y sus socios principales, con relación al Mundo.
    """ 
    # Unir los DataFrames de EFTA con los de importaciones y exportaciones mundiales
    relative_world_imports = world_imports.merge(efta_imports, on='Year', how='left', suffixes=('', '_EFTA'))
    relative_world_imports['EFTAParticipation'] = relative_world_imports['RealValue_EFTA'] / relative_world_imports['RealValue']

    relative_world_exports = world_exports.merge(efta_exports, on='Year', how='left', suffixes=('', '_EFTA'))
    relative_world_exports['EFTAParticipation'] = relative_world_exports['RealValue_EFTA'] / relative_world_exports['RealValue']

    # Unir los DataFrames de los socios principales con los de importaciones y exportaciones mundiales
    relative_world_imports = relative_world_imports.merge(main_partners_imports, on='Year', how='left', suffixes=('', '_MainPartner'))
    relative_world_imports['MainPartnerParticipation'] = relative_world_imports['RealValue_MainPartner'] / relative_world_imports['RealValue']

    relative_world_exports = relative_world_exports.merge(main_partners_exports, on='Year', how='left', suffixes=('', '_MainPartner'))
    relative_world_exports['MainPartnerParticipation'] = relative_world_exports['RealValue_MainPartner'] / relative_world_exports['RealValue']

except Exception as e:
    print(f"Error processing relative comparison: {e}")


# --- Comparación relativa EFTA/Socios principales ---
try:
    """
    Por cada unidad de dolar importada/exportada de EFTA, ¿cuánto se importa/exporta de los principales socios?
    """

    relative_efta_imports = efta_imports.merge(main_partners_imports, on='Year', how='left', suffixes=('', '_MainPartner'))
    relative_efta_imports['MainPartnerParticipation'] = relative_efta_imports['RealValue'] / relative_efta_imports['RealValue_MainPartner']

    relative_efta_exports = efta_exports.merge(main_partners_exports, on='Year', how='left', suffixes=('', '_MainPartner'))
    relative_efta_exports['MainPartnerParticipation'] = relative_efta_exports['RealValue'] / relative_efta_exports['RealValue_MainPartner']

except Exception as e:
    print(f"Error processing relative comparison EFTA/Main Partners: {e}")


# --- Guardar resultados ---
try:
    # Diccionario que asocia nombres de archivos con DataFrames
    dataframes_to_save = {
        'Data_Processed/efta_imports.csv': efta_imports,
        'Data_Processed/efta_exports.csv': efta_exports,
        'Data_Processed/main_partners_imports.csv': main_partners_imports,
        'Data_Processed/main_partners_exports.csv': main_partners_exports,
        'Data_Processed/world_imports.csv': world_imports,
        'Data_Processed/world_exports.csv': world_exports,
        'Data_Processed/relative_efta_imports.csv': relative_efta_imports,
        'Data_Processed/relative_efta_exports.csv': relative_efta_exports,
        'Data_Processed/relative_world_imports.csv': relative_world_imports,
        'Data_Processed/relative_world_exports.csv': relative_world_exports,
    }

    # Crear el directorio si no existe
    if not os.path.exists('Data_Processed'):
        os.makedirs('Data_Processed')

    # Guardar cada DataFrame en su archivo correspondiente
    for file, dataframe in dataframes_to_save.items():

        if os.path.exists(file):
            user_input = input(f"El archivo {file} ya existe. ¿Desea sobreescribirlo? (s/n): ").strip().lower()
            if user_input == 's':
                os.remove(file)
                dataframe.to_csv(file, index=False)
                print(f"El archivo {file} se ha sobreescrito.")
            else:
                print(f"El archivo {file} no se ha modificado.")

        else:
            dataframe.to_csv(file, index=False)
            print(f"El archivo {file} se ha guardado.")

except Exception as e:
    print(f"Error saving results: {e}")
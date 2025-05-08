import pandas as pd


# --- Cargar datos ---
DB = 'Data_Processed/trade_deflated.csv'
COLS = {
    'Year': 'int32',
    'Partner': 'str',
    'Flow': 'str',
    'HSCode': 'str',
    'RealValue': 'float64'
}

try:

    df = pd.read_csv(DB, encoding='latin1',
                    usecols=COLS.keys(),
                    dtype=COLS
                    )
    print("\nEl DataFrame se cargó con éxito:\n")

except Exception as e:
    print(f"Error reading CSV file: {e}")

# --- Variables globales ---
SECTORS = df[df['HSCode'].str.match(r'^\d{2}$')].reset_index(drop=True)
INDUSTRIES = df[df['HSCode'].str.match(r'^\d{4}$')].reset_index(drop=True)
PRODUCTS = df[df['HSCode'].str.match(r'^\d{6}$')].reset_index(drop=True)


# 1. Sectores, industrias y productos más importantes para el Mundo
# 1.1a Sectores de importación
def world_sectors():
    try:
        efta_import_sectors = SECTORS.query('Flow == "Import" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        world_import_sectors = SECTORS.query('Flow == "Import"')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        world_import_sectors = world_import_sectors\
            .merge(efta_import_sectors, on=['Year', 'HSCode'],
            how='left', suffixes=('', '_EFTA')).fillna(0)
        
        world_import_sectors['RealValue'] =\
            world_import_sectors['RealValue'] - world_import_sectors['RealValue_EFTA']
        
        temp = []
        for year, group in world_import_sectors.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        world_import_sectors = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 1.1b Sectores de exportación
    try:
        efta_export_sectors = SECTORS.query('Flow == "Export" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        world_export_sectors = SECTORS.query('Flow == "Export"')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        world_export_sectors = world_export_sectors\
            .merge(efta_export_sectors, on=['Year', 'HSCode'],
            how='left', suffixes=('', '_EFTA')).fillna(0)
        
        world_export_sectors['RealValue'] =\
            world_export_sectors['RealValue'] - world_export_sectors['RealValue_EFTA']
        
        temp = []
        for year, group in world_export_sectors.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        world_export_sectors = pd.concat(temp).reset_index(drop=True)

        return world_import_sectors, world_export_sectors

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

# 1.2a Industrias de importación
def world_industries():
    try:
        efta_import_industries = INDUSTRIES.query('Flow == "Import" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        world_import_industries = INDUSTRIES.query('Flow == "Import"')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        world_import_industries = world_import_industries\
            .merge(efta_import_industries, on=['Year', 'HSCode'],
            how='left', suffixes=('', '_EFTA')).fillna(0)
        
        world_import_industries['RealValue'] =\
            world_import_industries['RealValue'] - world_import_industries['RealValue_EFTA']
        
        temp = []
        for year, group in world_import_industries.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        world_import_industries = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 1.2b Industrias de exportación
    try:
        efta_export_industries = INDUSTRIES.query('Flow == "Export" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        world_export_industries = INDUSTRIES.query('Flow == "Export"')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        world_export_industries = world_export_industries\
            .merge(efta_export_industries, on=['Year', 'HSCode'],
            how='left', suffixes=('', '_EFTA')).fillna(0)
        
        world_export_industries['RealValue'] =\
            world_export_industries['RealValue'] - world_export_industries['RealValue_EFTA']
        
        temp = []
        for year, group in world_export_industries.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        world_export_industries = pd.concat(temp).reset_index(drop=True)

        return world_import_industries, world_export_industries

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

# 1.3a Productos de importación
def world_products():
    try:
        efta_import_products = PRODUCTS.query('Flow == "Import" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        world_import_products = PRODUCTS.query('Flow == "Import"')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        world_import_products = world_import_products\
            .merge(efta_import_products, on=['Year', 'HSCode'],
            how='left', suffixes=('', '_EFTA')).fillna(0)
        
        world_import_products['RealValue'] =\
            world_import_products['RealValue'] - world_import_products['RealValue_EFTA']
        
        temp = []
        for year, group in world_import_products.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        world_import_products = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 1.3b Productos de exportación
    try:
        efta_export_products = PRODUCTS.query('Flow == "Export" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        world_export_products = PRODUCTS.query('Flow == "Export"')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        world_export_products = world_export_products\
            .merge(efta_export_products, on=['Year', 'HSCode'],
            how='left', suffixes=('', '_EFTA')).fillna(0)
        
        world_export_products['RealValue'] =\
            world_export_products['RealValue'] - world_export_products['RealValue_EFTA']
        
        temp = []
        for year, group in world_export_products.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        world_export_products = pd.concat(temp).reset_index(drop=True)

        return world_import_products, world_export_products

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

# 2. Sectores, industrias y productos más importantes para EFTA
# 2.1a Sectores de importación
def efta_sectors():
    try:
        efta_import_sectors = SECTORS.query('Flow == "Import" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        efta_export_sectors = SECTORS.query('Flow == "Export" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        temp = []
        for year, group in efta_import_sectors.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        efta_import_sectors = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 2.1b Sectores de exportación
    try:
        temp = []
        for year, group in efta_export_sectors.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        efta_export_sectors = pd.concat(temp).reset_index(drop=True)

        return efta_import_sectors, efta_export_sectors

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

# 2.2a Industrias de importación
def efta_industries():
    try:
        efta_import_industries = INDUSTRIES.query('Flow == "Import" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        efta_export_industries = INDUSTRIES.query('Flow == "Export" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        temp = []
        for year, group in efta_import_industries.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        efta_import_industries = pd.concat(temp).reset_index(drop=True)
            
    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 2.2b Industrias de exportación
    try:
        temp = []
        for year, group in efta_export_industries.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        efta_export_industries = pd.concat(temp).reset_index(drop=True)

        return efta_import_industries, efta_export_industries

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

# 2.3a Productos de importación
def efta_products():
    try:
        efta_import_products = PRODUCTS.query('Flow == "Import" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        efta_export_products = PRODUCTS.query('Flow == "Export" and Partner in ["Switzerland", "Norway", "Iceland"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        temp = []
        for year, group in efta_import_products.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        efta_import_products = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 2.3b Productos de exportación
    try:
        temp = []
        for year, group in efta_export_products.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        efta_export_products = pd.concat(temp).reset_index(drop=True)

        return efta_import_products, efta_export_products

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")


# 3. Sectores, industrias y productos más importantes para principales socios
# 3.1a Sectores de importación
def main_partners_sectors():
    try:
        main_partners_import_sectors = SECTORS.query('Flow == "Import" and Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        main_partners_export_sectors = SECTORS.query('Flow == "Export" and Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        temp = []
        for year, group in main_partners_import_sectors.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        main_partners_import_sectors = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 3.1b Sectores de exportación
    try:
        temp = []
        for year, group in main_partners_export_sectors.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        main_partners_export_sectors = pd.concat(temp).reset_index(drop=True)

        return main_partners_import_sectors, main_partners_export_sectors

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

# 3.2a Industrias de importación
def main_partners_industries():
    try:
        main_partners_import_industries = INDUSTRIES.query('Flow == "Import" and Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        main_partners_export_industries = INDUSTRIES.query('Flow == "Export" and Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        temp = []
        for year, group in main_partners_import_industries.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        main_partners_import_industries = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 3.2b Industrias de exportación
    try:
        temp = []
        for year, group in main_partners_export_industries.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        main_partners_export_industries = pd.concat(temp).reset_index(drop=True)

        return main_partners_import_industries, main_partners_export_industries

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

# 3.3a Productos de importación
def main_partners_products():
    try:
        main_partners_import_products = PRODUCTS.query('Flow == "Import" and Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()
        
        main_partners_export_products = PRODUCTS.query('Flow == "Export" and Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
            .groupby(['Year', 'HSCode'])['RealValue']\
            .sum().reset_index()

        temp = []
        for year, group in main_partners_import_products.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        main_partners_import_products = pd.concat(temp).reset_index(drop=True)

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")

    # 3.3b Productos de exportación
    try:
        temp = []
        for year, group in main_partners_export_products.groupby('Year'):
            # print(f"Año: {year}\nGrupo: {group}")
            temp.append(group.nlargest(10, 'RealValue'))
        main_partners_export_products = pd.concat(temp).reset_index(drop=True)

        return main_partners_import_products, main_partners_export_products

    except Exception as e:
        print(f"Error calculating world sectors, industries, products: {e}")


"""
TODO: Puedo probar a agrupar por país para EFTA y principales socios
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
""" from trade_volume import world_trade_volume, relative_world_trade_volume,\
efta_trade_volume, efta_relative_trade_volume,\
main_partners_trade_volume
from trade_pattern import world_sectors, world_industries, world_products,\
efta_sectors, efta_industries, efta_products,\
main_partners_sectors, main_partners_industries, main_partners_products """

""" efta_imports, efta_exports = efta_trade_volume()

main_partners_imports, main_partners_exports = main_partners_trade_volume()
main_partners_imports = main_partners_imports.groupby('Year')['RealValue'].sum().reset_index()
main_partners_exports = main_partners_exports.groupby('Year')['RealValue'].sum().reset_index()

world_imports, world_exports = world_trade_volume()
 """

DB = 'Data_Processed/trade_deflated.csv'
DTYPES = {
    'Year': 'str',
    'Partner': 'str',
    'Flow': 'str',
    'HSCode': 'str',
    'RealValue': 'float64'
}
df = pd.read_csv(DB, encoding='latin1', usecols=DTYPES.keys(), dtype=DTYPES)
df = df[df['HSCode'].str.match(r'^\d{2}$')].reset_index(drop=True)

# Se utiliza un transformación logarítmica de la columna RealValue
# para eliminar el ruido de los valores atípicos 
# y poder observar los patrones de los datos
LOG_SCALES = [x for x in np.expm1(range(1,11))]
world = df.query('Partner == "World"').reset_index(drop=True)
world['RealValueLog'] = np.log1p(world['RealValue'])

top_chapters = world.groupby('HSCode', observed=False)['RealValue'].sum().nlargest(10).sort_values(ascending=False).reset_index()
top_chapters = world[world['HSCode'].isin(top_chapters['HSCode'].unique())].reset_index()

class EDA:

    def world_trade():
        try:
            fig, axs = plt.subplots(ncols=2, figsize=(10,14))
            x, y = world['Year'], world['RealValueLog']

            sns.lineplot(x=x, y=y, ax=axs[0])
            axs[0].set_title('Continuidad')

            sns.histplot(x=y, ax=axs[1], kde=True)
            axs[1].set_title('Distribución')
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error en 'world_trade': {e}")

    def hs_chapters():
        try:
            fig, axs = plt.subplots(ncols=2, figsize=(10,14))
            x, y = top_chapters['HSCode'], top_chapters['RealValueLog']

            sns.histplot(x=x, y=y, ax=axs[0])
            axs[0].set_title('Distribución Bivariada')

            sns.boxplot(x=x, y=y, ax=axs[1])
            axs[1].set_title('Comparación de Distribuciones')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error en la hs_chapter: {e}")

EDA.world_trade()
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np

# --- Configuración de datos ---

DB = 'Data_Processed/trade_deflated.csv'
DTYPES = {
    'Year': 'str',
    'Partner': 'str',
    'Flow': 'str',
    'HSCode': 'str',
    'RealValue': 'float64'
}


# --- Variables globales ---
DF= pd.read_csv(DB, encoding='latin1', usecols=DTYPES.keys(), dtype=DTYPES)
DF['RealValue'] = DF['RealValue'] * 1e6
DF['RealValueLog'] = np.log1p(DF['RealValue'])

LOG_SCALES = [x for x in np.expm1(range(1,23))]

# --- Funciones utilitarias
## Agregar por dígitos HS
def aggregate_hs(df: pd.DataFrame, hs:int = 2) -> pd.DataFrame:
    try:
        match hs:
            case 2:
                df = df[df['HSCode'].str.match(r'^\d{2}$')].reset_index(drop=True)
                return df
            case 4:
                df = df[df['HSCode'].str.match(r'^\d{4}$')].reset_index(drop=True)
                return df
            case 6:
                df = df[df['HSCode'].str.match(r'^\d{6}$')].reset_index(drop=True)
                return df
            case _:
                print(f'Opción {hs} inválida. Opciones válidas: 2, 4, 6')
                return 

        return df
    except Exception as e:
        print(f'Error agregando HS: {e}')

## Visualizar gráficos
def visualize(config:str='all') -> None:
    try:
        frames = [Frames.world_bilateral_trade(aggregate_hs(DF))\
                , Frames.efta_bilateral_trade(aggregate_hs(DF))\
                , Frames.mp_bilateral_trade(aggregate_hs(DF))]

        match config:
            case 'all':
                for frame in frames:
                        print(f'\nGraficando: {frame[0]}')
                        EDA.bilateral_trade(frame[0])
                        print(f'\nGraficando: {frame[1]}')
                        EDA.hs_chapters(frame[1])
                        print(f'\nGraficando: {frame[2]}')
                        EDA.hs_chapters(frame[2])
            case 'world':
                EDA.bilateral_trade(frames[0][0])
                EDA.hs_chapters(frames[0][1])
                EDA.hs_chapters(frames[0][2])
                return
            case 'efta':
                EDA.bilateral_trade(frames[1][0])
                EDA.hs_chapters(frames[1][1])
                EDA.hs_chapters(frames[1][2])
                return
            case 'mp':
                EDA.bilateral_trade(frames[2][0])
                EDA.hs_chapters(frames[2][1])
                EDA.hs_chapters(frames[2][2])
                return
            case _:
                print('Opción inválida. Intenta: all, world, efta, mp')
                return               

    except Exception as e:
        print(f'Error graficando: {e}')

# --- Clases ---
## Construcción de gráficas
class EDA:

    def bilateral_trade(df: pd.DataFrame) -> None:
        try:
            fig = plt.figure(figsize=(10,14))
            gs = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
            x, y, hue = df['Year'], df['RealValueLog'], df['Flow']
            ax00 = fig.add_subplot(gs[0, 0])
            ax01 = fig.add_subplot(gs[0, 1])
            ax10 = fig.add_subplot(gs[1, :])

            sns.lineplot(x=x, y=y, hue=hue, ax=ax00)
            ax00.set_title('Continuidad')

            sns.histplot(x=y, hue=hue, multiple='stack', kde=True, ax=ax01)
            ax01.set_title('Distribución de frecuencia')

            sns.boxplot(x=y, hue=hue, ax=ax10)
            ax10.set_title('Distribución por quantiles')
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error en 'world_trade': {e}")

    def hs_chapters(df_top_hs:pd.DataFrame) -> None:
        try:
            fig, axs = plt.subplots(ncols=2, figsize=(10,14))
            x, y, hue = df_top_hs['HSCode'], df_top_hs['RealValueLog'], df_top_hs['Partner']

            sns.histplot(x=x, y=y, hue=hue, ax=axs[0])
            axs[0].set_title('Distribución Bivariada')

            sns.boxplot(x=x, y=y, hue=hue, ax=axs[1])
            axs[1].set_title('Comparación de Distribuciones')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error en la hs_chapter: {e}")

## Filtrado y Agrupación
class Frames:
    def world_bilateral_trade(df:pd.DataFrame) -> tuple:
        """ Se utiliza un transformación logarítmica de la columna RealValue
        para eliminar el ruido de los valores atípicos y poder observar los patrones de los datos. """
        try:
            
            # Comercio bilateral
            world = df.query('Partner == "World"').reset_index(drop=True)

            # Top hs importaciones
            world_top_hs_imports = world.query('Flow == "Import"').reset_index()
            world_top_hs_imports = world_top_hs_imports.groupby(['HSCode'], observed=False)['RealValue']\
                .sum().nlargest(10).reset_index()
            world_top_hs_imports = world[(world['HSCode'].isin(world_top_hs_imports['HSCode'].unique()))\
                                 & (world['Flow'] == 'Import')].reset_index(drop=True)
            
            # Top hs exportaciones
            world_top_hs_exports = world.query('Flow == "Export"').reset_index()
            world_top_hs_exports = world_top_hs_exports.groupby(['HSCode'], observed=False)['RealValue']\
                .sum().nlargest(10).reset_index()
            world_top_hs_exports = world[(world['HSCode'].isin(world_top_hs_exports['HSCode'].unique()))\
                                 & (world['Flow'] == 'Export')].reset_index(drop=True)            

            return world, world_top_hs_imports, world_top_hs_exports
        except Exception as e:
            print(f'Error construyendo world_bilateral_trade: {e}')

    def mp_bilateral_trade(df:pd.DataFrame) -> tuple:
        try:
            # Cual son los diez principales socios
            main_partners = df.query('Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
                .groupby('Partner')['RealValue'].sum().nlargest(5).reset_index()
            
            # Comercio bilateral
            mp_bilateral_trade = df[df['Partner'].isin(main_partners['Partner'].unique())]

            # Top hs importaciones
            mp_top_hs_imports = mp_bilateral_trade.query('Flow == "Import"').reset_index()
            mp_top_hs_imports = mp_top_hs_imports.groupby(['HSCode'], observed=False)['RealValue']\
                .sum().nlargest(10).reset_index()
            mp_top_hs_imports = mp_bilateral_trade[(mp_bilateral_trade['HSCode'].isin(mp_top_hs_imports['HSCode'].unique()))\
                                 & (mp_bilateral_trade['Flow'] == 'Import')].reset_index(drop=True)
            
            # Top hs exportaciones
            mp_top_hs_exports = mp_bilateral_trade.query('Flow == "Export"').reset_index()
            mp_top_hs_exports = mp_top_hs_exports.groupby(['HSCode'], observed=False)['RealValue']\
                .sum().nlargest(10).reset_index()
            mp_top_hs_exports = mp_bilateral_trade[(mp_bilateral_trade['HSCode'].isin(mp_top_hs_exports['HSCode'].unique()))\
                                 & (mp_bilateral_trade['Flow'] == 'Export')].reset_index(drop=True)
            
            return mp_bilateral_trade, mp_top_hs_imports, mp_top_hs_exports
        
        except Exception as e:
            print(f'Error procesando mp_bilateral_trade: {e}')
            return
        
    def efta_bilateral_trade(df:pd.DataFrame) -> tuple:
        try:
            # Comercio bilateral
            efta_bilateral_trade = df.query('Partner in ["Switzerland", "Norway", "Iceland"]')

            # Top hs importaciones
            efta_top_hs_imports = efta_bilateral_trade.query('Flow == "Import"').reset_index()
            efta_top_hs_imports = efta_top_hs_imports.groupby(['HSCode'], observed=False)['RealValue']\
                .sum().nlargest(10).reset_index()
            efta_top_hs_imports = efta_bilateral_trade[(efta_bilateral_trade['HSCode'].isin(efta_top_hs_imports['HSCode'].unique()))\
                                 & (efta_bilateral_trade['Flow'] == 'Import')].reset_index(drop=True)
            
            # Top hs exportaciones
            efta_top_hs_exports = efta_bilateral_trade.query('Flow == "Export"').reset_index()
            efta_top_hs_exports = efta_top_hs_exports.groupby(['HSCode'], observed=False)['RealValue']\
                .sum().nlargest(10).reset_index()
            efta_top_hs_exports = efta_bilateral_trade[(efta_bilateral_trade['HSCode'].isin(efta_top_hs_exports['HSCode'].unique()))\
                                 & (efta_bilateral_trade['Flow'] == 'Export')].reset_index(drop=True)
            
            return efta_bilateral_trade, efta_top_hs_imports, efta_top_hs_exports
        
        except Exception as e:
            print(f'Error procesando efta_bilateral_trade: {e}')
            return
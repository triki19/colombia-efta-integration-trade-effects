import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
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

        print(df['RealValue'].describe())
        return df
    except Exception as e:
        print(f'Error agregando HS: {e}')

DF = aggregate_hs(DF)

# --- Clases ---

## Filtrado y Agrupación
class Frames:
        
    @staticmethod
    def world_bilateral_trade(df:pd.DataFrame) -> tuple:
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

    @staticmethod
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

    @staticmethod    
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
    
    @staticmethod
    def partner_groups(df:pd.DataFrame=DF) -> pd.DataFrame:
        try:
            top_partners = df.query('Partner not in ["Switzerland", "Norway", "Iceland", "World"]')\
                .groupby('Partner')['RealValue']\
                .sum().nlargest(10).index.tolist()
           
            conditions = [df['Partner'] == 'Switzerland',
                          df['Partner'] == 'Norway',
                          df['Partner'] == 'Iceland',
                          df['Partner'] == 'World',
                          df['Partner'].isin(top_partners)]
            choices = ['EFTA', 'EFTA', 'EFTA', 'World', 'Primary']
            
            df['PartnerGroup'] = np.select(conditions, choices, default='Secundary')
            
            return df

        except Exception as e:
            print(f'Error in partner_groups: {e}')
            return pd.DataFrame()

    @staticmethod
    def time_groups(df:pd.DataFrame=None) -> pd.DataFrame:
        try:
            if df is None or df.empty:
                df = Frames.partner_groups()
            if df is None or df.empty:
                raise ValueError('df not passed or partner_groups returned None or empty')
                
            df['Year'] = df['Year'].astype('Int16')

            df_2000_2010 = df[df['Year'] <= 2010].copy().reset_index(drop=True)
            df_2012_2022 = df[df['Year'] >= 2012].copy().reset_index(drop=True)

            df_2000_2010['Year'] = df_2000_2010['Year'].astype('str')
            df_2012_2022['Year'] = df_2012_2022['Year'].astype('str')

            return [df_2000_2010, df_2012_2022]

        except Exception as e:
            print(f'Error in time_groups: {e}')

    @staticmethod
    def yearly_growth_rate(time_groups:list=None, who:str='all') -> pd.DataFrame:
        if time_groups:
            df_2000_2010, df_2012_2022 = time_groups
        else:
            time_groups = Frames.time_groups()
            if time_groups is None:
                raise ValueError('time_groups returned None')
            df_2000_2010, df_2012_2022 = time_groups

        def efta_growth_rate() -> pd.DataFrame:
            try:            
                # Tasa de Crecimiento para EFTA: 2000-2010
                efta_2000_2010 = df_2000_2010.query('PartnerGroup == "EFTA"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                efta_2000_2010['GrowthRate'] = efta_2000_2010.groupby('Flow')['RealValue'].pct_change().fillna(0)
                efta_2000_2010['GrowthRate'] *= 100

                # Tasa de Crecimiento para EFTA: 2012-2022
                efta_2012_2022 = df_2012_2022.query('PartnerGroup == "EFTA"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                efta_2012_2022['GrowthRate'] = efta_2012_2022.groupby('Flow')['RealValue'].pct_change().fillna(0)
                efta_2012_2022['GrowthRate'] *= 100

                return [efta_2000_2010, efta_2012_2022]
            except Exception as e:
                print(f'Error in efta_growth_rate(): {e}')

        def mpp_growth_rate() -> list[pd.DataFrame]:
            try:
                # Tasa de Crecimiento para Secundary Partners: 2000-2010
                mpp_2000_2010 = df_2000_2010.query('PartnerGroup == "Primary"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                mpp_2000_2010['GrowthRate'] = mpp_2000_2010.groupby('Flow')['RealValue'].pct_change().fillna(0)
                mpp_2000_2010['GrowthRate'] *= 100

                # Tasa de Crecimiento para Primary Partners: 2012-2022
                mpp_2012_2022 = df_2012_2022.query('PartnerGroup == "Primary"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                mpp_2012_2022['GrowthRate'] = mpp_2012_2022.groupby('Flow')['RealValue'].pct_change().fillna(0)
                mpp_2012_2022['GrowthRate'] *= 100

                return [mpp_2000_2010, mpp_2012_2022]
            except Exception as e:
                print(f'Error in mpp_growth_rate(): {e}')

        def mps_growth_rate() -> list[pd.DataFrame]:
            try:
                # Tasa de Crecimiento para Secundary Partners: 2000-2010
                mps_2000_2010 = df_2000_2010.query('PartnerGroup == "Secundary"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                mps_2000_2010['GrowthRate'] = mps_2000_2010.groupby('Flow')['RealValue'].pct_change().fillna(0)
                mps_2000_2010['GrowthRate'] *= 100

                # Tasa de Crecimiento para Secundary Partners: 2012-2022
                mps_2012_2022 = df_2012_2022.query('PartnerGroup == "Secundary"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                mps_2012_2022['GrowthRate'] = mps_2012_2022.groupby('Flow')['RealValue'].pct_change().fillna(0)
                mps_2012_2022['GrowthRate'] *= 100

                return [mps_2000_2010, mps_2012_2022]
            except Exception as e:
                print(f'Error in mps_growth_rate(): {e}')

        def world_growth_rate() -> list[pd.DataFrame]:
            try:
                efta_2000_2010, efta_2012_2022 = efta_growth_rate()
                mpp_2000_2010, mpp_2012_2022 = mpp_growth_rate()
                mps_2000_2010, mps_2012_2022 = mps_growth_rate()
                # Tasa de Crecimiento para el Resto del Mundo: 2000-2010
                world_2000_2010 = df_2000_2010.query('PartnerGroup == "World"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                world_2000_2010['RealValue'] -= (efta_2000_2010['RealValue'] + mpp_2000_2010['RealValue'] + mps_2000_2010['RealValue'])
                world_2000_2010['GrowthRate'] = world_2000_2010.groupby('Flow')['RealValue'].pct_change().fillna(0)
                world_2000_2010['GrowthRate'] *= 100

                # Tasa de Crecimiento para el Resto del Mundo: 2012-2022
                world_2012_2022 = df_2012_2022.query('PartnerGroup == "World"').groupby(['Flow', 'Year'])['RealValue'].sum().reset_index()
                world_2012_2022['RealValue'] -= (efta_2012_2022['RealValue'] + mpp_2012_2022['RealValue'] + mps_2012_2022['RealValue'])
                world_2012_2022['GrowthRate'] = world_2012_2022.groupby('Flow')['RealValue'].pct_change().fillna(0)
                world_2012_2022['GrowthRate'] *= 100                 
            
                return [world_2000_2010, world_2012_2022]
            except Exception as e:
                print(f'Error in world_growth_rate(): {e}')


        def all_growth_rates() -> pd.DataFrame:
            try:
                efta1, efta2 = efta_growth_rate()
                mpp1, mpp2 = mpp_growth_rate()
                mps1, mps2 = mps_growth_rate()
                world1, world2 = world_growth_rate()
                frames = [efta1, efta2, mpp1, mpp2,
                          mps1, mps2, world1, world2]
                keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                
                all = pd.concat(frames, keys=keys)
                all.loc['a':'b', 'PartnerGroup'] = 'EFTA'
                all.loc['c':'d', 'PartnerGroup'] = 'Primary'
                all.loc['e':'f', 'PartnerGroup'] = 'Secundary'
                all.loc['g':'h', 'PartnerGroup'] = 'World'

                return all

            except Exception as e:
                print(f'Error in all_growth_rates: {e}')

        match who:
            case 'all':
                return all_growth_rates()
            case 'world':        
                return world_growth_rate()
            case 'mpp':
                return mpp_growth_rate()
            case 'mps':
                return mps_growth_rate()
            case 'efta':
                return efta_growth_rate()
            case _:
                print('Opción inválida. Prueba: world, mpp, mps, efta')
            

## Construcción de gráficas
class EDA:

    def distribution() -> None:
        try:
            df = Frames.partner_groups(DF)

            fig, axs = plt.subplots(nrows=2)
            sns.histplot(x=df['RealValueLog'], hue=df["Flow"], kde=True, ax=axs[0])
            sns.boxplot(x=df['RealValueLog'], hue=df['Flow'], ax=axs[1])

            plt.show()

        except Exception as e:
            print(f"Error en 'world_trade': {e}")

    def growth_rate() -> None:
        try:
            tms1 = Frames.yearly_growth_rate(who='all')
            tms1['GrowthRate'] = np.log1p(tms1['GrowthRate'])
            fig, axs = plt.subplots(nrows=2)
            sns.lineplot(x=tms1['Year'], y=tms1['GrowthRate'], hue=tms1['PartnerGroup'], style=tms1['Flow'], errorbar=None, ax=axs[0])
            sns.boxplot(x=tms1['GrowthRate'], hue=tms1['Flow'])
            plt.show()
        
        except Exception as e:
            print(f'Error in growth_rate: {e}')

    def trade_magnitude() -> None:
        try:
            df = Frames.partner_groups().query('PartnerGroup != "World"')

            fig, ax = plt.subplots()
            sns.lineplot(x=df['Year'], y=df['RealValueLog'], hue=df['PartnerGroup'], style=df['Flow'], errorbar=None)
            ax.set_title('Comparación de Tendencias: 2000-2022')
            plt.show()
        except Exception as e:
            print(f'Error in trade_magniude: {e}')

#EDA.growth_rate()
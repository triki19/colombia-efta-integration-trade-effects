import pandas as pd

def tests(df=None):
    print(df.info())
    print(df.shape())
    print(df.isnull().sum())
    print(df.isna().sum())
    print(df.head())
    print(df.tail())
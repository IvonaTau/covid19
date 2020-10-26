import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


def read():
    df1 = pd.read_csv("CSV/ETH_BTC_USD_2015-08-09_2020-04-04-CoinDesk.csv")
    df1.columns = ['date', 'ETH', 'BTC']
    df1.date = pd.to_datetime(df1.date, dayfirst=True)
    df1.set_index('date', inplace=True)
    
    EOS = pd.read_csv("ICO_coins/EOS_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    IOTA = pd.read_csv("ICO_coins/IOTA_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    LSK = pd.read_csv("ICO_coins/LSK_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    NEO = pd.read_csv("ICO_coins/NEO_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    TRX = pd.read_csv("ICO_coins/tron/TRX_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    ADA = pd.read_csv("ICO_coins/cardano/ADA_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    GOLD = pd.read_csv("CSV/XAU-GOLD_USD_Historical Data_2018-06-06--2020-04-04.csv")
    SP500 = pd.read_csv("CSV/S_P_500_Historical Data_2018-06-06--2020-04-04.csv")
    
    GOLD['Currency'] = GOLD.apply(lambda row:'XAU', axis=1)
    SP500['Currency'] = SP500.apply(lambda row:'SP500', axis=1)
    
    df = EOS.append(IOTA).append(LSK).append(NEO).append(TRX).append(ADA).append(GOLD).append(SP500)
    df.Date = pd.to_datetime(df.Date, dayfirst=True)

    df['Closing Price (USD)'] = df.apply(lambda row: str(row['Closing Price (USD)']).replace(',', ''), axis=1 )
    df['Closing Price (USD)'] = df['Closing Price (USD)'].astype(float)

    tbl = df.pivot_table('Closing Price (USD)', ['Date'], 'Currency')
    tbl=tbl.dropna()
    
    df_all = pd.concat([df1,tbl], join='inner', axis=1)
    
    return df_all


def read_crypto():
    df1 = pd.read_csv("CSV/ETH_BTC_USD_2015-08-09_2020-04-04-CoinDesk.csv")
    df1.columns = ['date', 'ETH', 'BTC']
    df1.date = pd.to_datetime(df1.date, dayfirst=True)
    df1.set_index('date', inplace=True)
    
    EOS = pd.read_csv("ICO_coins/EOS_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    IOTA = pd.read_csv("ICO_coins/IOTA_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    LSK = pd.read_csv("ICO_coins/LSK_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    NEO = pd.read_csv("ICO_coins/NEO_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    TRX = pd.read_csv("ICO_coins/tron/TRX_USD_2018-06-06_2020-04-02-CoinDesk.csv")
    ADA = pd.read_csv("ICO_coins/cardano/ADA_USD_2018-06-06_2020-04-02-CoinDesk.csv")


    
    df = EOS.append(IOTA).append(LSK).append(NEO).append(TRX).append(ADA)
    df.Date = pd.to_datetime(df.Date, dayfirst=True)

    df['Closing Price (USD)'] = df.apply(lambda row: str(row['Closing Price (USD)']).replace(',', ''), axis=1 )
    df['Closing Price (USD)'] = df['Closing Price (USD)'].astype(float)

    tbl = df.pivot_table('Closing Price (USD)', ['Date'], 'Currency')
    tbl=tbl.dropna()
    
    df_all = pd.concat([df1,tbl], join='inner', axis=1)
    
    return df_all

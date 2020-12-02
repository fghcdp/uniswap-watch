import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

config_file = "../status.json"
tx_dir = "../txs/"

def analyse_contract(contract):

    return

status = json.load(open(config_file, "r"))

print(status.keys())
for contract in status['uniswap_contracts']:
    print("\n\n\n")
    print(contract)
    print(contract['contract_address'])
    df = pd.read_csv(tx_dir + contract['contract_address'] + ".csv")
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')

    # Clean garbage rows by selecting token contract
    df = df[df.tokenName == contract['name']]

    # Correct token decimal values
    #df['value'] = df['value'].astype(str).apply(lambda x: x[:-9]).astype(float)
    td = df['tokenDecimal'][0]
    print("Token decimals")
    print(td)
    df['value'] = pd.to_numeric(df['value'].astype(str).apply(lambda x: x[:-td//2]), errors='coerce')/10**(td-td//2)

    
    ## Early skip criteria

    # Require 1 trade per day
    try:
        trade_rate = len(df) / (df['timeStamp'].max() - df['timeStamp'].min()).days
    except Exception as e:
        print(e)
        print("Skipping...")
        continue

    print("Trade Rate: {} trades per day".format(trade_rate))

    if trade_rate < 1:
        continue

    #### CALC STATS #####

    # Increase in volume compared to 6 week moving average
    df2 = df.groupby(pd.Grouper(key='timeStamp', freq='1w'))['value'].sum()
    rollingVol = df2.rolling(6).mean()
    six_week_volume_delta = rollingVol[-1]/rollingVol[-2]-1
    print("{:.2f}% volume increase from rolling average".format(six_week_volume_delta*100))

    # Increase in unique traders compared to 6 week moving average 
    df2 = df.groupby(pd.Grouper(key='timeStamp', freq='1w'))['from'].nunique()
    rollingUniq = df2.rolling(6).mean()
    six_week_uniq_delta = rollingUniq[-1]/rollingUniq[-2]-1
    print(rollingUniq)
    print("{:.2f}% unique traders increase from rolling average".format(six_week_uniq_delta*100))

    
    input()




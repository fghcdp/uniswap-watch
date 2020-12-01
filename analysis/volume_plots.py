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

    print("heighest")
    print(df['value'].idxmax())
    print(df.iloc[df['value'].idxmax()])

    df2 = df.groupby(pd.Grouper(key='timeStamp', freq='1M'))['value'].sum()
    df2.index = df2.index.strftime('%Y-%m-%d')
    
    fig, ax = plt.subplots(figsize=(20,10))
    print("DF2")
    print(df2.head())

    ax.bar(df2.index, df2.values)
    fig.autofmt_xdate()

    plt.title("{} Weekly Volume".format(contract['name']))
    plt.savefig("{}.png".format(contract['contract_address']))

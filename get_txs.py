import subprocess
import requests
import time
import argparse
import random
import pickle
import pandas as pd

import get_uni_contracts

# ETHERSCAN API KEY
API_KEY = "F9XFJY5G3GVIS1VQC6WD8N8B5BA9PGN4SU"

def get_uniswap_txs(address, block):

    etherscan_url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock={block}&sort=asc&apikey={API_KEY}'

    while True:
        try:
            etherscan_response = requests.get(etherscan_url).json()
            break
        except Exception as e:
            print(e)
            time.sleep(60)
            continue

    result = etherscan_response['result']

    if len(result) == 0:
        return None

    contract_dataframe = pd.DataFrame()
    contract_dataframe = contract_dataframe.from_dict(result)

    return contract_dataframe



# block = '0'
#
# uniswaps = get_uni.uniswaps
# random.shuffle(uniswaps)
#
# for i, uniswap in enumerate(uniswaps[:1000]):
#     print("Checking {}".format(uniswap['tokenAddress']))
#     contract_dataframe = get_uniswap_txs(uniswap['uniswapContract'], block)
#     print(contract_dataframe)
#     time.sleep(10)
#
#     #
    # tokenMatches.append({'name' : uniswap['tokenAddress'],
    #                      'matches' : matches})

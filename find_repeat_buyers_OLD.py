import subprocess
import requests
import time
import argparse
import random
import pickle
import get_uni

# ETHERSCAN API KEY
API_KEY = "F9XFJY5G3GVIS1VQC6WD8N8B5BA9PGN4SU"

def get_uniswap_txs(address, block):

    etherscan_url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock={block}&sort=asc&apikey={API_KEY}'

    etherscan_response = requests.get(etherscan_url).json()
    result = etherscan_response['result']

    print(len(result))
    if len(result) == 0:
        return

    print(result[0].items())
    matches = []
    select_keys = ['tokenName', 'from', 'to', 'value']

    for i, transaction in enumerate(result):
        for match in matches:
            for key in select_keys:
                if transaction[key] != match[key]:
                    break
            else:
                # print("Matched transaction {}".format(match))
                match['count'] += 1
                break
        else:
            new_match = {}
            for key in select_keys:
                new_match[key] = transaction[key]
            new_match['count'] = 1
            matches.append(new_match)
            # print("New item {}".format(new_match))

    print("------------------------")
    print("{} TOP MATCHES:".format(address))
    matches.sort(key=lambda x: x['count'], reverse=True)

    print("From\t\tTo\t\tAmount\t\tCount")
    for match in matches[:10]:
        print("{}\t{}\t{}\t{}".format(match['from'], match['to'], match['value'], match['count']))

    print("\n\n")

    return matches
block = '0'

uniswaps = get_uni.uniswaps
random.shuffle(uniswaps)

tokenMatches = []
for i, uniswap in enumerate(uniswaps[:1000]):
    # print("Checking Token {}".format(uniswap['name']))
    print("Checking {}".format(uniswap['tokenAddress']))
    matches = get_uniswap_txs(uniswap['uniswapContract'], block)
    if matches is None:
        continue
    #
    # tokenMatches.append({'name' : uniswap['tokenAddress'],
    #                      'matches' : matches})

    tokenMatches.append({'name' : matches[0]['tokenName'],
                         'matches' : matches})

print(len(tokenMatches))

# import pdb; pdb.set_trace()
tokenMatches.sort(key=lambda x: x['matches'][0]['count'], reverse=True)

pickle.dump(tokenMatches, open("token_matches.p", "wb"))

for token in tokenMatches:
    print(token['matches'][0]['count'])

for matches in tokenMatches:
    print("TOKEN : {}".format(matches['name']))
    print("From\t\tTo\t\tAmount\t\tCount")
    for match in matches['matches'][:5]:
        print("{}\t{}\t{}\t{}".format(match['from'], match['to'], match['value'], match['count']))
    print("\n\n")

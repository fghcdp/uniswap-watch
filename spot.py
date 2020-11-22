import subprocess
import requests
import time
import argparse
import random
import get_uni

# ETHERSCAN API KEY
API_KEY = "F9XFJY5G3GVIS1VQC6WD8N8B5BA9PGN4SU"

# Argument parser
#parser = argparse.ArgumentParser("Watch ERC-20 send txs from an address and sound alarms")
#parser.add_argument("-a", "--address", default="0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23", help="Watch address")
#parser.add_argument("-b", "--block", default="1", help="Start block, send txs after this block height will sound the alarm.")
#args = parser.parse_args()

# Linux / Mac(?)
def beep():
    cmd = "mpg123 ./gold_please.mp3"
    for i in range(2):
    #for i in range(3):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(2)
        p.kill()
    print("BEEP")
    return

def get_eth_txn_status(address, block):

    etherscan_url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock={block}&sort=asc&apikey={API_KEY}'

    etherscan_response = requests.get(etherscan_url).json()
    #print(etherscan_response)
    result = etherscan_response['result']

    print(len(result))
    if len(result) == 0:
        return

    for key in result[0].keys():
        print(key, result[0][key])

    matches = []

    select_keys = ['from', 'to', 'value']
    print(len(result))

    for i, transaction in enumerate(result):
        # print("Looking at tx {}".format(i))
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

    #
    #
    #     import pdb; pdb.set_trace()
    #
    #
    #     if etherscan_response['result'][i]['from'] == address:
    #         print("Sending telegram")
    #         details = "\n ".join([etherscan_response['result'][i][key] for key in ["value", "tokenName", "tokenDecimal"]])
    #         telebot.send(details)
    #         print("Sent telegram")
    #         beep()
    #         block = etherscan_response['result'][i]['blockNumber']
    #         block = str(int(block)+1)
    #         print("\n\n\n")
    #
    # return block

#beep()


# address = '0x3c442bab170f19dd40d0b1a405c9d93b088b9332' #args.address
block = '0' #args.block

uniswaps = get_uni.uniswaps
random.shuffle(uniswaps)

tokenMatches = []
for i, uniswap in enumerate(uniswaps[:100]):
    # print("Checking Token {}".format(uniswap['name']))
    print("Checking {}".format(uniswap['tokenAddress']))
    matches = get_eth_txn_status(uniswap['uniswapContract'], block)

    tokenMatches.append({'name' : uniswap['tokenAddress'],
                         'matches' : matches})

tokenMatches.sort(key=lambda x: matches['matches'][0]['count'], reverse=True)

for match in tokenMatches:
    print("TOKEN : {}".format(matches['name']))
    print("From\t\tTo\t\tAmount\t\tCount")
    for match in matches['matches'][:5]:
        print("{}\t{}\t{}\t{}".format(match['from'], match['to'], match['value'], match['count']))
    print("\n\n")
#
# i = 0
# while True:
#     try:
#         i += 1
#         print("{} - Checking {} ERC20 txs above block {}".format(i, address, block))
#         block = get_eth_txn_status("", block)
#         time.sleep(20)
#     except Exception as e:
#         print(e)
#         continue

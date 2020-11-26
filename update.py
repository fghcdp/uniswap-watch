import json
import time
import os
import pandas as pd

import get_txs
import get_uni_contracts

def get_status(stat_file='./status.json'):
    if not os.path.isfile(stat_file):
        with open(stat_file, 'w+') as f:
            status = {
                'up_to_block' : 0,
                'uniswap_contracts' : []
                }
            json.dump(status, f)

    with open(stat_file, 'r') as f:
        status = json.load(f)

    return status

def write_status(status, status_file='./status.json'):
    with open(status_file, 'w') as f:
        json.dump(status, f)
    return


if __name__ == "__main__":
    status = get_status()
    print("Found {} contracts previously synced.".format(len(status['uniswap_contracts']), status['up_to_block']))

    print("Getting live contracts from uniswap factory contract...")
    uniswap_contracts = [] #get_uni_contracts.get_contracts()
    print("Found {} contracts online".format(len(uniswap_contracts)))

    current_contract_addresses = [contract['contract_address'] for contract in status['uniswap_contracts']]

    new_contracts = [contract['contract_address'] for contract in uniswap_contracts if contract['contract_address'] not in current_contract_addresses]
    resp = input("Found {} new contracts... download them first? (y/n)".format(len(new_contracts)))

    if resp == 'y':
        for i, contract_address in enumerate(new_contracts):
            print("Downloading {}/{} - {}".format(i+1, len(new_contracts), contract_address))
            new_contract = {'contract_address' : contract_address}
            transactions = get_txs.get_uniswap_txs(contract_address, status['up_to_block'])

            if transactions is None:
                print("0 transactions to this contract, skipping...\n")
                continue
            else:
                transactions.to_csv("./txs/{}.csv".format(contract_address))
                new_contract['name'] = transactions['tokenName'][0]
                new_contract['last_updated_block'] = transactions['blockNumber'].max()
                status['uniswap_contracts'].append(new_contract)
                print("Saved {} new contract transactions - {}".format(len(transactions), new_contract['name']))

            write_status(status)

            print()

    for contract in [contract for contract in status['uniswap_contracts'] if contract['contract_address'] not in new_contracts]:
        print("Updating transactions for {} - {}".format(contract['name'], contract['contract_address']))
        old_transactions = pd.read_csv("./txs/{}.csv".format(contract['contract_address']))
        new_transactions = get_txs.get_uniswap_txs(contract['contract_address'], contract['last_updated_block'])

        if len(new_transactions) == 10000:
            print("WARNING -- More than 10,000 new txs, increase update frequency?")

        # for new_tx in new_transactions.iterrows():
        #     print(new_tx)
        #     print(new_tx['hash'])
        #     print("uwu")
        #     print(old_transactions['hash'])
        #
        #     if new_tx['hash'] not in old_transactions['hash']:
        #         old_transactions.append(new_tx)
        #
        #     else:
        #         print("WARNING -- Already saved this transaction... Not saving.")

        transactions = pd.concat([old_transactions, new_transactions])
        transactions.to_csv("./txs/{}.csv".format(contract['contract_address']))
        contract['last_updated_block'] = int(transactions['blockNumber'].astype('int').max())
        print("Saved {} new contract transactions {}".format(len(new_transactions), contract['name']))

        print()
        write_status(status)

    print("Done.")

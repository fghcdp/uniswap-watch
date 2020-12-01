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


def update_contract(contract):
    print("Updating transactions for {} - {}".format(contract['name'], contract['contract_address']))
    old_transactions = pd.read_csv("./txs/{}.csv".format(contract['contract_address']))
    transactions = old_transactions

    repeat_downloads = True
    while repeat_downloads:
        repeat_downloads = False
        new_transactions = get_txs.get_uniswap_txs(contract['contract_address'], int(contract['last_updated_block']) + 1)

        if new_transactions is None:
            print("No new transactions found, skipping...")
            return

        if len(new_transactions) == 10000:
            print("WARNING -- More than 10,000 new txs, increase update frequency?")
            print("Repeating update!")
            repeat_downloads = True

        transactions = transactions.append(new_transactions)
        contract['last_updated_block'] = int(transactions['blockNumber'].astype('int').max())
        print("Synced to block {}".format(contract['last_updated_block']))

    transactions.to_csv("./txs/{}.csv".format(contract['contract_address']), index=False)
    print("Saved {} new contract transactions {}".format(len(transactions) - len(old_transactions), contract['name']))

    print()
    write_status(status)
    return

def get_new_contract(contract):
    transactions = get_txs.get_uniswap_txs(contract['contract_address'], 0)

    if transactions is None:
        print("0 transactions to this contract, skipping...\n")
        return
    else:
        transactions.to_csv("./txs/{}.csv".format(contract['contract_address']), index=False)
        contract['name'] = transactions['tokenName'][0]
        contract['last_updated_block'] = transactions['blockNumber'].max()
        status['uniswap_contracts'].append(new_contract)
        print("Saved {} new contract transactions - {}".format(len(transactions), contract['name']))

    if len(transactions) == 10000:
        print("More than 10000 transactions found, downloading more...")
        update_contract(contract)
    else:
        write_status(status)

    return

if __name__ == "__main__":
    status = get_status()
    print("Found {} contracts previously synced.".format(len(status['uniswap_contracts']), status['up_to_block']))

    print("Getting live contracts from uniswap factory contract...")
    uniswap_contracts = get_uni_contracts.get_contracts()
    print("Found {} contracts online".format(len(uniswap_contracts)))

    current_contract_addresses = [contract['contract_address'] for contract in status['uniswap_contracts']]

    new_contracts = [contract['contract_address'] for contract in uniswap_contracts if contract['contract_address'] not in current_contract_addresses]
    resp = input("Found {} new contracts... download them first? (y/n)".format(len(new_contracts)))

    if resp == 'y':
        for i, contract_address in enumerate(new_contracts):
            new_contract = {'contract_address' : contract_address}
            print("Downloading {}/{} - {}".format(i+1, len(new_contracts), contract_address))
            get_new_contract(new_contract)

    for contract in [contract for contract in status['uniswap_contracts'] if contract['contract_address'] not in new_contracts]:
        update_contract(contract)

        # print("Updating transactions for {} - {}".format(contract['name'], contract['contract_address']))
        # old_transactions = pd.read_csv("./txs/{}.csv".format(contract['contract_address']))
        #
        # repeat_downloads = True
        # while repeat_downloads:
        #     repeat_downloads = False
        #     new_transactions = get_txs.get_uniswap_txs(contract['contract_address'], int(contract['last_updated_block']) + 1)
        #
        #     if len(new_transactions) == 10000:
        #         print("WARNING -- More than 10,000 new txs, increase update frequency?")
        #         print("Repeating update!")
        #         repeat_downloads = True
        #
        #     transactions = old_transactions.append(new_transactions)
        #
        # transactions.to_csv("./txs/{}.csv".format(contract['contract_address']), index=False)
        # contract['last_updated_block'] = int(transactions['blockNumber'].astype('int').max())
        # print("Saved {} new contract transactions {}".format(len(new_transactions), contract['name']))
        #
        # print()
        # write_status(status)

    print("Done.")

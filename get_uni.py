from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/6f269a3fc5b84a00a2dfc3f192c3c906'))

abi = [{"name": "NewExchange", "inputs": [{"type": "address", "name": "token", "indexed": True}, {"type": "address", "name": "exchange", "indexed": True}], "anonymous": False, "type": "event"}]

uniswap = w3.eth.contract('0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95', abi=abi)
# tokenName = uniswap.functions.name().call()
events = uniswap.events.NewExchange.createFilter(fromBlock=6627917).get_all_entries()
# print(events)

uniswaps = [{'tokenAddress' : e.args.token,
            'uniswapContract' : e.args.exchange
            }
           for e in events]

# print(token_exchange)
#
# for token, exchange in token_exchange.items():
#     print(token, exchange)

# uniswaps = token_exchange.items()

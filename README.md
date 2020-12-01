# uniswap-watch
Download all ethereum transactions to uniswap contracts, storing them in `txs/` as `csv` files.

## Sync transactions
```
python sync_uniswap_txs.py
```

## Get a list of token - uni_contract pairs:
```
python get_uni_contracts.py
```

# Analytics
* WIP volume plotter 
~[stinky](analysis/0xF173214C720f58E03e194085B1DB28B50aCDeeaD.png)

# Monitoring todo
* Sort by hourly increase in volume
* Sort by new addresses today
* Recreate find_repeat_buys.py to try spot repeat traders (same amounts? from same address?), frontrun possible?
* Track options contracts, check for arbitrage opportunities

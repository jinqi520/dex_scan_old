import sqlite3
import threading
from scan_util import scanutil
from web3 import Web3, HTTPProvider
from time import sleep


def save_token(token_address, index, chain, pair_contract):
    cx = sqlite3.connect("./token.db")
    c = cx.cursor()
    tokens = c.execute(
        "select ID from token where contract_address = '" + str(token_address) + "' and chain = '" + chain + "'").fetchall()
    if len(tokens) == 0:
        print("save :" + token_address)
        c.execute(
            "insert into token (contract_address, chain, pair_index, done, pair_contract) values ('" +
            token_address + "','" + chain + "'," + str(index) + ", 0, '" + pair_contract + "')")
    cx.commit()
    c.close()
    cx.close()


def scan_old_eth_token(eth_index):
    index = eth_index
    try:
        mainnet_w3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/851f27ac9a6e42f2a76b6dcd14286d24'))
        factory_contract = scanutil.get_uniswap_factory(mainnet_w3)
        if eth_index == 0:
            eth_index = scanutil.get_allpair_len(factory_contract) - 1
        for i in range(0, eth_index):
            index = eth_index - i
            pair_contract = scanutil.get_pair_contract_byindex(factory_contract, index)
            (token0, token1) = scanutil.get_tokens_bypair(mainnet_w3, pair_contract)
            save_token(token0, index, "eth", pair_contract)
            save_token(token1, index, "eth", pair_contract)
            sleep(10)
    except Exception as e:
        print(e)
        scan_old_eth_token(index)


def scan_old_bsc_token(bsc_index):
    index = eth_index
    try:
        mainnet_w3 = Web3(HTTPProvider(
            'https://restless-little-paper.bsc.discover.quiknode.pro/77fac075694faf5935b6f199c38df1a0a5be6c37/'))
        factory_contract = scanutil.get_pancake_factory(mainnet_w3)
        if bsc_index == 0:
            bsc_index = scanutil.get_allpair_len(factory_contract) - 1
        for i in range(0, bsc_index):
            index = bsc_index - i
            pair_contract = scanutil.get_pair_contract_byindex(factory_contract, index)
            (token0, token1) = scanutil.get_tokens_bypair(mainnet_w3, pair_contract)
            save_token(token0, index, "bsc", pair_contract)
            save_token(token1, index, "bsc", pair_contract)
            sleep(10)
    except Exception as e:
        print(e)
        scan_old_bsc_token(index)


if __name__ == "__main__":
    cx = sqlite3.connect("./token.db")
    c = cx.cursor()
    tables = c.execute("select name from sqlite_master where type = 'table'").fetchall()
    eth_index = 0
    bsc_index = 0
    if not tables:
        c.execute(
            '''CREATE TABLE token (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, contract_address TEXT NOT NULL, chain TEXT NOT NULL, pair_index INT NOT NULL, done INT NOT NULL, pair_contract TEXT NOT NULL)''')
    else:
        eth_token = c.execute(
            "select pair_index from token where chain = 'eth' order by pair_index ASC").fetchone()
        bsc_token = c.execute(
            "select pair_index from token where chain = 'bsc' order by pair_index ASC").fetchone()
        if eth_token is not None:
            eth_index = eth_token[0] - 1
        if bsc_token is not None:
            bsc_index = bsc_token[0] - 1
    c.close()
    cx.close()
    t1 = threading.Thread(target=scan_old_eth_token, args=(eth_index,))
    t2 = threading.Thread(target=scan_old_bsc_token, args=(bsc_index,))
    t1.start()
    t2.start()

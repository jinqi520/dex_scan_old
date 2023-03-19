from web3 import Web3, HTTPProvider
from scan_util import scanutil


def get_contract_code(chain, contract_address):
    if chain == "bsc":
        mainnet_w3 = Web3(HTTPProvider(
            'https://restless-little-paper.bsc.discover.quiknode.pro/77fac075694faf5935b6f199c38df1a0a5be6c37/'))
    else:
        mainnet_w3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/851f27ac9a6e42f2a76b6dcd14286d24'))
    address = Web3.toChecksumAddress(contract_address)
    bytecode = mainnet_w3.toHex(mainnet_w3.eth.get_code(address))
    return bytecode


def checkDeliver(chain, contract_address, pair_contract):
    print("扫描deliver模块", contract_address)
    bytecode = get_contract_code(chain, contract_address)
    function_str = "633bd5d173"
    if function_str in bytecode:
        flag = scanutil.if_over_totalsupply(chain, contract_address, pair_contract)
        if flag:
            print("%s链：  合约地址：%s   疑似存在deliver()的安全问题，pair合约地址：%s" % (
                chain, contract_address, pair_contract))
            scanutil.ding_send_text(
                "[chain_poc]" + chain + "：  疑似存在deliver()的安全问题：" + contract_address + " pair合约地址：   " + pair_contract)


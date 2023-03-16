import random
import requests
from web3 import Web3
from eth_abi import encode_abi
from eth_utils import function_signature_to_4byte_selector
from scan_util import scanutil


def randomIP():
    a = random.sample(range(1, 256), 4)
    b = map(str, a)
    return '.'.join(b)


def checkTransfer(chain, contract_address, pair_contract):
    print("扫描transfer模块", contract_address)
    test_account = Web3.toChecksumAddress("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
    balance = scanutil.get_erc20_balance(chain, contract_address, pair_contract)
    if balance == 0:
        return
    fn_selector = function_signature_to_4byte_selector('transfer(address,uint256)')
    ms_data1 = encode_abi(["address", "uint256"],
                          [test_account, balance])
    input_data = Web3.toHex(fn_selector + ms_data1)
    if chain == "eth":
        chain_id = 1
    else:
        chain_id = 56
    result, logs = scanutil.simulat(chain_id, pair_contract, contract_address, input_data)
    if result is None or not result["transaction"]["status"] or logs is None:
        ms_data2 = encode_abi(["address", "uint256"],
                              [Web3.toChecksumAddress(pair_contract), balance // 2])
        input_data2 = Web3.toHex(fn_selector + ms_data2)
        # print(input_data2)
        result, logs = scanutil.simulat(chain_id, pair_contract, contract_address, input_data2)
        if result is None or not result["transaction"]["status"] or logs is None:
            return
        amount = 0
        # print(logs)
        for log in logs:
            if log['raw']['address'] == contract_address.lower() and \
                    log['raw']["topics"][0] == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef" and \
                    log['raw']["topics"][1][26:].lower() == pair_contract[2:].lower() and \
                    log['raw']["topics"][2][26:].lower() != pair_contract[2:].lower():
                amount = amount + Web3.toInt(hexstr=log['raw']["data"])
        # "amount != balance * 2" 是为了排除特殊情况
        if amount > balance // 2 and amount != balance * 2:
            print("%s链：  合约地址：%s   疑似存在transfer收取额外手续费的安全问题，pair合约地址：%s" % (
                chain, contract_address, pair_contract))
            scanutil.ding_send_text(
                "[chain_poc]" + chain + "：  token合约疑似存在转账收取额外手续费的安全问题：" + contract_address + " pair合约地址：   " + pair_contract)
    else:
        amount = 0
        for log in logs:
            if log['raw']['address'] == contract_address.lower() and \
                    log['raw']["topics"][0] == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef" and \
                    log['raw']["topics"][1][26:].lower() == pair_contract[2:].lower() and \
                    log['raw']["topics"][2][26:].lower() == "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266":
                amount = amount + Web3.toInt(hexstr=log['raw']["data"])
        if amount == balance * 2:
            print("%s链：  合约地址：%s   疑似存在transfer错误打印两次event日志的安全问题，pair合约地址：%s" % (
                chain, contract_address, pair_contract))
            scanutil.ding_send_text(
                "[chain_poc]" + chain + "：  疑似存在transfer错误打印两次event日志的安全问题：" + contract_address + " pair合约地址：   " + pair_contract)


if __name__ == "__main__":
    # print(randomIP())
    # eth 0x7800FFF0C88784e83aB23357bBBE53a5f58B439B 0x35944065A706C5436AF45DE884d4a90a5Ddd93E7 0x7794A9BE78684fd8de6Ed65b6c192FF3C37d2D77 0x2725d93ED1A0F9A75FA21183Cd97FFa7642a3586 0xCD56A62CE22dBc5c585C6a3b081C3F68D510a0Dd 0xd7443f8bD9ac5a7E429f809Ae0257792809B901E
    # checkTransfer("eth", "0xd7443f8bD9ac5a7E429f809Ae0257792809B901E", "0xaab7a1A1217fAad781622C3E19F9cccD6012B8C8")
    checkTransfer("bsc", "0x22A76474A36a058aE818093d08a648a6B204010c", "0x9F1a0AA1fF5f63d8E61a913266BB1326862B38Bf")

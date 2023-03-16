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


def checkTransferTo(chain, contract_address, pair_contract):
    print("扫描transferTo模块", contract_address)
    fn_selector = function_signature_to_4byte_selector('test_transfer_to(address)')
    ms_data1 = encode_abi(["address"],
                          [contract_address])
    input_data = Web3.toHex(fn_selector + ms_data1)
    if chain == "eth":
        chain_id = 1
        evil_contract = "0x84a6c1de33eba06a67ffe4980f6519a0fa2690fe"
    else:
        chain_id = 56
        evil_contract = "0x9559f57a6d9fbc6c84eee6952ccf448dab1b2d9d"
    result, logs = scanutil.simulat(chain_id, pair_contract, evil_contract, input_data)
    if result is None or not result["transaction"]["status"] or logs is None:
        return
    for log in logs:
        if log['raw']['address'] == contract_address.lower() and \
                log['raw']["topics"][0] == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef" and \
                log['raw']["topics"][2][26:].lower() == evil_contract[2:].lower():
            print("%s链：  合约地址：%s   疑似存在TransferTo的安全问题，pair合约地址：%s" % (
                chain, contract_address, pair_contract))
            scanutil.ding_send_text(
                "[chain_poc]" + chain + "：  疑似存在TransferTo的安全问题：" + contract_address + " pair合约地址：   " + pair_contract)


# def checkTransferTo_byphalcon(chain, contract_address, pair_contract):
#     user_contract, balance = scanutil.get_handle_ande_balance(chain, contract_address)
#     print(user_contract)
#     if user_contract is None:
#         return
#     headers = {
#         "Content-Type": "application/json;charset=utf-8",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
#         "X-Forwarded-For": randomIP()
#     }
#     fn_selector = function_signature_to_4byte_selector('test_transfer_to(address)')
#     ms_data1 = encode_abi(["address"],
#                           [contract_address])
#     if chain == "eth":
#         chain_id = 1
#         evil_contract = "0x84a6c1de33eba06a67ffe4980f6519a0fa2690fe"
#     else:
#         chain_id = 56
#         evil_contract = "0x9559f57a6d9fbc6c84eee6952ccf448dab1b2d9d"
#     print(Web3.toHex(fn_selector + ms_data1))
#     post_data = {
#         "chainID": chain_id,
#         "sender": str(user_contract),
#         "receiver": str(evil_contract),
#         "inputData": Web3.toHex(fn_selector + ms_data1),
#         "value": "0",
#         "block": 0,
#         "position": 0,
#         "gasLimit": 1000000,
#         "gasPrice": "100"
#     }
#     print(post_data)
#     try:
#         resp = requests.post(url="https://phalcon.xyz/api/v1/tx/simulate/2", json=post_data,
#                              headers=headers).json()
#         print(resp)
#         if resp['transaction'] is not None and \
#                 resp['transaction']['balanceChanges'] is not None and \
#                 len(resp['transaction']['balanceChanges']) > 0:
#             for change in resp['transaction']['balanceChanges']:
#                 if change['account'] == evil_contract:
#                     print("%s链：  合约地址：%s   疑似存在TransferTo的安全问题，pair合约地址：%s" % (
#                         chain, contract_address, pair_contract))
#                     # scanutil.ding_send_text(
#                     #     "[chain_poc]" + chain + "：  token合约疑似存在TransferTo的安全问题：" + contract_address + " pair合约地址：   " + pair_contract)
#     except Exception as e:
#         print(e)


if __name__ == "__main__":
    # print(randomIP())
    checkTransferTo("bsc", "0xE4Ae305ebE1AbE663f261Bc00534067C80ad677C", "0x8894E0a0c962CB723c1976a4421c95949bE2D4E3")

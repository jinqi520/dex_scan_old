from web3 import Web3
from eth_abi import encode_abi
from eth_utils import function_signature_to_4byte_selector


if __name__ == "__main__":
    fn_selector = function_signature_to_4byte_selector('swap(uint256,uint256,address,bytes)')
    ms_data1 = encode_abi(["uint256,uint256,address,bytes"],
                          [])
    input_data = Web3.toHex(fn_selector + ms_data1)
    print(input_data)

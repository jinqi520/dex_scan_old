import sqlite3
from pocs import check_transfer, check_transferto, check_deliver


def checkIsVul(chain, contract_address, pair_contract):
    try:
        check_transfer.checkTransfer(chain, contract_address, pair_contract)
        check_transferto.checkTransferTo(chain, contract_address, pair_contract)
        check_deliver.checkDeliver(chain, contract_address, pair_contract)
    except Exception as e:
        print(e)
        

def get_token_to_scan():
    while True:
        cx = sqlite3.connect("./token.db")
        c = cx.cursor()
        tokens = c.execute("select contract_address, chain, pair_contract from token where done = 0 limit 50").fetchall()
        for token_info in tokens:
            contract_address = token_info[0]
            chain = token_info[1]
            pair_contract = token_info[2]
            checkIsVul(chain.lower(), contract_address, pair_contract)
            c.execute(
                "update token set done = 1 where contract_address = '" + contract_address + "' and chain = '" + chain + "'")
            cx.commit()
        c.close()
        cx.close()


if __name__ == "__main__":
    get_token_to_scan()
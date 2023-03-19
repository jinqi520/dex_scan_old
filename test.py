import requests, json, time
from scan_util import scanutil

url = "https://www.binance.com/bapi/composite/v1/public/cms/article/latest/query"

while True:
    time.sleep(10)

    resp = requests.get(url)

    res = json.loads(resp.text)["data"]["latestArticles"][0]

    resid = res["id"]
    if resid != 153079:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), time.time(), res)
        scanutil.ding_send_text("[chain_poc]" + time.strftime("%Y-%m-%d %H:%M:%S"))

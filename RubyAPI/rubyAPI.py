import json
from urllib import request
import xml.etree.ElementTree as ET

APPID = "123"  # <-- ここにあなたのClient ID（アプリケーションID）を設定してください。
URL = "https://jlp.yahooapis.jp/FuriganaService/V2/furigana"


def post(query):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Yahoo AppID: {}".format(APPID),
    }
    param_dic = {
      "id": "1234-1",
      "jsonrpc": "2.0",
      "method": "jlp.furiganaservice.furigana",
      "params": {
        "q": query,
        "grade": 1
      }
    }
    params = json.dumps(param_dic).encode()
    req = request.Request(URL, params, headers)
    with request.urlopen(req) as res:
        body = res.read()
    return body.decode()


response = post("漢字かな交じり文にふりがなを振ること。")
#response_dumped=json.dumps(response)
root= json.loads(response)
result=root["result"]["word"]#ヘッダー切り離し
for word in result:
    if('furigana' in word):
        print(len(word))
    else:
        print ("a")
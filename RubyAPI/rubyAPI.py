import json
from urllib import request
import xml.etree.ElementTree as ET
import regex #文字種判別
from lxml import html
import codecs

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

htmlfile=r'monogatari\Kunezumi\Aozora\kunezumi.html'
with open(htmlfile,mode='rb') as f:
    t=html.fromstring(f.read().decode('shiftJIS'))
honbun=(t.text_content())

p = regex.compile(r'\p{Script=Han}+') #漢字判定用正規表現らしい
response = post(honbun)

t=""
#response_dumped=json.dumps(response)
root= json.loads(response)
result=root["result"]["word"]#ヘッダー切り離し
for word in result:
    if('furigana' in word): #ふりがなが入っていたら furiganaが含まれる
        if('subword'in word): #カナ交じりだったらsubwordが含まれる
            for kanamajiri in word["subword"]:
                if(p.fullmatch(kanamajiri["surface"])):
                    t+=("\\ruby{"+kanamajiri["surface"]+"}"+"{"+kanamajiri["furigana"]+"}")
                else:
                    t+=(kanamajiri["surface"])
        else:
            t+=("\\ruby{"+word["surface"]+"}"+"{"+word["furigana"]+"}") #漢字のみのフリガナ設定
    else:
        t+=str(word["surface"])
print(t)
from typing import List
import binascii
import json

import re
import requests
from lxml import etree
from Crypto.Cipher import AES
from Crypto.Hash import MD5


def decrypt(pid: str|int, cache_sign: str) -> List[str]:
    pid = int(pid)
    IV = "".join([str(pid % i % 9) for i in range(2, 18)]).encode()
    key = MD5.new((f"{pid}6af0ce23e2f85cd971f58bdf61ed93a6").encode()).hexdigest()[8:24].encode()
    aes = AES.new(key, AES.MODE_CBC, IV)
    result = aes.decrypt(binascii.a2b_hex(cache_sign)).rstrip()

    result = re.findall(r'(\[.*\])', result.decode())[0]
    return json.loads(result)


def get_cache_sign(pid: str|int) -> str|None:
    url = "https://mmzztt.com/photo/{}".format(pid)
    res = requests.get(url, headers={
        "referer": "https://mmzztt.com/",
        "user-agent": "Mozilla/5.0"
    })
    if res.status_code == 200:
        html = etree.HTML(res.text)
        return html.xpath("//html/comment()")[0].__str__()[68:-3]

if __name__ == '__main__':
    pid = ''
    res = get_cache_sign(pid)

    resp = decrypt(pid, res)
    print(resp)
# coding: utf-8

import requests

headers = {
    'Content-Type': 'application/json;charset=UTF-8'
}

json_body = {
    "text": "36977f9e-41b0-49dd-b293-d059a79bbb35",
    "key": "dyd"
}

url = "http://127.0.0.1:3002/aes-encrypt"

res = requests.post(url, json=json_body, headers=headers)
if res.status_code == 200:
    print(res.content.decode())
else:
    print("报错！")
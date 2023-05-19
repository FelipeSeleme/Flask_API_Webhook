import requests
import json

webhook_url = 'http://127.0.0.1:5000/teste'

data = '{"nome": "Devayanne2", "email": "Jayani06@yandex.com", "status": "aprovado", "valor": 520, "forma_pagamento": "pix", "parcelas": 4}'

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

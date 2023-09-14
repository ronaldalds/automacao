import requests
import time
headers_auth = {
    "Authorization": "9f801004f0730444cb227dd438dff0cdef1241bc"
    }
data_json_auth = {
    "PublicKey": "d8913f9062094f139a6f949f06f1afacf282a509"
    }
auth = requests.post(
     "https://api.desk.ms/Login/autenticar",
     json=data_json_auth,
     headers=headers_auth
)

data_json_relatorio = {
    "Chave": "100"
    }
headers_relatorio = {
    "Authorization": auth.json()
    # "Authorization": "afsgdsbnfgnbcstgdb"
    }
response = requests.post(
    "https://api.desk.ms/Relatorios/imprimir",
    json=data_json_relatorio,
    headers=headers_relatorio
)
if response.json().get("root"):
    print(response.json())
else:
    print(response.json().get("root"))
    print("ok")
import os
import requests
import time

class Desk:
    def __init__(self):
        self.__url_auth = os.environ.get("END_POINT_AUTH")
        self.__url_relatorio = os.environ.get("END_POINT_RELATORIO")
        self.__auth = self.authentication()

    def authentication(self):
        headers = {
            "Authorization": os.environ.get("CHAVE_DESK_ADM")
            }
        data_json = {
            "PublicKey": os.environ.get("CHAVE_DESK_AMBIENTE")
            }
        try:
            response = requests.post(self.__url_auth, json=data_json, headers=headers)
        except:
            print("Error na resposta da rota autenticar")
            time.sleep(14)
            self.authentication()
            
        if (response.status_code == 200) and (len(response.json()) == 59):
            return response.json()
        else:
            print("Error na resposta da rota autenticar")

    def relatorio(self, id) -> dict:
        headers = {
            "Authorization": self.__auth
        }

        data_json = {
            "Chave": id
        }
        try:
            response = requests.post(
                self.__url_relatorio,
                json=data_json,
                headers=headers
            )
        except:
            print("Error na resposta da rota relatário")
            time.sleep(60)
            self.__auth = self.authentication()
            self.relatorio(id)
        
        if (response.status_code == 200) and (response.json().get("root")):
            return response.json()
        else:
            print("Error na resposta da rota relatário")
            self.__auth = self.authentication()
            self.relatorio(id)



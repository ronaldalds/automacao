import os
import requests
import time

class Desk:
    def __init__(self):
        self.__url_auth = os.environ.get("END_POINT_AUTH")
        self.__url_relatorio = os.environ.get("END_POINT_RELATORIO")
        self.__auth = self.authentication()

    def authentication(self):
        try:
            headers = {
                "Authorization": os.environ.get("CHAVE_DESK_ADM")
                }
            data_json = {
                "PublicKey": os.environ.get("CHAVE_DESK_AMBIENTE")
                }
            response = requests.post(self.__url_auth, json=data_json, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(response)
            
        except Exception as e:
            print(f"Error getting: {e}")
    
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
            time.sleep(60)
            self.__auth = self.authentication()
            self.relatorio(id)
        
        if (response.status_code == 200) and (response.json().get("root")):
            return response.json()
        else:
            self.__auth = self.authentication()
            self.relatorio(id)



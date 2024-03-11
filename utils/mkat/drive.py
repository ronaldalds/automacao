import requests
from datetime import datetime, timedelta
from .models import UserMkat


URL_TECNICO = "https://mkat.online.psi.br/agenda/tecnico"
URL_OS = "https://mkat.online.psi.br/agenda/os"


class Mkat:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.__url_agenda_tecnico = URL_TECNICO
        self.__url_agenda_os = URL_TECNICO

    def _make_request(self, url, data_json):
        try:
            response = self.session.post(url, json=data_json)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None

    def agenda_os(self):
        auth = UserMkat.objects.get(nome="TOKEN_MKAT")
        data_json = {
            "token": auth.token,
            "de": datetime.now().strftime('%Y-%m-%d'),
            "ate": (
                datetime.now() + timedelta(days=7)
            ).strftime('%Y-%m-%d'),
            "mk": 1
        }
        response = self._make_request(
            self.__url_agenda_os,
            data_json=data_json
        )
        if response:
            if response.status_code == 200:
                return response.json()

    def agenda_tecnico(self, tecnico):
        auth = UserMkat.objects.get(nome="TOKEN_MKAT")
        data_json = {
            "token": auth.token,
            "tecnico": tecnico,
            "de": datetime.now().strftime('%Y-%m-%d'),
            "ate": (
                datetime.now() + timedelta(days=1)
            ).strftime('%Y-%m-%d'),
            "mk": 1
        }
        response = self._make_request(
            self.__url_agenda_tecnico,
            data_json=data_json
        )
        if response:
            if response.status_code == 200:
                return response.json()

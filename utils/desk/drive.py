import requests
from datetime import datetime, timedelta
from .models import TokenDesk


AUTH_URL = "https://api.desk.ms/Login/autenticar"
REPORT_URL = "https://api.desk.ms/Relatorios/imprimir"
INTERACTION_URL = "https://api.desk.ms/ChamadosSuporte/interagir"
CALLS_URL = "https://api.desk.ms/ChamadosSuporte/lista"
OPERATORS_URL = "https://api.desk.ms/Operadores/lista"


class AuthDTO:
    def __init__(self, status: bool = False, token: str = None):
        self.token: str = token
        self.status: bool = status


class Desk:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.url_auth = AUTH_URL
        self.url_relatorio = REPORT_URL
        self.url_interagir = INTERACTION_URL
        self.url_chamados = CALLS_URL
        self.url_operadores = OPERATORS_URL

    def _make_request(self, url, headers, data_json):
        try:
            response = self.session.post(url, json=data_json, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None

    def authentication(self) -> AuthDTO:
        chave_desk: str = TokenDesk.objects.get(nome="CHAVE_DESK_ADM")
        headers = {"Authorization": chave_desk.operador}
        data_json = {"PublicKey": chave_desk.ambiente}
        response = self._make_request(self.url_auth, headers, data_json)
        auth_dto = AuthDTO()
        if response:
            if response.status_code == 200 and (len(response.json()) == 59):
                auth_dto.token = response.json()
                auth_dto.status = True
                return auth_dto

    def relatorio(self, id: str) -> dict:
        headers = {"Authorization": self.authentication().token}
        data_json = {"Chave": id}
        response = self._make_request(self.url_relatorio, headers, data_json)
        if (response.status_code == 200) and (response.json().get("root")):
            return response.json()
        return {}

    def interagir_chamado(
        self,
        chamado_desk,
        forma_atendimento,
        cod_status,
        operador,
        horario: datetime,
        descricao
    ):
        headers = {"Authorization": self.authentication().token}
        horario_inicial = horario - timedelta(minutes=2)
        data_json = {
            "Chave": chamado_desk,
            "TChamado": {
                "CodFormaAtendimento": forma_atendimento,
                "CodStatus": cod_status,
                "Descricao": descricao,
                "CodCausa": "",
                "CodOperador": operador,
                "CodGrupo": "",
                "DataInteracao": horario.strftime("%d-%m-%Y"),
                "HoraInicial": horario_inicial.strftime("%H:%M:%S"),
                "HoraFinal": horario.strftime("%H:%M")
            }
        }
        print(chamado_desk)
        print(data_json["TChamado"])
        try:
            requests.put(
                self.url_interagir,
                json=data_json,
                headers=headers
            )

        except Exception as e:
            print(f"Error Interagir: {e}")

    def lista_chamados(self):
        headers = {"Authorization": self.authentication().token}
        data_json = {
            "Pesquisa": "",
            "Tatual": "",
            "Ativo": "Todos",
            "StatusSLA": "N",
            "Colunas": {
                "Chave": "on",
                "CodChamado": "on",
                "ChaveUsuario": "on",
                "NomeUsuario": "on",
                "SobrenomeUsuario": "on",
                "NomeOperador": "on",
                "SobrenomeOperador": "on"
            },
            "Ordem": [
                {
                    "Coluna": "Chave",
                    "Direcao": "false"
                }
            ]
        }
        response = self._make_request(self.url_chamados, headers, data_json)
        if response.status_code == 200:
            return response.json()
        return {}

    def lista_operador(self):
        headers = {"Authorization": self.authentication().token}
        data_json = {
            "Colunas": {
                "Chave": "on",
                "Nome": "on",
                "Sobrenome": "on",
                "Email": "on",
                "OnOff": "on",
                "GrupoPrincipal": "on",
                "EmailGrupo": "on",
                "CodGrupo": "on"
            },
            "Pesquisa": "",
            "Ativo": "S",
            "Filtro": {
                "Ramal": [""],
                "GrupoPrincipal": [""],
                "Perfil": [""],
                "Online": [""],
                "LicencaDMS": [""],
                "LicencaCHAT": [""],
                "LicencaRCS": [""],
                "LicencaFornecedor": [""]
            },
            "Ordem": [
                {
                    "Coluna": "Nome",
                    "Direcao": "true"
                }
            ]
        }
        response = self._make_request(self.url_operadores, headers, data_json)
        if response.status_code == 200:
            return response.json()
        return {}

    def operador_do_chamado(self, id_chamado):
        chamados = self.lista_chamados()
        for chamado in chamados["root"]:
            try:
                if chamado["CodChamado"] == id_chamado:
                    operadores = self.lista_operador()
                    operador_chamado = {
                        "NomeOperador": chamado["NomeOperador"],
                        "SobrenomeOperador": chamado["SobrenomeOperador"],
                    }
                    for operador in operadores["root"]:
                        nome = operador["Nome"] == operador_chamado["NomeOperador"]
                        sobrenome = operador["Sobrenome"] == operador_chamado["SobrenomeOperador"]
                        if nome and sobrenome:
                            return operador["Chave"]

            except Exception as e:
                print(f"Error: {e}")
                return False

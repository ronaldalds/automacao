import requests
from time import sleep
from datetime import datetime, timedelta
from .models import TokenDesk


class AuthDTO:
    def __init__(self, status: bool = False, token: str = None):
        self.token: str = token
        self.status: bool = status


class Desk:
    def __init__(self) -> None:
        self.url_auth = "https://api.desk.ms/Login/autenticar"
        self.url_relatorio = "https://api.desk.ms/Relatorios/imprimir"
        self.url_interagir = "https://api.desk.ms/ChamadosSuporte/interagir"
        self.url_chamados = "https://api.desk.ms/ChamadosSuporte/lista"
        self.url_operadores = "https://api.desk.ms/Operadores/lista"

    def authentication(self) -> AuthDTO:
        chave_desk: str = TokenDesk.objects.get(nome="CHAVE_DESK_ADM")
        headers = {"Authorization": chave_desk.operador}
        data_json = {"PublicKey": chave_desk.ambiente}
        response = AuthDTO()

        try:
            request = requests.post(
                self.url_auth,
                json=data_json,
                headers=headers
            )
            if request.status_code == 200 and (len(request.json()) == 59):
                response.token = request.json()
                response.status = True

            return response

        except Exception as e:
            print(f"Error getting: {e}")
            sleep(14)
            self.authentication()

    def relatorio(self, id: str) -> dict:
        headers = {"Authorization": self.authentication().token}
        data_json = {"Chave": id}

        try:
            response = requests.post(
                self.url_relatorio,
                json=data_json,
                headers=headers
            )
        except Exception as e:
            print(f"Error: {e}")
            sleep(60)
            self.relatorio(id)

        if (response.status_code == 200) and (response.json().get("root")):
            return response.json()
        else:
            print("Error na resposta da rota relatário")
            self.relatorio(id)

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
        try:
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

            response = requests.post(
                self.url_chamados,
                json=data_json,
                headers=headers
            )

            if response.status_code == 200:
                return response.json()

        except Exception as e:
            print(f"Error lista chamados: {e}")

    def lista_operador(self):
        try:
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

            response = requests.post(
                self.url_operadores,
                json=data_json,
                headers=headers
            )

            if response.status_code == 200:
                return response.json()

        except Exception as e:
            print(f"Error lista operador: {e}")

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

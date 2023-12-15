import requests
from time import sleep
from datetime import datetime, timedelta
from dotenv import dotenv_values

env: dict = dotenv_values(".env")


class AuthDTO:
    def __init__(self, status: bool, token: str = None):
        self.token: str = token
        self.status: bool = status


class Desk:
    def __init__(self):
        self.chave_operador: str = env.get("CHAVE_DESK_ADM")
        self.chave_ambiente: str = env.get("CHAVE_DESK_AMBIENTE")

    def authentication(self) -> AuthDTO:
        headers = {"Authorization": self.chave_operador}
        data_json = {"PublicKey": self.chave_ambiente}
        response: AuthDTO = AuthDTO(status=False)

        try:
            request = requests.post(
                "https://api.desk.ms/Login/autenticar",
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

    def relatorio(self, id) -> dict:
        headers = {"Authorization": self.authentication().token}
        data_json = {"Chave": id}
        try:
            response = requests.post(
                "https://api.desk.ms/Relatorios/imprimir",
                json=data_json,
                headers=headers
            )
        except Exception as e:
            print(f"Error: {e}")
            sleep(60)
            self.__auth = self.authentication()
            self.relatorio(id)

        if (response.status_code == 200) and (response.json().get("root")):
            return response.json()
        else:
            print("Error na resposta da rota relatário")
            self.__auth = self.authentication()
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
                "https://api.desk.ms/ChamadosSuporte/interagir",
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
                    "Colunas":
                    {
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
                "https://api.desk.ms/ChamadosSuporte/lista",
                json=data_json,
                headers=headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(response)

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
                    "Filtro":
                    {
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
                "https://api.desk.ms/Operadores/lista",
                json=data_json,
                headers=headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(response)

        except Exception as e:
            print(f"Error lista operador: {e}")

    def operador_do_chamado(self, id_chamado):
        chamados = self.lista_chamados()
        operadores = self.lista_operador()

        for chamado in chamados["root"]:
            try:
                if chamado["CodChamado"] == id_chamado:
                    try:
                        operador_chamado = {
                            "NomeOperador": chamado["NomeOperador"],
                            "SobrenomeOperador": chamado["SobrenomeOperador"],
                        }
                        for operador in operadores["root"]:
                            if (operador["Nome"] == operador_chamado["NomeOperador"]) and (operador["Sobrenome"] == operador_chamado["SobrenomeOperador"]):
                                return operador["Chave"]

                    except Exception as e:
                        print(f"chamado sem Operador associado! {e}")
                        return False

            except Exception as e:
                print(f"Error operador do chamado {e}")
                return False

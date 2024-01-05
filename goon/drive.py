import json
from zeep import Client
import xmltodict
from goon.models import TokenGoon


class Goon:
    def __init__(self) -> None:
        self.url = "https://ws.goon.mobi/webservices/keeplefieldintegration.asmx?wsdl"

    def get_all_located_orders_by_agent(
        self,
        agente_codigo,
        mobile_agent,
        data
    ):
        try:
            auth_goon = TokenGoon.objects.get(
                nome="AUTH_CODE_GET_ALL_LOCATED_ORDERS_BY_AGENT"
            )

            reques_data = {
                'authCode': auth_goon.auth,
                'clientCode': auth_goon.cliente,
                'agenteCodigo': agente_codigo,
                'mobileAgentCodeSource': mobile_agent,
                'dataFinalizacaoCancelamento': data,
            }

            client = Client(self.url)
            response = client.service.GetAllocatedOrdersByAgent(**reques_data)

            dicionario = json.loads(response)

            if not dicionario["success"]:
                return False

            xml = dicionario["answersXML"].replace('<>', '-')

            data_goon = xmltodict.parse(
                xml,
                force_list=(
                    "FormAnswer",
                    "StatusInfo",
                    "ItemAnswer"
                )
            )

            return data_goon

        except Exception as e:
            print(f"Error getting get all located: {e}")
            return False

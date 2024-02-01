import json
from zeep import Client
import xmltodict
from .models import TokenGoon

URL_GOON = "https://ws.goon.mobi/webservices/keeplefieldintegration.asmx?wsdl"
AUTH_CODE = "AUTH_CODE_GET_ALL_LOCATED_ORDERS_BY_AGENT"


class Goon:
    def __init__(self) -> None:
        self.url = URL_GOON
        self.auth_code = AUTH_CODE

    def get_all_located_orders_by_agent(
        self,
        agente_codigo,
        mobile_agent,
        data
    ):
        try:
            auth_goon = TokenGoon.objects.get(nome=self.auth_code)

            request_data = {
                'authCode': auth_goon.auth,
                'clientCode': auth_goon.cliente,
                'agenteCodigo': agente_codigo,
                'mobileAgentCodeSource': mobile_agent,
                'dataFinalizacaoCancelamento': data,
            }

            client = Client(self.url)
            response = client.service.GetAllocatedOrdersByAgent(**request_data)

            dictionary = json.loads(response)

            if not dictionary["success"]:
                return False

            xml = dictionary["answersXML"].replace('<>', '-')
            xml = xml.replace('&', '')

            goon_data = xmltodict.parse(
                xml,
                force_list=(
                    "FormAnswer",
                    "StatusInfo",
                    "ItemAnswer"
                )
            )

            return goon_data

        except TokenGoon.DoesNotExist:
            print(f"TokenGoon with name {AUTH_CODE} does not exist.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

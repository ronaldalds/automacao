import json
import xml.etree.ElementTree as ET
from zeep import Client
from goon.models import TokenGoon, UrlGoon


class Goon:
    def parse_goon_xml_to_dict(self, xml_str):
        # Faz o parse do XML para obter o elemento raiz
        root = ET.fromstring(xml_str)

        # Lista para armazenar os dados
        results = []

        # Percorre todas as tags FormAnswer
        for form_answer in root.findall('FormAnswer'):
            form_data = {}

            # Extrai as informações da tag FormAnswer
            for child in form_answer:
                form_data[child.tag] = child.text

            # Lista para armazenar os dados da StatusSequence
            status_sequence_data = []

            # Percorre todas as tags StatusInfo dentro de StatusSequence
            tag_status_info = './/StatusSequence/StatusInfo'
            for status_info in form_answer.findall(tag_status_info):
                status_info_data = {}

                # Extrai as informações da tag StatusInfo
                for child in status_info:
                    status_info_data[child.tag] = child.text

                status_sequence_data.append(status_info_data)

            form_data['StatusSequence'] = status_sequence_data

            # Lista para armazenar os dados da ItemAnswers
            item_answers_data = []

            # Percorre todas as tags ItemAnswer dentro de ItemAnswers
            tag_item_answer = './/ItemAnswers/ItemAnswer'
            for item_answer in form_answer.findall(tag_item_answer):
                item_answer_data = {}

                # Extrai as informações da tag ItemAnswer
                for child in item_answer:
                    if child.tag == 'Answer':
                        item_answer_data[child.tag] = {
                            i_child.tag: i_child.text for i_child in child
                        }
                    else:
                        item_answer_data[child.tag] = child.text

                item_answers_data.append(item_answer_data)

            form_data['ItemAnswers'] = item_answers_data

            results.append(form_data)

        return results

    def get_all_located_orders_by_agent(
        self,
        agente_codigo,
        mobile_agent,
        data
    ) -> list:
        data_goon = []
        try:
            auth_goon = TokenGoon.objects.get(
                nome="AUTH_CODE_GET_ALL_LOCATED_ORDERS_BY_AGENT"
            )
            url_goon = UrlGoon.objects.get(id=1)
            reques_data = {
                'authCode': auth_goon.auth,
                'clientCode': auth_goon.cliente,
                'agenteCodigo': agente_codigo,
                'mobileAgentCodeSource': mobile_agent,
                'dataFinalizacaoCancelamento': data,
            }

            client = Client(url_goon.url)
            response = client.service.GetAllocatedOrdersByAgent(**reques_data)

            dicionario = json.loads(response)

            if not dicionario["success"]:
                return dicionario["success"]

            xml = dicionario["answersXML"].replace('<>', '-')

            data_goon = self.parse_goon_xml_to_dict(xml)

        except Exception as e:
            print(f"Error getting get all located: {e}")

        return data_goon

from datetime import datetime, timedelta


data = datetime.now()
tempo_ciclo = 5
proxima_data = data + timedelta(minutes=tempo_ciclo)
str_data = data.strftime("%d/%m/%Y %H:%M")
str_proixma_data = proxima_data.strftime("%d/%m/%Y %H:%M")
print(str_data, str_proixma_data)

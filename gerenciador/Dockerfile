FROM python:3.11.3-alpine
LABEL mantainer="ronald.ralds@gmail.com"

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

WORKDIR /gerenciador

COPY . .

ENV TZ=America/Fortaleza

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# uso em desenvolvimento
# CMD python manage.py runserver 0.0.0.0:8000

# uso em produção
CMD gunicorn core.wsgi:application --bind 0.0.0.0:8000
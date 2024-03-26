FROM selenium/standalone-chrome:122.0

USER root

ENV TZ=America/Fortaleza

# Instala o Python, pip e xvfb
RUN apt-get update && apt install -y python3.11 python3-pip xvfb

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD xvfb-run --server-args="-screen 0, 1280x960" -a gunicorn core.wsgi:application --bind 0.0.0.0:5000
# CMD xvfb-run --server-args="-screen 0, 1280x960" -a python3 manage.py runserver 0.0.0.0:5000
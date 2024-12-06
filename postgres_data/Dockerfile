#installation de l'image python-slim
FROM python:3.12.3-slim 

#répertoire de travail
WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["sleep", "infinity"]

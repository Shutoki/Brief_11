#installation de l'image python-slim
FROM python:3.12.3-slim 

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

RUN apt-get -y update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Copier le fichier requirements.txt dans le répertoire de travail
COPY . /app

# Installer les dépendances nécessaires
RUN pip3 install -r requirements.txt

# Définir la commande pour lancer l'application
CMD ["sleep", "infinity"]

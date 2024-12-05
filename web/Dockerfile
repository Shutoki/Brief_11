FROM python:3.12.3-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git

RUN apt-get install -y libpq-dev gcc \
    && pip install psycopg2

COPY . /app

RUN pip3 install -r requirements.txt

# EXPOSE 8501

#vérification pour voir si l'appli fonctionne
# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["sleep", "infinity"]

# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

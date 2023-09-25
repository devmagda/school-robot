# Verwende ein Python-Image als Basis
FROM python:3

# Setze den Arbeitsverzeichnis im Container
WORKDIR /usr/src/app

# Kopiere die Python-Anwendung in den Container
COPY . .

# Installiere die benötigten Python-Pakete
RUN pip install psycopg2

# Starte die Python-Anwendung
CMD ["python", "database.py"]

import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Hier kannst du SQL-Anfragen ausführen, z.B.
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, name VARCHAR);")

# Wichtige Änderungen an der Datenbank müssen mit commit bestätigt werden
conn.commit()

# Verbindung schließen
cur.close()
conn.close()

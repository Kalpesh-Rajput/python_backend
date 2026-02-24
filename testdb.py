import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="740542",
    port="5432"
)

print("Connected successfully!")

conn.close()

import psycopg2

db_engine = psycopg2.connect(
    user="postgres",
    database="jednostki_policji",
    password="postgres",
    port="5432",
    host="localhost"
)
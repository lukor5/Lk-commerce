import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


conn_string = "host='lkcommercedb.cfu8mwgk6xtw.eu-north-1.rds.amazonaws.com' dbname='lkcommercedb' user='postgres' password='miriam123'"
conn = psycopg2.connect(conn_string)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

print("Database opened successfully")
cursor = conn.cursor();
cursor.execute("create database lkcommerce_db");

conn.close()

conn_string = "host='localhost' dbname='lkcommerce_db' user='lukor' password='miriam123'"
conn = psycopg2.connect(conn_string)
# here you need to populate database wit tables "create table mytbl..."
conn.close()
print("Database Closed successfully")
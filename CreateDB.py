import psycopg2
import sys

conn = None
conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432")
conn.set_isolation_level(0)
cursor = conn.cursor()
try:
    cursor.execute('DROP DATABASE  projectium')
    print "DB has been deleted."
except psycopg2.ProgrammingError:
    print "DB does not exist."
except psycopg2.OperationalError:
    print "DB In use, cannot delete."
    sys.exit(1)
cursor.execute('CREATE DATABASE Polireserva')
cursor.close()
conn.close()
print "Db created."
sys.exit(0)

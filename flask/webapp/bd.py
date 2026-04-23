#Archivo donde definimos la funcion de conexion con la base de datos,
#para no estarla colocando varias veces en el archivo view.py lo mismo
#muchas veces: 
# bd.py
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )


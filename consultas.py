import psycopg2
import statistics
from helper import FunVacuum, create_indexes, drop_indexes
import time


# nos conectamos a la bd

conn = psycopg2.connect(
    host="localhost",
    database="proyecto",
    user="postgres",
    password="Goleador0107",
    options="-c search_path=mil"
)
cursor = conn.cursor()
conn.autocommit = True


# consulta1.sql en una variable

with open('sql/Consulta1.sql', 'r') as file:
    consulta1 = file.read()


# ejecutamos la consulta

def execute_query(query, schema):
    start_time = time.time()
    cursor.execute(f"SET search_path TO {schema}")
    cursor.execute(query)
    end_time = time.time()
    return end_time - start_time


def registros(query, schema, index):
    if index == 1:
        cursor.execute(create_indexes(schema))
    else:
        cursor.execute(drop_indexes(schema))
    num_executions = 5

    execution_times = []
    for i in range(num_executions):
        FunVacuum(schema)
        execution_time = execute_query(query, schema)
        execution_times.append(execution_time)
        print(
            f"Ejecución {i+1}: Tiempo de ejecución = {execution_time} segundos")

    average_time = statistics.mean(execution_times)
    std_deviation = statistics.stdev(execution_times)

    print(f"\nTiempo promedio de ejecución: {average_time} segundos")
    print(f"Desviación estándar: {std_deviation} segundos")


registros(consulta1, "mil")

import psycopg2
import statistics
from typing import List
from helpers import FunVacuum, create_indexes, drop_indexes, create_latex_table
import time
from dotenv import load_dotenv
import os

load_dotenv()
# Crear instancia de Faker
conn = psycopg2.connect(
    host="localhost",
    database="proyecto",
    user="postgres",
    password="Goleador0107"
)
cursor = conn.cursor()
conn.autocommit = True

num_executions = 5

# consulta1.sql en una variable

with open('sql/Consulta1.sql', 'r') as file:
    consulta1 = file.read()

with open('sql/Consulta2.sql', 'r') as file:
    consulta2 = file.read()

with open('sql/Consulta3.sql', 'r') as file:
    consulta3 = file.read()


# ejecutamos la consulta

def execute_query(query, schema):
    start_time = time.time()
    cursor.execute(f"SET search_path TO {schema}")
    cursor.execute(query)
    end_time = time.time()
    return end_time - start_time


def registros(query, schema, index) -> List[float]:
    if index:
        cursor.execute(create_indexes(schema))
    else:
        cursor.execute(drop_indexes(schema))

    execution_times: List[float] = []
    for i in range(num_executions):
        cursor.execute(FunVacuum(schema))
        execution_time = execute_query(query, schema)
        execution_times.append(execution_time)
        print(
            f"Ejecución {i+1}: Tiempo de ejecución = {execution_time} segundos")

    average_time = statistics.mean(execution_times)
    std_deviation = statistics.stdev(execution_times)

    print(f"\nTiempo promedio de ejecución: {average_time} segundos")
    print(f"Desviación estándar: {std_deviation} segundos")

    execution_times = [round(num, 3) for num in execution_times]
    execution_times.append(round(average_time, 4))
    execution_times.append(round(average_time, 6))

    return execution_times


def gen_latex_table(title, query, has_indexes):
    print(f"\n\n{title}\n")
    arr = []
    schemas = ["mil", "diezmil", "cienmil", "millon"]
    for i in range(4):
        arr.append(registros(query, schemas[i], has_indexes))

    try:
        create_latex_table(title, arr, num_executions, has_indexes)
    except Exception as e:
        print("No hay compilador, pero se pudo crear la tabla :)")


if __name__ == "__main__":
    # Sin índices
    # gen_latex_table("Consulta 1", consulta1, False)

    # gen_latex_table("Consulta 2", consulta2, False)

    # gen_latex_table("Consulta 3", consulta3, False)

    # Con índices
    gen_latex_table("Consulta 1", consulta1, True)

    gen_latex_table("Consulta 2", consulta2, True)

    gen_latex_table("Consulta 3", consulta3, True)

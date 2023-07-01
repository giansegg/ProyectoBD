import psycopg2
import statistics
from typing import List
from helpers import FunVacuum, create_indexes, drop_indexes, create_latex_table
import time
from dotenv import load_dotenv
from graficas import create_graphic
import os

load_dotenv()
# Crear instancia de Faker
conn = psycopg2.connect(
    host="localhost",
    database="proyecto",
    user="postgres",
    password="1234"
)
cursor = conn.cursor()
conn.autocommit = True

NUM_EXECUTIONS = 5
SCHEMAS = ["mil", "diezmil", "cienmil", "millon"]

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
    for i in range(NUM_EXECUTIONS):
        cursor.execute(FunVacuum(schema))
        execution_time = execute_query(query, schema)
        execution_times.append(execution_time)
        # print(
            # f"Ejecución {i+1}: Tiempo de ejecución = {execution_time} segundos")

    average_time = statistics.mean(execution_times)
    std_deviation = statistics.stdev(execution_times)

    # print(f"\nTiempo promedio de ejecución: {average_time} segundos")
    # print(f"Desviación estándar: {std_deviation} segundos")

    execution_times = [round(num, 3) for num in execution_times]
    execution_times.append(round(average_time, 4))
    execution_times.append(round(average_time, 6))

    return execution_times


def gen_latex_table(title, query, has_indexes):
    print(f"\n\n{title}\n")
    arr = []
    for i in range(4):
        arr.append(registros(query, SCHEMAS[i], has_indexes))

    try:
        create_latex_table(title, arr, NUM_EXECUTIONS, has_indexes)
    except Exception as e:
        print("No hay compilador, pero se pudo crear la tabla :)")


def plot_times(title: str, query):
    print("Grafico de: " + title)
    # Tiempos promedio para las consultas con/sin índices
    # times[0] tiempos promedios sin índices
    # times[1] tiempos promedios con índices
    times: List[List[float]] = []
    # Tiempos promedio para cada esquema 1k, 10k, 100k y 1M
    arr: List[float] = []

    complete_array: List[float] = []
    times_for_latex: List[List[float]] = []
    for i in range(4):
        complete_array = registros(query, SCHEMAS[i], False)
        tiempo_promedio: float = complete_array[NUM_EXECUTIONS]
        arr.append(tiempo_promedio)
        times_for_latex.append(complete_array)

    create_latex_table(title, times_for_latex, NUM_EXECUTIONS, False)

    times.append(arr)
    arr.clear()
    times_for_latex.clear()


    for i in range(4):
        complete_array = registros(query, SCHEMAS[i], True)
        tiempo_promedio: float = complete_array[NUM_EXECUTIONS]
        arr.append(tiempo_promedio)
        times_for_latex.append(complete_array)

    create_latex_table(title, times_for_latex, NUM_EXECUTIONS, True)

    times.append(arr)

    create_graphic(title, times)


if __name__ == "__main__":
    # Sin índices
    # gen_latex_table("Consulta 1", consulta1, False)

    # gen_latex_table("Consulta 2", consulta2, False)

    # gen_latex_table("Consulta 3", consulta3, False)

    # Con índices
    # gen_latex_table("Consulta 1", consulta1, True)

    # gen_latex_table("Consulta 2", consulta2, True)

    # gen_latex_table("Consulta 3", consulta3, True)

    plot_times("Consulta 1", consulta1)
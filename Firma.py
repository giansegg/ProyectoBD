from typing import List, Tuple, Any
import numpy as np
import psycopg2
from faker import Faker
from dotenv import load_dotenv
import concurrent.futures
import multiprocessing
import os

load_dotenv()
# Crear instancia de Faker
fake = Faker()
# Conexión a la base de datos
conn = psycopg2.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD")
)
cursor = conn.cursor()

# Delete tables if exists
with open("EliminarTablas.sql", "r") as file:
    sql = file.read()
    cursor.execute(sql)


# Create tables if not exists
with open("CrearTablas.sql", "r") as file:
    sql = file.read()
    cursor.execute(sql)


class Firma:
    def __init__(self, n):
        print(f"Instancia de {n} datos creada!")
        self.n_personas = n
        self.n_empleados = (3*n)//4
        self.n_abogados = (3*self.n_empleados)//4
        self.personas = np.empty(shape=(0, 2), dtype=str)


    def createData(self):
        try:
            self.createPersonas()
            # self.createEmpleados()
            # self.createAbogados()
            # self.createSecretarios()
            # self.createCasos()
            conn.commit()
            print("Datos insertados correctamente")
        except Exception as e:
            print("Error: ", e)

        conn.close()

    def createPersonas(self) -> None:
        sql = "INSERT INTO Persona (tipo_documento, numero_documento, nombre, apellido, sexo, correo) VALUES (%s, %s, %s, %s, %s, %s)"
        data: np.ndarray = np.empty(shape=(0, 6), dtype=str)

        def generate_persona():
            tipo_documento = fake.random_element(elements=("DNI", "Pasaporte"))
            numero_documento = fake.unique.random_number(digits=8)
            nombre = fake.first_name()
            apellido = fake.last_name()
            sexo = fake.random_element(elements=("M", "F"))
            correo = fake.email()

            return (tipo_documento, numero_documento, nombre, apellido, sexo, correo)

        num_cores = multiprocessing.cpu_count()
        num_threads = int(num_cores * 0.9)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Get the number of threads used by the ThreadPoolExecutor
            num_threads = executor._max_workers

            # Generate the data for personas in parallel
            futures = [executor.submit(generate_persona) for _ in range(self.n_personas)]

            # Get the results of the futures
            for future in concurrent.futures.as_completed(futures):
                data = np.append(data, [future.result()], axis=0)

        cursor.executemany(sql, data)


    # def createPersonas(self) -> None:
    #     sql: str = "INSERT INTO Persona (tipo_documento, numero_documento, nombre, apellido, sexo, correo) VALUES (%s,%s,%s,%s,%s,%s)"
    #     data: np.ndarray = np.empty(shape=(0, 6), dtype=str)
    #     for _ in range(self.n_personas):
    #         tipo_documento = fake.random_element(
    #             elements=("DNI", "Pasaporte"))
    #         numero_documento = fake.unique.random_number(digits=8)
    #         nombre = fake.first_name()
    #         apellido = fake.last_name()
    #         sexo = fake.random_element(elements=("M", "F"))
    #         correo = fake.email()
    #         # Insert into personas array to take the reference
    #         self.personas = np.append(self.personas, [(tipo_documento, numero_documento)], axis=0)
    #
    #         # Insert into temporal array to insert the data
    #         data = np.append(data, [(tipo_documento, numero_documento,nombre,apellido,sexo,correo)], axis=0)
    #
    #     cursor.executemany(sql, data)

    def createEmpleados(self) -> None:
        for _ in range(0, self.n_empleados):
            [tipo_documento, numero_documento] = self.personas[_]
            sueldo = fake.random_int(min=2000, max=10000)
            fecha_inicio = fake.date_time_between(start_date="-5y", end_date="now")
            tiempo_parcial = fake.random_element(elements=(True, False))
            cursor.execute(
                "INSERT INTO Empleado (numero_documento, tipo_documento, sueldo, fecha_inicio, tiempo_parcial) VALUES (%s, %s, %s, %s, %s)",
                (numero_documento, tipo_documento, sueldo, fecha_inicio, tiempo_parcial)
            )


    def createAbogados(self) -> None:
        for _ in range(0, self.n_abogados):
            [tipo_documento, numero_documento] = self.personas[_]
            sueldo = fake.random_int(min=2000, max=10000)
            fecha_inicio = fake.date_time_between(start_date="-5y", end_date="now")
            tiempo_parcial = fake.random_element(elements=(True, False))
            especializacion = fake.random_element(
                elements=("Civil", "Penal", "Laboral", "Familiar", "Mercantil"))
            numero_colegiatura = fake.random_number(digits=6)
            casos_ganados = fake.random_int(min=0, max=100)
            casos_perdidos = fake.random_int(min=0, max=100)
            cursor.execute(
                "INSERT INTO Abogado (numero_documento, tipo_documento, especializacion, numero_colegiatura, casos_ganados, casos_perdidos) VALUES (%s, %s, %s, %s, %s, %s)",
                (numero_documento, tipo_documento, sueldo, fecha_inicio,
                 tiempo_parcial, especializacion, numero_colegiatura, casos_ganados, casos_perdidos)
            )

    def createSecretarios(self):
        for _ in range(self.n_abogados, self.n_empleados):
            [tipo_documento, numero_documento, nombre,
             apellido, sexo, correo] = self.personas[_]
            formacion_tecnica = fake.random_element(elements=(True, False))
            tiempo_parcial = fake.random_element(elements=(True, False))
            fecha_inicio = fake.date_time_between(start_date="-5y", end_date="now")
            sueldo = fake.random_int(min=2000, max=10000)
            cursor.execute(
                "INSERT INTO Secretario (numero_documento, tipo_documento, formacion_tecnica, tiempo_parcial) VALUES (%s, %s, %s, %s)",
                (numero_documento, tipo_documento, nombre, apellido,
                 sexo, correo, sueldo, fecha_inicio, formacion_tecnica, tiempo_parcial)
            )

    def createCasos(self):
        for _ in range():
            codigo = fake.unique.random_number(digits=6)
            nombre = "Caso numero" + str(fake.unique.random_number(digits=6))
            estado = fake.random_element(elements=('Registrado', 'EnProceso', 'Culminado'))
            fecha_inicio = fake.date_time_between(start_date="-5y", end_date="now")
            fecha_fin = fake.date_time_between(start_date=fecha_inicio, end_date="now")
            tipo_caso = fake.random_element(
                elements=("Civil", "Penal", "Laboral", "Familiar", "Mercantil"))
            cursor.execute(
                "INSERT INTO Caso (codigo, nombre, estado, fecha_inicio, fecha_fin, tipo_caso) VALUES (%s, %s, %s, %s, %s, %s)",
                (codigo, nombre, estado, fecha_inicio, fecha_fin, tipo_caso)
            )
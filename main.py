import psycopg2
from faker import Faker
from dotenv import load_dotenv
import random
import os
from helper import create_tables, drop_tables
import time

load_dotenv()
# Crear instancia de Faker
fake = Faker()
# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="proyecto",
    user="postgres",
    password="Goleador0107"
)
cursor = conn.cursor()

conn.autocommit = True


def create_all(n, schema) -> None:
    """
    Mock de la base de datos de aprox. n tuplas en un esquema
    """
    # Create schema
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")

    # Delete tables if exists
    cursor.execute(drop_tables(schema))

    # Create tables if not exists
    cursor.execute(create_tables(schema))

    # Tabla Personas n
    def genPersonas():
        i = 0
        while i < n:
            try:
                tipo_documento = fake.random_element(
                    elements=("DNI", "Pasaporte"))
                numero_documento = fake.unique.random_number(digits=8)
                nombre = fake.first_name()
                apellido = fake.last_name()
                sexo = fake.random_element(elements=("M", "F"))
                correo = fake.email()
                cursor.execute(
                    f"SELECT 1 FROM {schema}.Persona WHERE (tipo_documento, numero_documento) = ('{tipo_documento}','{numero_documento}');")
                if not cursor.fetchone():
                    cursor.execute(
                        f"INSERT INTO {schema}.Persona (tipo_documento, numero_documento, nombre, apellido, sexo, correo) VALUES (%s, %s, %s, %s, %s, %s)",
                        (tipo_documento, numero_documento,
                         nombre, apellido, sexo, correo)
                    )
                    i += 1
            except Exception as e:
                pass

    # Tabla Casos n

    def genCasos():
        i = 0
        while i < 300000:
            try:
                codigo = fake.unique.random_number(digits=9)
                nombre = "Caso numero" + \
                    str(fake.unique.random_number(digits=9))
                estado = fake.random_element(
                    elements=('Registrado', 'EnProceso', 'Culminado'))
                fecha_inicio = fake.date_time_between(
                    start_date="-5y", end_date="now")
                fecha_fin = fake.date_time_between(
                    start_date=fecha_inicio, end_date="now")
                tipo_caso = fake.random_element(
                    elements=("Civil", "Penal", "Laboral", "Familiar", "Mercantil"))

                cursor.execute(
                    f"INSERT INTO {schema}.Caso (codigo, nombre, estado, fecha_inicio, fecha_fin, tipo_caso) VALUES (%s, %s, %s, %s, %s, %s)",
                    (codigo, nombre, estado, fecha_inicio, fecha_fin, tipo_caso)
                )
                i += 1
            except Exception as e:
                print(e)

    # Tabla Telefonos 50% de n

    def genTelefonos():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Persona;")
        res = cursor.fetchall()
        while i < 0.2*n:
            try:
                fk = random.choice(res)
                numero = '9' + str(fake.unique.random_number(digits=8))

                cursor.execute(
                    f"INSERT INTO {schema}.Telefono (numero, numero_documento, tipo_documento) VALUES (%s, %s, %s);",
                    (numero, fk[1], fk[0]))
                i += 1
            except Exception as e:
                pass

    # Tabla Empleados 80% de n

    def genEmpleados():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Persona WHERE (tipo_documento, numero_documento) NOT IN (SELECT tipo_documento, numero_documento FROM {schema}.Empleado);")
        res = cursor.fetchall()
        while i < n*0.8:
            try:
                fk = random.choice(res)
                sueldo = fake.random_int(min=2000, max=10000)
                fecha_inicio = fake.date_time_between(
                    start_date="-5y", end_date="now")
                tiempo_parcial = fake.random_element(elements=(True, False))

                cursor.execute(
                    f"INSERT INTO {schema}.Empleado (numero_documento, tipo_documento, sueldo, fecha_inicio, tiempo_parcial) VALUES (%s, %s, %s, %s, %s)",
                    (fk[1], fk[0], sueldo, fecha_inicio, tiempo_parcial)
                )
                i += 1
            except Exception as e:
                pass

    # Tabla Abogados 70%*80% de n

    def genAbogados():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Empleado;")
        res = cursor.fetchall()
        while i < n*0.7*0.8:
            try:
                fk = random.choice(res)
                especializacion = fake.random_element(
                    elements=("Civil", "Penal", "Laboral", "Familiar", "Mercantil"))
                numero_colegiatura = fake.random_number(digits=6)
                casos_ganados = fake.random_int(min=0, max=500)
                casos_perdidos = fake.random_int(min=0, max=500)
                cursor.execute(
                    f"INSERT INTO {schema}.Abogado (numero_documento, tipo_documento, especializacion, numero_colegiatura, casos_ganados, casos_perdidos) VALUES (%s, %s, %s, %s, %s, %s)",
                    (fk[1], fk[0], especializacion,
                        numero_colegiatura, casos_ganados, casos_perdidos)
                )
                i += 1
            except Exception as e:
                pass

    # Tabla Secretarios 30%*80% de n

    def genSecretarios():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Empleado  WHERE EXISTS (SELECT * FROM {schema}.Abogado WHERE (tipo_documento, numero_documento) = (tipo_documento, numero_documento));")
        res = cursor.fetchall()
        while i < 0.3*0.8*n:
            try:
                fk = random.choice(res)
                formacion_tecnica = fake.random_element(elements=(True, False))
                cursor.execute(
                    f"INSERT INTO {schema}.Secretario (numero_documento, tipo_documento, formacion_tecnica) VALUES (%s, %s, %s)",
                    (fk[1], fk[0], formacion_tecnica)
                )
                i += 1
            except Exception as e:
                pass

    # Tabla Departamentos
    departamentos_nombres = ["Civil", "Penal", "Laboral", "Familiar", "Mercantil",
                             "Administrativo", "Constitucional", "Tributario", "Ambiental", "Procesal"]

    def genDepartamentos():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Abogado;")
        res = cursor.fetchall()
        while i < len(departamentos_nombres):
            try:
                fk = random.choice(res)
                nombre = departamentos_nombres[i]
                fecha_creacion = fake.date_time_between(
                    start_date="-5y", end_date="now")
                cursor.execute(
                    f"SELECT 1 FROM {schema}.Departamento WHERE (tipo_documento_abogado_responsable, numero_documento_abogado_responsable) = ('{fk[0]}','{fk[1]}');")
                if not cursor.fetchone():
                    cursor.execute(
                        f"INSERT INTO {schema}.Departamento (nombre, numero_documento_abogado_responsable, tipo_documento_abogado_responsable, fecha_creacion) VALUES (%s, %s, %s, %s)",
                        (nombre, fk[1], fk[0], fecha_creacion)
                    )
                    i += 1
            except Exception as e:
                pass

    # Tabla AbogadoTrabaja 80% de n

    def genAbogadoTrabaja():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Abogado;")
        res = cursor.fetchall()
        while i < 0.8*n:
            try:
                fk = random.choice(res)
                nombre = random.choice(departamentos_nombres)

                cursor.execute(
                    f"INSERT INTO {schema}.AbogadoTrabaja (numero_documento_abogado, tipo_documento_abogado, nombre_departamento) VALUES (%s, %s, %s)",
                    (fk[1], fk[0], nombre)
                )
                i += 1
            except Exception as e:
                pass

    # Tabla SecretarioAsiste 60%*80% de n

    def genSecretarioAsiste():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Abogado;")
        res = cursor.fetchall()
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Secretario;")
        res2 = cursor.fetchall()
        while i < 0.6*0.8*n:
            try:
                fk = random.choice(res)
                fk2 = random.choice(res2)
                cursor.execute(
                    f"INSERT INTO {schema}.SecretarioAsiste (numero_documento_abogado, tipo_documento_abogado, numero_documento_secretario, tipo_documento_secretario) VALUES (%s, %s, %s, %s)",
                    (fk[1], fk[0], fk2[1], fk2[0])
                )
                i += 1
            except Exception as e:
                pass

    # Tabla PersonaParticipa 50% de n

    def genPersonaParticipa():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Persona;")
        res = cursor.fetchall()
        cursor.execute(f"SELECT codigo FROM {schema}.Caso;")
        res2 = cursor.fetchall()
        while i < 0.5*n:
            try:
                fk = random.choice(res)
                fk2 = random.choice(res2)
                tipo = random.choice(["testigo", "demandado", "demandante"])

                cursor.execute(
                    f"INSERT INTO {schema}.PersonaParticipa (numero_documento, tipo_documento, caso_codigo, tipo) VALUES (%s, %s, %s, %s)",
                    (fk[1], fk[0], fk2[0], tipo)
                )
                i += 1
            except Exception as e:
                pass

    # Tabla PersonaJuridica

    def genPersonaJuridica():
        for i in range(200):
            razon_social = fake.company()
            ruc = fake.unique.random_number(digits=11)
            try:
                cursor.execute(
                    f"INSERT INTO {schema}.PersonaJuridica (razon_social, ruc) VALUES (%s, %s)",
                    (razon_social, ruc)
                )
                i += 1
            except Exception as e:
                pass

    # Tabla PersonaRepresenta 50% de n

    def genPersonaRepresenta():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Persona;")
        res = cursor.fetchall()
        cursor.execute(f"SELECT ruc FROM {schema}.PersonaJuridica;")
        res2 = cursor.fetchall()
        cursor.execute(f"SELECT codigo FROM {schema}.Caso;")
        res3 = cursor.fetchall()
        while i < 0.5*n:
            try:
                fk = random.choice(res)
                fk2 = random.choice(res2)
                fk3 = random.choice(res3)

                cursor.execute(
                    f"INSERT INTO {schema}.PersonaRepresenta (numero_documento, tipo_documento, ruc, caso_codigo) VALUES (%s, %s, %s, %s)",
                    (fk[1], fk[0], fk2[0], fk3[0])
                )
                i += 1
            except Exception as e:
                pass

    # Tabla AbogadoParticipa 80% de n

    def genAbogadoParticipa():
        i = 0
        cursor.execute(
            f"SELECT tipo_documento, numero_documento FROM {schema}.Abogado;")
        res = cursor.fetchall()
        cursor.execute(f"SELECT codigo FROM {schema}.Caso;")
        res2 = cursor.fetchall()
        while i < 0.8*n:
            try:
                fk = random.choice(res)
                fk2 = random.choice(res2)

                cursor.execute(
                    f"INSERT INTO {schema}.AbogadoParticipa (numero_documento_abogado, tipo_documento_abogado, caso_codigo) VALUES (%s, %s, %s)",
                    (fk[1], fk[0], fk2[0])
                )
                i += 1
            except Exception as e:
                pass

    # Tabla Documento 50% de n

    def genDocumento():
        i = 0
        cursor.execute(f"SELECT codigo FROM {schema}.Caso;")
        res = cursor.fetchall()
        while i < 0.5*n:
            try:
                fk = random.choice(res)
                id = fake.uuid4()
                enlace = fake.url()
                fecha = fake.date_time_between(
                    start_date="-5y", end_date="now")
                nombre = fake.file_name(extension=random.choice(
                    ["pdf", "csv", "xlsx", "docs", "cpp", "py"]))
                procedencia = fake.random_element(
                    elements=("Cliente", "Contraparte", "Tribunal"))

                cursor.execute(
                    f"INSERT INTO {schema}.Documento (id, enlace, fecha, nombre, procedencia, codigo_caso) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, enlace, fecha, nombre, procedencia, fk[0])
                )
                i += 1
            except Exception as e:
                pass

    start_time = time.time()
    # Creating the data
    genPersonas()
    genCasos()
    genTelefonos()
    genEmpleados()
    genAbogados()
    genSecretarios()
    genDepartamentos()
    genAbogadoTrabaja()
    genSecretarioAsiste()
    genPersonaParticipa()
    genPersonaJuridica()
    genPersonaRepresenta()
    genAbogadoParticipa()
    genDocumento()

    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print(f"Time of execution for {n} elements: {elapsed_time} seconds")


if __name__ == "__main__":
    create_all(1000, "mil")
    create_all(10000, "diezmil")
    create_all(100000, "cienmil")
    create_all(1000000, "millon")

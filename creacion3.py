import psycopg2
from faker import Faker
import random
from dotenv import load_dotenv
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

# PersonaJuridica (
#   razon_social VARCHAR(50),
#   ruc VARCHAR(20),
#   PRIMARY KEY (ruc)
# );

cursor.execute("SELECT numero_documento, tipo_documento FROM Personas")
personas = cursor.fetchall()

cursor.execute("SELECT codigo FROM Casos")
casos = cursor.fetchall()


tuplas = 10

# tabla PersonaJuridica
razones = ["S.A.", "S.R.L", "S.C", "S.A.S"]
for _ in range(tuplas):
    razon_social = random.choice(razones)
    ruc = fake.unique.random_number(digits=11)

    cursor.execute(
        "INSERT INTO PersonaJuridica (razon_social, ruc) VALUES (%s, %s)",
        (razon_social, ruc)
    )


participacion = ["testigo", "demandado", "demandante"]
# TABLA personaparticipa
for _ in range(tuplas):
    [numero_documento, tipo_documento] = personas[_]
    caso_codigo = casos[_]
    tipo = random.choice(participacion)

    cursor.execute(
        "INSERT INTO PersonaParticipa (numero_documento, tipo_documento, caso_codigo, tipo) VALUES (%s, %s, %s, %s)",
        (numero_documento, tipo_documento, caso_codigo, tipo)
    )


# TABLA personarepresenta
cursor.execute("SELECT ruc FROM PersonaJuridica")
personajuridica = cursor.fetchall()

for _ in range(tuplas):
    [numero_documento, tipo_documento] = personas[_]
    ruc = personajuridica[_]
    caso_codigo = casos[_]

    cursor.execute(
        "INSERT INTO PersonaRepresenta (numero_documento, tipo_documento, ruc, caso_codigo) VALUES (%s, %s, %s, %s)",
        (numero_documento, tipo_documento, ruc, caso_codigo)
    )


conn.commit()
conn.close()

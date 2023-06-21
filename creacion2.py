import psycopg2
from faker import Faker

# Crear instancia de Faker
fake = Faker()

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="proyecto",
    user="postgres",
    password=""
)
cursor = conn.cursor()

num_registros = 10  # Número de registros a generar

cursor.execute('SELECT numero_documento, tipo_documento FROM Personas')
personas = cursor.fetchall()

cursor.execute('SELECT * FROM Empleados')
empleados = cursor.fetchall()

cursor.execute('SELECT numero_documento, tipo_documento FROM Abogados')
abogados = cursor.fetchall()

cursor.execute('SELECT numero_documento, tipo_documento FROM Secretarios')
secretarios = cursor.fetchall()

cursor.execute('SELECT codigo FROM Casos')
casos = cursor.fetchall()


departamentos_nombres = ["Civil", "Penal", "Laboral", "Familiar", "Mercantil",
                         "Administrativo", "Constitucional", "Tributario", "Ambiental", "Procesal"]
# Tabla Departamentos
for _ in range(20):
    nombre = "Dpto " + departamentos_nombres[(_ % 10)] + str(_ % 10+_//10 + 1)
    [numero_documento_abogado_responsable,
        tipo_documento_abogado_responsable] = abogados[_]
    fecha_creacion = fake.date_time_between(start_date="-5y", end_date="now")
    cursor.execute(
        "INSERT INTO Departamentos (nombre, numero_documento_abogado_responsable, tipo_documento_abogado_responsable, fecha_creacion) VALUES (%s, %s, %s, %s)",
        (nombre, numero_documento_abogado_responsable,
         tipo_documento_abogado_responsable, fecha_creacion)
    )


cursor.execute('SELECT nombre FROM Departamentos')
departamentos = cursor.fetchall()
# Tabla AbogadoParticipa
for _ in range(num_registros):
    [numero_documento_abogado, tipo_documento_abogado] = abogados[_]
    caso_codigo = casos[_]
    cursor.execute(
        "INSERT INTO AbogadoParticipa (numero_documento_abogado, tipo_documento_abogado, caso_codigo) VALUES (%s, %s, %s)",
        (numero_documento_abogado, tipo_documento_abogado, caso_codigo)
    )


# Tabla AbogadoTrabaja
for _ in range(num_registros):
    [numero_documento_abogado, tipo_documento_abogado] = abogados[_]
    nombre_departamento = departamentos[_]
    cursor.execute(
        "INSERT INTO AbogadoTrabaja (numero_documento_abogado, tipo_documento_abogado, nombre_departamento) VALUES (%s, %s, %s)",
        (numero_documento_abogado, tipo_documento_abogado, nombre_departamento)
    )


# Tabla Documentos
for _ in range(num_registros):
    id = fake.unique.random_number(digits=11)
    enlace = fake.url()
    fecha = fake.date_time_between(start_date="-5y", end_date="now")
    nombre = fake.file_name(extension="pdf")
    procedencia = fake.random_element(
        elements=("Cliente", "Contraparte", "Tribunal"))
    codigo_caso = casos[_]

    cursor.execute(
        "INSERT INTO Documentos (id, enlace, fecha, nombre, procedencia, codigo_caso) VALUES (%s, %s, %s, %s, %s, %s)",
        (id, enlace, fecha, nombre, procedencia, codigo_caso)
    )


# Tabla SecretarioAsiste
for _ in range(num_registros):
    [numero_documento_abogado, tipo_documento_abogado] = abogados[_]
    [numero_documento_secretario, tipo_documento_secretario] = secretarios[_]
    cursor.execute(
        "INSERT INTO SecretarioAsiste (numero_documento_abogado, tipo_documento_abogado, numero_documento_secretario, tipo_documento_secretario) VALUES (%s, %s, %s, %s)",
        (numero_documento_abogado, tipo_documento_abogado,
         numero_documento_secretario, tipo_documento_secretario)
    )

# Tabla Telefonos
for _ in range(num_registros):
    numero = '9' + str(fake.unique.random_number(digits=8))
    [numero_documento, tipo_documento] = personas[_]

    cursor.execute(
        "INSERT INTO Telefonos (numero, numero_documento, tipo_documento) VALUES (%s, %s, %s)",
        (numero, numero_documento, tipo_documento)
    )

conn.commit()
conn.close()

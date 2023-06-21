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

# Generar datos y poblar las tablas
num_registros = 100  # Número de registros a generar


# Tabla Personas
for _ in range(num_registros):
    tipo_documento = fake.random_element(
        elements=("DNI", "Pasaporte"))
    numero_documento = fake.unique.random_number(digits=8)
    nombre = fake.first_name()
    apellido = fake.last_name()
    sexo = fake.random_element(elements=("M", "F"))
    correo = fake.email()

    cursor.execute(
        f"INSERT INTO Personas (tipo_documento, numero_documento, nombre, apellido, sexo, correo) VALUES (%s, %s, %s, %s, %s, %s)",
        (tipo_documento, numero_documento, nombre, apellido, sexo, correo)
    )


cursor.execute('SELECT * FROM Personas')
personas = cursor.fetchall()
# Tabla Empleados
for _ in range(num_registros//2):
    [tipo_documento, numero_documento, nombre,
        apellido, sexo, correo] = personas[_]
    sueldo = fake.random_int(min=2000, max=10000)
    fecha_inicio = fake.date_time_between(start_date="-5y", end_date="now")
    tiempo_parcial = fake.random_element(elements=(True, False))

    cursor.execute(
        "INSERT INTO Empleados (numero_documento, tipo_documento, nombre, apellido, sexo, correo, sueldo, fecha_inicio, tiempo_parcial) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (numero_documento, tipo_documento, nombre, apellido,
         sexo, correo, sueldo, fecha_inicio, tiempo_parcial)
    )

# Tabla Abogados
for _ in range(num_registros//3):
    [tipo_documento, numero_documento, nombre,
        apellido, sexo, correo] = personas[_]
    sueldo = fake.random_int(min=2000, max=10000)
    fecha_inicio = fake.date_time_between(start_date="-5y", end_date="now")
    tiempo_parcial = fake.random_element(elements=(True, False))
    especializacion = fake.random_element(
        elements=("Civil", "Penal", "Laboral", "Familiar", "Mercantil"))
    numero_colegiatura = fake.random_number(digits=6)
    casos_ganados = fake.random_int(min=0, max=100)
    casos_perdidos = fake.random_int(min=0, max=100)

    cursor.execute(
        "INSERT INTO Abogados (numero_documento, tipo_documento, nombre, apellido, sexo, correo, sueldo, fecha_inicio, tiempo_parcial, especializacion, numero_colegiatura, casos_ganados, casos_perdidos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (numero_documento, tipo_documento, nombre, apellido, sexo, correo, sueldo, fecha_inicio,
         tiempo_parcial, especializacion, numero_colegiatura, casos_ganados, casos_perdidos)
    )


# Tabla Secretarios
for _ in range(num_registros//4):
    [tipo_documento, numero_documento, nombre,
        apellido, sexo, correo] = personas[_]
    formacion_tecnica = fake.random_element(elements=(True, False))
    tiempo_parcial = fake.random_element(elements=(True, False))

    cursor.execute(
        "INSERT INTO Secretarios (numero_documento, tipo_documento, nombre, apellido, sexo, correo, formacion_tecnica, tiempo_parcial) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (numero_documento, tipo_documento, nombre, apellido,
         sexo, correo, formacion_tecnica, tiempo_parcial)
    )


# Tabla Casos
for _ in range(num_registros):
    codigo = fake.unique.random_number(digits=6)
    nombre = "Caso numero" + str(fake.unique.random_number(digits=6))
    estado = fake.random_element(elements=("En proceso", "Finalizado"))
    fecha_inicio = fake.date_time_between(start_date="-5y", end_date="now")
    fecha_fin = fake.date_time_between(start_date=fecha_inicio, end_date="now")
    tipo_caso = fake.random_element(
        elements=("Civil", "Penal", "Laboral", "Familiar", "Mercantil"))

    cursor.execute(
        "INSERT INTO Casos (codigo, nombre, estado, fecha_inicio, fecha_fin, tipo_caso) VALUES (%s, %s, %s, %s, %s, %s)",
        (codigo, nombre, estado, fecha_inicio, fecha_fin, tipo_caso)
    )

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

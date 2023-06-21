import psycopg2
from faker import Faker

# Crear instancia de Faker
fake = Faker()

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="firma",
    user="postgres",
    password=""
)
cursor = conn.cursor()

# Aquí puedes ejecutar tus consultas y operaciones en la base de datos utilizando el cursor

# Ejemplo: Crear una tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        edad INTEGER,
        email TEXT
    )
''')

# Generar datos y poblar la tabla
num_registros = 1000000  # Número de registros a generar

for _ in range(num_registros):
    nombre = fake.name()
    edad = fake.random_int(min=18, max=65)
    email = fake.email()

    # Insertar datos en la tabl
    cursor.execute(
        "INSERT INTO usuarios (nombre, edad, email) VALUES (%s, %s, %s)", (nombre, edad, email))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

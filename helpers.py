from typing import List
from pylatex import Tabular, MultiColumn, Table, Center


# times es el arreglo de tiempos por cada esquema -> [tiempos_del_esquema1k, tiempos_del_esquema10k, tiempos_del_esquema100k, tiempos_del_esquema1M]
def create_latex_table(title: str, times: List[List[float]], iterations: int, has_indexes: bool):

    table = Table()
    center = Center()

    # Generate data table
    table1 = Tabular('|l|l|l|l|l|', width=5, col_space="0.3in")
    table1.add_hline()
    table1.add_row((MultiColumn(5, align='|c|', data=title),))
    table1.add_hline()
    table1.add_row(("Ejecución", "1K", "10k", "100k", "1M"))
    table1.add_hline()

    print(len(times[0]))
    for i in range(iterations):
        table1.add_row((i+1, times[0][i], times[1]
                       [i], times[2][i], times[3][i]))
        table1.add_hline()

    # Promedio
    table1.add_row(("Promedio", times[0][iterations], times[1]
                   [iterations], times[2][iterations], times[3][iterations]))
    table1.add_hline()
    # Desviación Estándar
    table1.add_row(("Desviación Estándar", times[0][iterations+1], times[1]
                   [iterations+1], times[2][iterations+1], times[3][iterations+1]))
    table1.add_hline()

    center.append(table1)
    table.append(center)
    table.add_caption(
        title + " con índices" if has_indexes else title + " sin índices")

    table.generate_tex("TablasConIndices/" +
                       title if has_indexes else "TablasSinIndices/"+title)


def create_tables(squema):
    return f"""
-- Tabla Personas
CREATE TABLE IF NOT EXISTS {squema}.Persona (
  tipo_documento VARCHAR(15) CHECK ( tipo_documento IN ('Pasaporte', 'DNI') ),
  numero_documento VARCHAR(20),
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(70) NOT NULL,
  sexo VARCHAR(1) NOT NULL CHECK(sexo IN ('F', 'M', 'O')),
  correo VARCHAR(70) NOT NULL CHECK(correo LIKE '%__@__%.__%'),
  PRIMARY KEY (tipo_documento, numero_documento)
);

-- Tabla Telefonos
CREATE TABLE IF NOT EXISTS {squema}.Telefono (
  numero VARCHAR(15),
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  PRIMARY KEY (numero),
  FOREIGN KEY (numero_documento, tipo_documento) REFERENCES {squema}.Persona(numero_documento, tipo_documento)
);

-- Tabla Empleados
CREATE TABLE IF NOT EXISTS {squema}.Empleado (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  sueldo INT NOT NULL CHECK(sueldo >= 0),
  fecha_inicio TIMESTAMP NOT NULL,
  tiempo_parcial BOOLEAN NOT NULL,
    PRIMARY KEY (numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES {squema}.Persona(numero_documento, tipo_documento)
);

-- Tabla Abogados
CREATE TABLE IF NOT EXISTS {squema}.Abogado (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  especializacion VARCHAR(20) NOT NULL CHECK ( especializacion IN ('Civil', 'Penal', 'Laboral', 'Familiar', 'Mercantil') ),
  numero_colegiatura VARCHAR(20) NOT NULL,
  casos_ganados SMALLINT CHECK(casos_ganados >= 0),
  casos_perdidos SMALLINT CHECK(casos_perdidos >= 0),
    PRIMARY KEY (numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES {squema}.Empleado(numero_documento, tipo_documento)
);

-- Tabla Secretarios
CREATE TABLE IF NOT EXISTS {squema}.Secretario (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  formacion_tecnica BOOLEAN NOT NULL,
    PRIMARY KEY (numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES {squema}.Empleado(numero_documento, tipo_documento)
);

-- Tabla Departamentos
CREATE TABLE IF NOT EXISTS {squema}.Departamento (
    nombre VARCHAR(20),
    numero_documento_abogado_responsable VARCHAR(20),
    tipo_documento_abogado_responsable VARCHAR(15),
    fecha_creacion TIMESTAMP NOT NULL,
    PRIMARY KEY (nombre),
    FOREIGN KEY (numero_documento_abogado_responsable, tipo_documento_abogado_responsable) REFERENCES {squema}.Abogado(numero_documento, tipo_documento)
);

-- Tabla Casos
CREATE TABLE IF NOT EXISTS {squema}.Caso (
  codigo VARCHAR(20),
  nombre VARCHAR(30) NOT NULL,
  estado VARCHAR(10) NOT NULL CHECK(estado IN ('Registrado', 'EnProceso', 'Culminado')),
  fecha_inicio TIMESTAMP NOT NULL,
  fecha_fin TIMESTAMP,
  tipo_caso VARCHAR(9) NOT NULL CHECK (tipo_caso IN ('Civil', 'Penal', 'Laboral', 'Familiar', 'Mercantil') ),
  PRIMARY KEY (codigo)
);


-- Tabla AbogadoTrabaja
CREATE TABLE IF NOT EXISTS {squema}.AbogadoTrabaja (
  numero_documento_abogado VARCHAR(20),
  tipo_documento_abogado VARCHAR(15),
  nombre_departamento VARCHAR(20),
    PRIMARY KEY (numero_documento_abogado, tipo_documento_abogado, nombre_departamento),
    FOREIGN KEY (numero_documento_abogado, tipo_documento_abogado) REFERENCES {squema}.Abogado(numero_documento, tipo_documento),
    FOREIGN KEY (nombre_departamento) REFERENCES {squema}.Departamento(nombre)
);


-- Tabla SecretarioAsiste
CREATE TABLE IF NOT EXISTS {squema}.SecretarioAsiste (
    numero_documento_abogado VARCHAR(20),
    tipo_documento_abogado VARCHAR(15),
    numero_documento_secretario VARCHAR(20),
    tipo_documento_secretario VARCHAR(15),
    PRIMARY KEY (numero_documento_abogado, tipo_documento_abogado),
    FOREIGN KEY (numero_documento_abogado, tipo_documento_abogado) REFERENCES {squema}.Abogado(numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento_secretario, tipo_documento_secretario) REFERENCES {squema}.Secretario(numero_documento, tipo_documento)
);

-- Tabla PersonaJuridica
CREATE TABLE IF NOT EXISTS {squema}.PersonaJuridica (
  razon_social VARCHAR(50) NOT NULL,
  ruc VARCHAR(20),
  PRIMARY KEY (ruc)
);

-- Tabla PersonaParticipa
CREATE TABLE IF NOT EXISTS {squema}.PersonaParticipa (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  caso_codigo VARCHAR(20),
  tipo VARCHAR(10) NOT NULL CHECK(tipo IN ('testigo', 'demandado', 'demandante')),
    PRIMARY KEY (numero_documento, tipo_documento, caso_codigo),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES {squema}.Persona(numero_documento, tipo_documento),
    FOREIGN KEY (caso_codigo) REFERENCES {squema}.Caso(codigo)
);

-- Tabla PersonaRepresenta
CREATE TABLE IF NOT EXISTS {squema}.PersonaRepresenta (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  ruc VARCHAR(20),
  caso_codigo VARCHAR(20),
    PRIMARY KEY (numero_documento, tipo_documento, ruc, caso_codigo),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES {squema}.Persona(numero_documento, tipo_documento),
    FOREIGN KEY (ruc) REFERENCES {squema}.PersonaJuridica(ruc),
    FOREIGN KEY (caso_codigo) REFERENCES {squema}.Caso(codigo)
);


-- Tabla AbogadoParticipa
CREATE TABLE IF NOT EXISTS {squema}.AbogadoParticipa (
  numero_documento_abogado VARCHAR(20),
  tipo_documento_abogado VARCHAR(15),
  caso_codigo VARCHAR(20),
    PRIMARY KEY (numero_documento_abogado, tipo_documento_abogado, caso_codigo),
    FOREIGN KEY (numero_documento_abogado, tipo_documento_abogado) REFERENCES {squema}.Abogado(numero_documento, tipo_documento),
    FOREIGN KEY (caso_codigo) REFERENCES {squema}.Caso(codigo)
);

-- Tabla Documentos
CREATE TABLE IF NOT EXISTS {squema}.Documento (
  id uuid DEFAULT gen_random_uuid(),
  enlace VARCHAR(100) NOT NULL,
  fecha TIMESTAMP NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  procedencia VARCHAR(20) NOT NULL CHECK ( procedencia IN ('Cliente', 'Contraparte', 'Tribunal') ),
  codigo_caso VARCHAR(20),
  PRIMARY KEY (id),
  FOREIGN KEY (codigo_caso) REFERENCES {squema}.Caso(codigo)
);
"""


def drop_tables(squema):
    return f"""
    -- Tabla Documentos
DROP TABLE IF EXISTS {squema}.Documento;

-- Tabla AbogadoParticipa
DROP TABLE IF EXISTS {squema}.AbogadoParticipa;

-- Tabla PersonaRepresenta
DROP TABLE IF EXISTS {squema}.PersonaRepresenta;

-- Tabla PersonaParticipa
DROP TABLE IF EXISTS {squema}.PersonaParticipa;

-- Tabla PersonaJuridica
DROP TABLE IF EXISTS {squema}.PersonaJuridica;

-- Tabla SecretarioAsiste
DROP TABLE IF EXISTS {squema}.SecretarioAsiste;

-- Tabla AbogadoTrabaja
DROP TABLE IF EXISTS {squema}.AbogadoTrabaja;

-- Tabla Casos
DROP TABLE IF EXISTS {squema}.Caso;

-- Tabla Departamentos
DROP TABLE IF EXISTS {squema}.Departamento;

-- Tabla Secretario
DROP TABLE IF EXISTS {squema}.Secretario;

-- Tabla Abogado
DROP TABLE IF EXISTS {squema}.Abogado;

-- Tabla Empleados
DROP TABLE IF EXISTS {squema}.Empleado;

-- Tabla Telefonos
DROP TABLE IF EXISTS {squema}.Telefono;

-- Tabla Persona
DROP TABLE IF EXISTS {squema}.Persona;
"""


def FunVacuum(squema):
    return f"""
    -- Funcion para limpiar la base de datos
CREATE OR REPLACE FUNCTION {squema}.vacuum() RETURNS void AS $$
DECLARE
    tablas RECORD;
BEGIN
    FOR tablas IN
        SELECT tablename FROM pg_tables WHERE schemaname = '{squema}'
    LOOP
        EXECUTE 'VACUUM ' || quote_ident(tablas.tablename) || ';';
    END LOOP;
END;
$$ LANGUAGE plpgsql;
"""


def create_indexes(squema):
    return f"""
    -- Indices de la base de datos
    -- Índices para la tabla Empleado
CREATE INDEX IF NOT EXISTS idx_empleado_sueldo ON {squema}.Empleado USING btree (sueldo);
CREATE INDEX IF NOT EXISTS idx_empleado_fecha_inicio ON {squema}.Empleado USING btree (fecha_inicio);

-- Índices para la tabla Abogado
CREATE INDEX IF NOT EXISTS idx_abogado_casos_ganados ON {squema}.Abogado USING btree (casos_ganados);
CREATE INDEX IF NOT EXISTS idx_abogado_casos_ganados ON {squema}.Abogado USING btree (casos_perdidos);

-- Índices para la tabla Persona
CREATE INDEX IF NOT EXISTS idx_persona_sexo ON {squema}.Persona USING hash (sexo);

-- Índices para la tabla Departamento
CREATE INDEX IF NOT EXISTS idx_departamento_nombre ON {squema}.Departamento USING hash (nombre);
CREATE INDEX IF NOT EXISTS idx_departamento_fecha_creacion ON {squema}.Departamento USING btree (fecha_creacion);

-- Índices para la tabla PersonaJuridica
CREATE INDEX IF NOT EXISTS idx_personajuridica_ruc ON {squema}.PersonaJuridica USING hash (ruc);
"""


def drop_indexes(squema):
    return f"""
    -- Indices de la base de datos
    -- Índices para la tabla Empleado
    -- Tabla Empleado
DROP INDEX IF EXISTS {squema}.idx_empleado_sueldo;
DROP INDEX IF EXISTS {squema}.idx_empleado_fecha_inicio;

-- Tabla Abogado
DROP INDEX IF EXISTS {squema}.idx_abogado_casos_ganados;
DROP INDEX IF EXISTS {squema}.idx_abogado_casos_perdidos;


-- Tabla Persona
DROP INDEX IF EXISTS {squema}.idx_persona_sexo;

-- Tabla Departamento
DROP INDEX IF EXISTS {squema}.idx_departamento_nombre;
DROP INDEX IF EXISTS {squema}.idx_departamento_fecha_creacion;

-- Tabla PersonaJuridica
DROP INDEX IF EXISTS {squema}.idx_personajuridica_ruc;

"""

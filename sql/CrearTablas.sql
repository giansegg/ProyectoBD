
-- Tabla Personas
CREATE TABLE IF NOT EXISTS Persona (
  tipo_documento VARCHAR(15) CHECK ( tipo_documento IN ('Pasaporte', 'DNI') ),
  numero_documento VARCHAR(20),
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(70) NOT NULL,
  sexo VARCHAR(1) NOT NULL CHECK(sexo IN ('F', 'M', 'O')),
  correo VARCHAR(70) NOT NULL CHECK(correo LIKE '%__@__%.__%'),
  PRIMARY KEY (numero_documento)
);

-- Tabla Telefonos
CREATE TABLE IF NOT EXISTS Telefono (
  numero VARCHAR(15),
  numero_documento VARCHAR(20),
  PRIMARY KEY (numero),
  FOREIGN KEY (numero_documento) REFERENCES Persona(numero_documento)
);

-- Tabla Empleados
CREATE TABLE IF NOT EXISTS Empleado (
  numero_documento VARCHAR(20),
  sueldo INT NOT NULL CHECK(sueldo >= 0),
  fecha_inicio TIMESTAMP NOT NULL,
  tiempo_parcial BOOLEAN NOT NULL,
    PRIMARY KEY (numero_documento),
    FOREIGN KEY (numero_documento) REFERENCES Persona(numero_documento)
);

-- Tabla Abogados
CREATE TABLE IF NOT EXISTS Abogado (
  numero_documento VARCHAR(20),
  especializacion VARCHAR(20) NOT NULL CHECK ( especializacion IN ('Civil', 'Penal', 'Laboral', 'Familiar', 'Mercantil') ),
  numero_colegiatura VARCHAR(20) NOT NULL,
  casos_ganados SMALLINT CHECK(casos_ganados >= 0),
  casos_perdidos SMALLINT CHECK(casos_perdidos >= 0),
    PRIMARY KEY (numero_documento),
    FOREIGN KEY (numero_documento) REFERENCES Empleado(numero_documento)
);

select * from abogado join secretario s on Abogado.numero_documento = s.numero_documento;

-- Tabla Secretarios
CREATE TABLE IF NOT EXISTS Secretario (
  numero_documento VARCHAR(20),
  formacion_tecnica BOOLEAN NOT NULL,
    PRIMARY KEY (numero_documento),
    FOREIGN KEY (numero_documento) REFERENCES Empleado(numero_documento)
);

-- Tabla Departamentos
CREATE TABLE IF NOT EXISTS Departamento (
    nombre VARCHAR(20),
    numero_documento_abogado_responsable VARCHAR(20),
    fecha_creacion TIMESTAMP NOT NULL,
    PRIMARY KEY (nombre),
    FOREIGN KEY (numero_documento_abogado_responsable) REFERENCES Abogado(numero_documento)
);

-- Tabla Casos
CREATE TABLE IF NOT EXISTS Caso (
  codigo VARCHAR(20),
  nombre VARCHAR(30) NOT NULL,
  estado VARCHAR(10) NOT NULL CHECK(estado IN ('Registrado', 'EnProceso', 'Culminado')),
  fecha_inicio TIMESTAMP NOT NULL,
  fecha_fin TIMESTAMP,
  tipo_caso VARCHAR(9) NOT NULL CHECK (tipo_caso IN ('Civil', 'Penal', 'Laboral', 'Familiar', 'Mercantil') ),
  PRIMARY KEY (codigo)
);


-- Tabla AbogadoTrabaja
CREATE TABLE IF NOT EXISTS AbogadoTrabaja (
  numero_documento_abogado VARCHAR(20),
  nombre_departamento VARCHAR(20),
    PRIMARY KEY (numero_documento_abogado, nombre_departamento),
    FOREIGN KEY (numero_documento_abogado) REFERENCES Abogado(numero_documento),
    FOREIGN KEY (nombre_departamento) REFERENCES Departamento(nombre)
);


-- Tabla SecretarioAsiste
CREATE TABLE IF NOT EXISTS SecretarioAsiste (
    numero_documento_abogado VARCHAR(20),

    numero_documento_secretario VARCHAR(20),

    PRIMARY KEY (numero_documento_abogado),
    FOREIGN KEY (numero_documento_abogado) REFERENCES Abogado(numero_documento),
    FOREIGN KEY (numero_documento_secretario) REFERENCES Secretario(numero_documento)
);

-- Tabla PersonaJuridica
CREATE TABLE IF NOT EXISTS PersonaJuridica (
  razon_social VARCHAR(50) NOT NULL,
  ruc VARCHAR(20),
  PRIMARY KEY (ruc)
);

-- Tabla PersonaParticipa
CREATE TABLE IF NOT EXISTS PersonaParticipa (
  numero_documento VARCHAR(20),
  caso_codigo VARCHAR(20),
  tipo VARCHAR(10) NOT NULL CHECK(tipo IN ('testigo', 'demandado', 'demandante')),
    PRIMARY KEY (numero_documento, caso_codigo),
    FOREIGN KEY (numero_documento) REFERENCES Persona(numero_documento),
    FOREIGN KEY (caso_codigo) REFERENCES Caso(codigo)
);

-- Tabla PersonaRepresenta
CREATE TABLE IF NOT EXISTS PersonaRepresenta (
  numero_documento VARCHAR(20),
  ruc VARCHAR(20),
  caso_codigo VARCHAR(20),
    PRIMARY KEY (numero_documento, ruc, caso_codigo),
    FOREIGN KEY (numero_documento) REFERENCES Persona(numero_documento),
    FOREIGN KEY (ruc) REFERENCES PersonaJuridica(ruc),
    FOREIGN KEY (caso_codigo) REFERENCES Caso(codigo)
);


-- Tabla AbogadoParticipa
CREATE TABLE IF NOT EXISTS AbogadoParticipa (
  numero_documento_abogado VARCHAR(20),
  caso_codigo VARCHAR(20),
    PRIMARY KEY (numero_documento_abogado, caso_codigo),
    FOREIGN KEY (numero_documento_abogado) REFERENCES Abogado(numero_documento),
    FOREIGN KEY (caso_codigo) REFERENCES Caso(codigo)
);

-- Tabla Documentos
CREATE TABLE IF NOT EXISTS Documento (
  id uuid DEFAULT gen_random_uuid(),
  enlace VARCHAR(100) NOT NULL,
  fecha TIMESTAMP NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  procedencia VARCHAR(20) NOT NULL CHECK ( procedencia IN ('Cliente', 'Contraparte', 'Tribunal') ),
  codigo_caso VARCHAR(20),
  PRIMARY KEY (id),
  FOREIGN KEY (codigo_caso) REFERENCES Caso(codigo)
);
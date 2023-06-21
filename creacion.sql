
-- Tabla Personas
CREATE TABLE IF NOT EXISTS Personas (
  tipo_documento VARCHAR(15),
  numero_documento VARCHAR(20),
  nombre VARCHAR(50),
  apellido VARCHAR(70),
  sexo VARCHAR(1),
  correo VARCHAR(70),
  PRIMARY KEY (tipo_documento, numero_documento)
);

-- Tabla Telefonos
CREATE TABLE IF NOT EXISTS Telefonos (
  numero VARCHAR(15),
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  PRIMARY KEY (numero),
  FOREIGN KEY (numero_documento, tipo_documento) REFERENCES Personas(numero_documento, tipo_documento)
);


-- Tabla Empleados
CREATE TABLE IF NOT EXISTS Empleados (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  sueldo INT,
  fecha_inicio TIMESTAMP,
  tiempo_parcial BOOLEAN,
    PRIMARY KEY (numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES Personas(numero_documento, tipo_documento)
) INHERITS (Personas);

-- Tabla Abogados
CREATE TABLE IF NOT EXISTS Abogados (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  especializacion VARCHAR(20),
  numero_colegiatura VARCHAR(20),
  casos_ganados SMALLINT,
  casos_perdidos SMALLINT,
    PRIMARY KEY (numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES Empleados(numero_documento, tipo_documento)
) INHERITS (Empleados);

-- Tabla Secretarios
CREATE TABLE IF NOT EXISTS Secretarios (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  formacion_tecnica BOOLEAN,
    PRIMARY KEY (numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES Empleados(numero_documento, tipo_documento)
) INHERITS (Empleados);

-- Tabla Departamentos
CREATE TABLE IF NOT EXISTS Departamentos (
    nombre VARCHAR(20),
    numero_documento_abogado_responsable VARCHAR(20),
    tipo_documento_abogado_responsable VARCHAR(15),
    fecha_creacion TIMESTAMP,
    PRIMARY KEY (nombre),
    FOREIGN KEY (numero_documento_abogado_responsable, tipo_documento_abogado_responsable) REFERENCES Abogados(numero_documento, tipo_documento)
);

-- Tabla Casos
CREATE TABLE IF NOT EXISTS Casos (
  codigo VARCHAR(20),
  nombre VARCHAR(30),
  estado VARCHAR(20),
  fecha_inicio TIMESTAMP,
  fecha_fin TIMESTAMP,
  tipo_caso VARCHAR(50),
  PRIMARY KEY (codigo)
);


-- Tabla AbogadoTrabaja
CREATE TABLE IF NOT EXISTS AbogadoTrabaja (
  numero_documento_abogado VARCHAR(20),
  tipo_documento_abogado VARCHAR(15),
  nombre_departamento VARCHAR(20),
    PRIMARY KEY (numero_documento_abogado, tipo_documento_abogado, nombre_departamento),
    FOREIGN KEY (numero_documento_abogado, tipo_documento_abogado) REFERENCES Abogados(numero_documento, tipo_documento),
    FOREIGN KEY (nombre_departamento) REFERENCES Departamentos(nombre)
);

-- Tabla SecretarioAsiste
CREATE TABLE IF NOT EXISTS SecretarioAsiste (
    numero_documento_abogado VARCHAR(20),
    tipo_documento_abogado VARCHAR(15),
    numero_documento_secretario VARCHAR(20),
    tipo_documento_secretario VARCHAR(15),
    PRIMARY KEY (numero_documento_abogado, tipo_documento_abogado),
    FOREIGN KEY (numero_documento_abogado, tipo_documento_abogado) REFERENCES Abogados(numero_documento, tipo_documento),
    FOREIGN KEY (numero_documento_secretario, tipo_documento_secretario) REFERENCES Secretarios(numero_documento, tipo_documento)
);

-- Tabla PersonaJuridica
CREATE TABLE IF NOT EXISTS PersonaJuridica (
  razon_social VARCHAR(50),
  ruc VARCHAR(20),
  PRIMARY KEY (ruc)
);

-- Tabla PersonaParticipa
CREATE TABLE IF NOT EXISTS PersonaParticipa (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  caso_codigo VARCHAR(20),
  tipo VARCHAR(10),
    PRIMARY KEY (numero_documento, tipo_documento, caso_codigo),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES Personas(numero_documento, tipo_documento),
    FOREIGN KEY (caso_codigo) REFERENCES Casos(codigo)
);

-- Tabla PersonaRepresenta
CREATE TABLE IF NOT EXISTS PersonaRepresenta (
  numero_documento VARCHAR(20),
  tipo_documento VARCHAR(15),
  ruc VARCHAR(20),
  caso_codigo VARCHAR(20),
    PRIMARY KEY (numero_documento, tipo_documento, ruc, caso_codigo),
    FOREIGN KEY (numero_documento, tipo_documento) REFERENCES Personas(numero_documento, tipo_documento),
    FOREIGN KEY (ruc) REFERENCES PersonaJuridica(ruc),
    FOREIGN KEY (caso_codigo) REFERENCES Casos(codigo)
);


-- Tabla AbogadoParticipa
CREATE TABLE IF NOT EXISTS AbogadoParticipa (
  numero_documento_abogado VARCHAR(20),
  tipo_documento_abogado VARCHAR(15),
  caso_codigo VARCHAR(20),
    PRIMARY KEY (numero_documento_abogado, tipo_documento_abogado, caso_codigo),
    FOREIGN KEY (numero_documento_abogado, tipo_documento_abogado) REFERENCES Abogados(numero_documento, tipo_documento),
    FOREIGN KEY (caso_codigo) REFERENCES Casos(codigo)
);

-- Tabla Documentos
CREATE TABLE IF NOT EXISTS Documentos (
  id VARCHAR(11),
  enlace VARCHAR(100),
  fecha TIMESTAMP,
  nombre VARCHAR(50),
  procedencia VARCHAR(20),
  codigo_caso VARCHAR(20),
  PRIMARY KEY (id),
  FOREIGN KEY (codigo_caso) REFERENCES Casos(codigo)
);
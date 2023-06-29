-- Índices para la tabla Empleado
CREATE INDEX idx_empleado_sueldo ON Empleado USING btree (sueldo);
CREATE INDEX idx_empleado_fecha_inicio ON Empleado USING hash (fecha_inicio);

-- Índices para la tabla Abogado
CREATE INDEX idx_abogado_casos_ganados ON Abogado USING btree (casos_ganados);
CREATE INDEX idx_abogado_tipo_doc_numero_doc ON Abogado USING hash (tipo_documento, numero_documento);
CREATE INDEX idx_abogado_fecha_inicio ON Abogado USING btree (fecha_inicio);

-- Índices para la tabla Caso
CREATE INDEX idx_caso_estado ON Caso USING hash (estado);

-- Índices para la tabla AbogadoParticipa
CREATE INDEX idx_abogado_participa_tipo_doc_abogado ON AbogadoParticipa USING hash (tipo_documento_abogado);

-- Índices para la tabla Persona
CREATE INDEX idx_persona_sexo ON Persona USING hash (sexo);

-- Índices para la tabla Departamento
CREATE INDEX idx_departamento_nombre ON Departamento USING hash (nombre);
CREATE INDEX idx_departamento_fecha_creacion ON Departamento USING btree (fecha_creacion);

-- Índices para la tabla PersonaJuridica
CREATE INDEX idx_personajuridica_ruc ON PersonaJuridica USING hash (ruc);

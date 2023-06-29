-- Tabla Empleado
DROP INDEX IF EXISTS idx_empleado_sueldo;
DROP INDEX IF EXISTS idx_empleado_fecha_inicio;

-- Tabla Abogado
DROP INDEX IF EXISTS idx_abogado_casos_ganados;
DROP INDEX IF EXISTS idx_abogado_tipo_doc_numero_doc;
DROP INDEX IF EXISTS idx_abogado_fecha_inicio;

-- Tabla Caso
DROP INDEX IF EXISTS idx_caso_estado;

-- Tabla AbogadoParticipa
DROP INDEX IF EXISTS idx_abogado_participa_tipo_doc_abogado;

-- Tabla Persona
DROP INDEX IF EXISTS idx_persona_sexo;

-- Tabla Departamento
DROP INDEX IF EXISTS idx_departamento_nombre;
DROP INDEX IF EXISTS idx_departamento_fecha_creacion;

-- Tabla PersonaJuridica
DROP INDEX IF EXISTS idx_personajuridica_ruc;
